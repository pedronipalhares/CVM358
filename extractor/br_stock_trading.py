# Libraries
import pandas as pd
import requests
import numpy as np
from datetime import datetime
import ssl
import warnings
from bs4 import BeautifulSoup
from io import BytesIO
import logging
from urllib3.util.ssl_ import create_urllib3_context
import re
import os
import tempfile
import utils
import concurrent.futures
from functools import lru_cache
import hashlib
from pathlib import Path
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import zipfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress only the specific warning about unverified HTTPS requests
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Suppress HTTPS verification warnings
requests.packages.urllib3.disable_warnings()

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = requests.packages.urllib3.util.ssl_.create_urllib3_context()
        ctx.check_hostname = False
        ctx.verify_mode = 0
        kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

def create_session():
    """Create a session with retry logic and connection pooling."""
    session = requests.Session()
    session.mount('https://', TLSAdapter())
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    # Mount the adapter with retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session

def download_and_extract_zip(url, temp_dir):
    """Download and extract a zip file."""
    try:
        session = create_session()
        response = session.get(url, verify=False)
        response.raise_for_status()
        
        # Create a BytesIO object from the content
        zip_content = BytesIO(response.content)
        
        # Extract the zip file
        with zipfile.ZipFile(zip_content) as zip_ref:
            # Extract all files to the temporary directory
            zip_ref.extractall(temp_dir)
            
            # Get list of extracted CSV files
            csv_files = [temp_dir / f for f in zip_ref.namelist() if f.endswith('.csv')]
            
            return csv_files
    except Exception as e:
        logger.error(f"Error downloading or extracting zip file: {str(e)}")
        raise

def process_trading_data(csv_files):
    """Process the trading data from CSV files."""
    try:
        consolidated_data = []
        individual_data = []
        
        for csv_path in csv_files:
            try:
                # Read CSV file with proper encoding for Brazilian Portuguese
                df = pd.read_csv(csv_path, encoding='latin1', sep=';', decimal=',')
                logger.info(f"Processing file: {csv_path.name}")
                
                # Add file type information and process accordingly
                if '_con_' in str(csv_path).lower():
                    df['File_Type'] = 'Consolidated'
                    # Mapping for consolidated files
                    columns_mapping = {
                        'CNPJ_Companhia': 'Company_CNPJ',
                        'Nome_Companhia': 'Company_Name',
                        'Data_Referencia': 'Reference_Date',
                        'Versao': 'Version',
                        'Tipo_Empresa': 'Company_Type',
                        'Empresa': 'Company',
                        'Tipo_Cargo': 'Position_Type',
                        'Tipo_Movimentacao': 'Movement_Type',
                        'Descricao_Movimentacao': 'Movement_Description',
                        'Tipo_Operacao': 'Operation_Type',
                        'Tipo_Ativo': 'Asset_Type',
                        'Caracteristica_Valor_Mobiliario': 'Security_Characteristic',
                        'Intermediario': 'Intermediary',
                        'Data_Movimentacao': 'Movement_Date',
                        'Quantidade': 'Quantity',
                        'Preco_Unitario': 'Unit_Price',
                        'Volume': 'Volume',
                        'File_Type': 'File_Type'
                    }
                    # Rename columns that exist in the data
                    df = df.rename(columns={k: v for k, v in columns_mapping.items() if k in df.columns})
                    consolidated_data.append(df)
                else:
                    df['File_Type'] = 'Individual'
                    # Mapping for individual files
                    columns_mapping = {
                        'CNPJ_Companhia': 'Company_CNPJ',
                        'Nome_Companhia': 'Company_Name',
                        'Data_Referencia': 'Reference_Date',
                        'Versao': 'Version',
                        'Codigo_CVM': 'CVM_Code',
                        'Categoria': 'Category',
                        'Tipo': 'Type',
                        'Data_Entrega': 'Delivery_Date',
                        'Tipo_Apresentacao': 'Presentation_Type',
                        'Motivo_Reapresentacao': 'Restatement_Reason',
                        'Protocolo_Entrega': 'Delivery_Protocol',
                        'Link_Download': 'Download_Link',
                        'File_Type': 'File_Type'
                    }
                    # Rename columns that exist in the data
                    df = df.rename(columns={k: v for k, v in columns_mapping.items() if k in df.columns})
                    individual_data.append(df)
                    
            except Exception as e:
                logger.error(f"Error processing file {csv_path}: {str(e)}")
                continue
        
        # Process consolidated data
        if consolidated_data:
            combined_consolidated = pd.concat(consolidated_data, ignore_index=True)
            # Convert date columns
            combined_consolidated['Reference_Date'] = pd.to_datetime(combined_consolidated['Reference_Date'])
            combined_consolidated['Movement_Date'] = pd.to_datetime(combined_consolidated['Movement_Date'])
            
            # Convert Version to numeric, replacing non-numeric versions with NaN
            combined_consolidated['Version'] = pd.to_numeric(combined_consolidated['Version'], errors='coerce')
            
            # Group by key fields and get the latest version
            key_fields = ['Reference_Date', 'Company_CNPJ', 'Company_Name', 'Movement_Date', 'Movement_Type']
            combined_consolidated = (combined_consolidated
                .sort_values(['Reference_Date', 'Version'], ascending=[True, False])
                .groupby(key_fields, as_index=False)
                .first()
                .sort_values('Reference_Date')
                .reset_index(drop=True))
            
            # Log version information
            logger.info(f"Consolidated data version range: {combined_consolidated['Version'].min()} to {combined_consolidated['Version'].max()}")
            logger.info(f"Number of unique dates in consolidated data: {combined_consolidated['Reference_Date'].nunique()}")
            
        else:
            combined_consolidated = pd.DataFrame()
            
        # Process individual data
        if individual_data:
            combined_individual = pd.concat(individual_data, ignore_index=True)
            # Convert date columns
            combined_individual['Reference_Date'] = pd.to_datetime(combined_individual['Reference_Date'])
            combined_individual['Delivery_Date'] = pd.to_datetime(combined_individual['Delivery_Date'])
            
            # Convert Version to numeric, replacing non-numeric versions with NaN
            combined_individual['Version'] = pd.to_numeric(combined_individual['Version'], errors='coerce')
            
            # Group by key fields and get the latest version
            key_fields = ['Reference_Date', 'Company_CNPJ', 'Company_Name', 'CVM_Code', 'Category', 'Type']
            combined_individual = (combined_individual
                .sort_values(['Reference_Date', 'Version'], ascending=[True, False])
                .groupby(key_fields, as_index=False)
                .first()
                .sort_values('Reference_Date')
                .reset_index(drop=True))
            
            # Log version information
            logger.info(f"Individual data version range: {combined_individual['Version'].min()} to {combined_individual['Version'].max()}")
            logger.info(f"Number of unique dates in individual data: {combined_individual['Reference_Date'].nunique()}")
            
        else:
            combined_individual = pd.DataFrame()
            
        return combined_consolidated, combined_individual
    except Exception as e:
        logger.error(f"Error processing trading data: {str(e)}")
        raise

