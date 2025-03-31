# CVM358 - Brazilian Stock Trading Data Extractor

This project provides a Python-based extractor for Brazilian stock trading data from CVM (Comissão de Valores Mobiliários).

## Features

- Downloads and processes stock trading data from CVM's website
- Handles both consolidated and individual trading data
- Robust error handling and retry mechanisms
- Efficient data processing with pandas
- Automatic data deduplication and versioning

## Requirements

- Python 3.7+
- pandas
- requests
- beautifulsoup4
- urllib3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pedronipalhares/CVM358.git
cd CVM358
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the extractor:
```bash
python extractor/br_stock_trading.py
```

The script will:
1. Download the latest trading data from CVM
2. Process both consolidated and individual trading data
3. Save the results in CSV format in the `datasets` directory at the root of the project

## Project Structure

```
CVM358/
├── README.md
├── requirements.txt
├── datasets/           # Output directory for CSV files
└── extractor/
    ├── br_stock_trading.py
    └── utils.py
```

## Output Files

The extractor generates two main CSV files in the `datasets` directory:
- `Brazil_Stock_Trading_Consolidated.csv`: Contains consolidated trading data
- `Brazil_Stock_Trading_Individual.csv`: Contains individual trading data

## License

MIT License 