import json
from datetime import datetime
from pathlib import Path
import pandas as pd
from colorama import init, Fore, Back, Style
import shutil
import os
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

# Initialize colorama
init()

class ReportGenerator:
    def __init__(self):
        """Initialize the ReportGenerator with paths for reports and backups."""
        self.reports_dir = Path('reports')
        self.backup_dir = self.reports_dir / 'history'
        self.latest_report_path = self.reports_dir / 'latest_report.html'
        self.history_file = self.reports_dir / 'run_history.json'
        
        # Create necessary directories
        self.reports_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Initialize run history if it doesn't exist
        if not self.history_file.exists():
            self._save_run_history({})
    
    def _save_run_history(self, history):
        """Save run history to JSON file."""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def _load_run_history(self):
        """Load run history from JSON file."""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _generate_transaction_stats(self, consolidated_data):
        """Generate transaction statistics and visualizations."""
        # Transaction type distribution
        transaction_types = consolidated_data['Movement_Type'].value_counts()
        
        # Create pie chart for transaction types
        plt.figure(figsize=(10, 6))
        plt.pie(transaction_types, labels=transaction_types.index, autopct='%1.1f%%')
        plt.title('Distribution of Transaction Types')
        plt.axis('equal')
        
        # Save plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        transaction_types_chart = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        plt.close()
        
        # Monthly transaction volume
        monthly_volume = consolidated_data.groupby(consolidated_data['Reference_Date'].dt.to_period('M'))['Volume'].sum()
        
        # Create line chart for monthly volume
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_volume.index.astype(str), monthly_volume.values, marker='o')
        plt.title('Monthly Transaction Volume')
        plt.xlabel('Month')
        plt.ylabel('Volume')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        monthly_volume_chart = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        plt.close()
        
        # Top 10 companies by transaction volume
        top_companies = consolidated_data.groupby('Company_Name')['Volume'].sum().sort_values(ascending=False).head(10)
        
        # Create bar chart for top companies
        plt.figure(figsize=(12, 6))
        plt.barh(top_companies.index, top_companies.values)
        plt.title('Top 10 Companies by Transaction Volume')
        plt.xlabel('Volume')
        plt.tight_layout()
        
        # Save plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        top_companies_chart = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        plt.close()
        
        # Calculate statistics
        total_volume = consolidated_data['Volume'].sum()
        avg_volume = consolidated_data['Volume'].mean()
        max_volume = consolidated_data['Volume'].max()
        min_volume = consolidated_data['Volume'].min()
        
        # Transaction type counts
        transaction_type_counts = transaction_types.to_dict()
        
        return {
            'transaction_types_chart': transaction_types_chart,
            'monthly_volume_chart': monthly_volume_chart,
            'top_companies_chart': top_companies_chart,
            'total_volume': total_volume,
            'avg_volume': avg_volume,
            'max_volume': max_volume,
            'min_volume': min_volume,
            'transaction_type_counts': transaction_type_counts
        }
    
    def _generate_html_report(self, report_data):
        """Generate an HTML report with modern styling."""
        # Create companies list HTML
        companies_html = ""
        for company in report_data['last_month_companies']:
            companies_html += f"""
                <div class="company-item">
                    <span class="company-name">{company['Company_Name']}</span>
                    <span class="company-cnpj">CNPJ: {company['Company_CNPJ']}</span>
                </div>
            """
        
        # Create transaction statistics HTML
        stats = report_data['transaction_stats']
        transaction_types_html = ""
        for ttype, count in stats['transaction_type_counts'].items():
            transaction_types_html += f"""
                <div class="metric">
                    <span class="metric-label">{ttype}</span>
                    <span class="metric-value">{count:,}</span>
                </div>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CVM358 Data Extraction Report</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #eee;
                }}
                .header h1 {{
                    color: #2c3e50;
                    margin: 0;
                    font-size: 2.5em;
                }}
                .section {{
                    margin-bottom: 30px;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                }}
                .section h2 {{
                    color: #2c3e50;
                    margin-top: 0;
                    font-size: 1.5em;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                .metric {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }}
                .metric:last-child {{
                    border-bottom: none;
                }}
                .metric-label {{
                    color: #666;
                    font-size: 1.1em;
                }}
                .metric-value {{
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .highlight {{
                    color: #3498db;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 2px solid #eee;
                    color: #666;
                }}
                .companies-list {{
                    max-height: 400px;
                    overflow-y: auto;
                    margin-top: 15px;
                }}
                .company-item {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 10px;
                    border-bottom: 1px solid #eee;
                    background-color: white;
                }}
                .company-item:last-child {{
                    border-bottom: none;
                }}
                .company-name {{
                    font-weight: 500;
                    color: #2c3e50;
                }}
                .company-cnpj {{
                    color: #666;
                    font-size: 0.9em;
                }}
                .chart-container {{
                    margin: 20px 0;
                    text-align: center;
                }}
                .chart-container img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }}
                .stat-card {{
                    background-color: white;
                    padding: 15px;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                    text-align: center;
                }}
                .stat-value {{
                    font-size: 1.5em;
                    font-weight: bold;
                    color: #3498db;
                    margin: 10px 0;
                }}
                .stat-label {{
                    color: #666;
                    font-size: 0.9em;
                }}
                @media (max-width: 768px) {{
                    .container {{
                        padding: 15px;
                    }}
                    .section {{
                        padding: 15px;
                    }}
                    .company-item {{
                        flex-direction: column;
                        align-items: flex-start;
                        gap: 5px;
                    }}
                    .stats-grid {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 CVM358 Data Extraction Report</h1>
                </div>
                
                <div class="section">
                    <h2>🕒 Run Information</h2>
                    <div class="metric">
                        <span class="metric-label">Run Time</span>
                        <span class="metric-value">{report_data['run_time']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Latest Data Available</span>
                        <span class="metric-value">{report_data['latest_data']}</span>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📈 Total Records</h2>
                    <div class="metric">
                        <span class="metric-label">Consolidated</span>
                        <span class="metric-value highlight">{report_data['total_records']:,}</span>
                    </div>
                </div>
                
                <div class="section">
                    <h2>✨ New Records Since Last Run</h2>
                    <div class="metric">
                        <span class="metric-label">Consolidated</span>
                        <span class="metric-value highlight">{report_data['new_records']:,}</span>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🏢 Unique Companies</h2>
                    <div class="metric">
                        <span class="metric-label">Consolidated</span>
                        <span class="metric-value highlight">{report_data['unique_companies']:,}</span>
                    </div>
                </div>

                <div class="section">
                    <h2>📊 Transaction Statistics</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-label">Total Volume</div>
                            <div class="stat-value">{stats['total_volume']:,.2f}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Average Volume</div>
                            <div class="stat-value">{stats['avg_volume']:,.2f}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Maximum Volume</div>
                            <div class="stat-value">{stats['max_volume']:,.2f}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Minimum Volume</div>
                            <div class="stat-value">{stats['min_volume']:,.2f}</div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>📋 Companies Reported in {report_data['latest_data']}</h2>
                    <div class="companies-list">
                        {companies_html}
                    </div>
                </div>
                
                <div class="section">
                    <h2>📊 Transaction Type Distribution</h2>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{stats['transaction_types_chart']}" alt="Transaction Type Distribution">
                    </div>
                    <div class="transaction-types">
                        {transaction_types_html}
                    </div>
                </div>
                
                <div class="section">
                    <h2>📈 Monthly Transaction Volume</h2>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{stats['monthly_volume_chart']}" alt="Monthly Transaction Volume">
                    </div>
                </div>
                
                <div class="section">
                    <h2>🏢 Top 10 Companies by Volume</h2>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{stats['top_companies_chart']}" alt="Top 10 Companies by Volume">
                    </div>
                </div>
                
                <div class="footer">
                    <p>Report generated by CVM358 Data Extractor</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Save the latest report
        with open(self.latest_report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Create a backup of the report with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f'report_{timestamp}.html'
        shutil.copy2(self.latest_report_path, backup_path)
        
        # Keep only the last 10 backup reports
        backup_files = sorted(self.backup_dir.glob('report_*.html'))
        if len(backup_files) > 10:
            for old_file in backup_files[:-10]:
                old_file.unlink()
    
    def generate_report(self, consolidated_data, _):
        """Generate a report from the data."""
        # Get current time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get latest data date
        latest_date = consolidated_data['Reference_Date'].max()
        latest_date_str = latest_date.strftime('%Y-%m')
        
        # Get companies from last month
        last_month_companies = consolidated_data[consolidated_data['Reference_Date'] == latest_date]
        last_month_companies_list = last_month_companies[['Company_CNPJ', 'Company_Name']].drop_duplicates()
        last_month_companies_list = last_month_companies_list.sort_values('Company_Name')
        
        # Get total records
        total_records = len(consolidated_data)
        
        # Get unique companies
        unique_companies = consolidated_data['Company_CNPJ'].nunique()
        
        # Load run history
        history = self._load_run_history()
        
        # Get new records since last run
        last_run = history.get('last_run', {})
        last_run_records = last_run.get('total_records', 0)
        if isinstance(last_run_records, dict):
            last_run_records = last_run_records.get('consolidated', 0)
        new_records = total_records - last_run_records
        
        # Generate transaction statistics
        transaction_stats = self._generate_transaction_stats(consolidated_data)
        
        # Create report data
        report_data = {
            'run_time': current_time,
            'latest_data': latest_date_str,
            'total_records': total_records,
            'new_records': new_records,
            'unique_companies': unique_companies,
            'last_month_companies': last_month_companies_list.to_dict('records'),
            'transaction_stats': transaction_stats
        }
        
        # Update run history
        history['last_run'] = {
            'timestamp': current_time,
            'total_records': total_records,
            'unique_companies': unique_companies
        }
        self._save_run_history(history)
        
        # Generate HTML report
        self._generate_html_report(report_data)
        
        return report_data
    
    def print_report(self, report_data):
        """Print the report to console."""
        print("\n" + "="*50)
        print("📊 CVM358 Data Extraction Report")
        print("="*50 + "\n")
        
        print(f"🕒 Run Time: {report_data['run_time']}")
        print(f"📅 Latest Data Available: {report_data['latest_data']}\n")
        
        print("📈 Total Records:")
        print(f"  • Consolidated: {report_data['total_records']:,}\n")
        
        print("✨ New Records Since Last Run:")
        print(f"  • Consolidated: {report_data['new_records']:,}\n")
        
        print("🏢 Unique Companies:")
        print(f"  • Consolidated: {report_data['unique_companies']:,}\n")
        
        print("📊 Transaction Statistics:")
        stats = report_data['transaction_stats']
        print(f"  • Total Volume: {stats['total_volume']:,.2f}")
        print(f"  • Average Volume: {stats['avg_volume']:,.2f}")
        print(f"  • Maximum Volume: {stats['max_volume']:,.2f}")
        print(f"  • Minimum Volume: {stats['min_volume']:,.2f}\n")
        
        print("📋 Transaction Types:")
        for ttype, count in stats['transaction_type_counts'].items():
            print(f"  • {ttype}: {count:,}")
        
        print("\n" + "="*50)
        print("Report generated by CVM358 Data Extractor")
        print("="*50 + "\n") 