def get_available_files(base_url):
    """Get list of available zip files from the CVM website."""
    try:
        session = create_session()
        response = session.get(base_url, verify=False)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        zip_files = [link.get('href') for link in soup.find_all('a') if link.get('href', '').endswith('.zip')]
        
        return zip_files
    except Exception as e:
        logger.error(f"Error getting available files: {str(e)}")
        raise

def main():
    """Main function to extract and process Brazilian stock trading data."""
    try:
        # Create temporary directory
        temp_dir = Path(tempfile.mkdtemp())
        logger.info(f"Created temporary directory: {temp_dir}")
        
        # Base URL for the data
        base_url = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/VLMO/DADOS/'
        
        # Get available files
        zip_files = get_available_files(base_url)
        logger.info(f"Found {len(zip_files)} zip files")
        
        all_csv_files = []
        for zip_file in zip_files:
            # Download and extract each zip file
            url = base_url + zip_file
            logger.info(f"Processing {url}")
            
            try:
                csv_files = download_and_extract_zip(url, temp_dir)
                all_csv_files.extend(csv_files)
            except Exception as e:
                logger.error(f"Error processing {zip_file}: {str(e)}")
                continue
        
        if not all_csv_files:
            raise Exception("No CSV files were successfully downloaded and extracted")
        
        # Process data
        consolidated_data, individual_data = process_trading_data(all_csv_files)
        logger.info("Processed trading data")
        
        # Create datasets directory if it doesn't exist
        datasets_dir = utils.ensure_datasets_dir()
        
        # Save consolidated data
        if not consolidated_data.empty:
            output_path = datasets_dir / 'Brazil_Stock_Trading_Consolidated.csv'
            consolidated_data.to_csv(output_path, index=False, encoding='utf-8-sig')
            logger.info(f"Saved Consolidated data to: {output_path}")
            logger.info(f"Consolidated data shape: {consolidated_data.shape}")
            logger.info(f"Consolidated columns: {consolidated_data.columns.tolist()}")
            
        # Save individual data
        if not individual_data.empty:
            output_path = datasets_dir / 'Brazil_Stock_Trading_Individual.csv'
            individual_data.to_csv(output_path, index=False, encoding='utf-8-sig')
            logger.info(f"Saved Individual data to: {output_path}")
            logger.info(f"Individual data shape: {individual_data.shape}")
            logger.info(f"Individual columns: {individual_data.columns.tolist()}")
        
        # Clean up
        for file in temp_dir.glob('*'):
            file.unlink()
        temp_dir.rmdir()
        logger.info("Cleaned up temporary files")
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        raise

if __name__ == "__main__":
    main() 