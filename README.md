# CVM358 - Brazilian Insider Trading Data Extractor

## 📊 Overview

This project extracts and processes Brazilian insider trading data from the CVM (Comissão de Valores Mobiliários) website, specifically focusing on the CVM358 dataset. CVM358 refers to CVM Instruction 358/02, which regulates the disclosure of insider trading and related-party transactions in the Brazilian market.

## 🎯 Purpose

CVM358 is crucial for market transparency and corporate governance in Brazil. This tool helps stakeholders to:

- Monitor insider trading activities
- Track related-party transactions
- Ensure compliance with regulatory requirements
- Analyze trading patterns of company insiders
- Support corporate governance analysis
- Enable regulatory reporting and compliance

## 📈 Data Context

### What We're Tracking

The data includes detailed information about insider trading and related-party transactions:

1. **Insider Trading Data**
   - Transactions by company executives
   - Board members' trading activities
   - Fiscal council members' transactions
   - Technical/consultative body members' trades

2. **Related-Party Information**
   - Transactions by controlling shareholders
   - Trading by related individuals (spouses, partners)
   - Transactions by dependent family members
   - Trading by controlled companies

3. **Transaction Details**
   - Trading dates and volumes
   - Security types (stocks, derivatives)
   - Transaction values
   - Related company information

### Why It Matters

This data is essential for:

- **Regulators**: Monitor compliance with CVM358 requirements
- **Investors**: Assess corporate governance practices
- **Companies**: Ensure regulatory compliance
- **Analysts**: Study insider trading patterns
- **Researchers**: Analyze market transparency

## 🌟 Features

### Data Extraction
- Parallel downloads of ZIP files using ThreadPoolExecutor
- Automatic handling of multiple file versions
- Support for both consolidated and individual trading data
- Robust error handling and retry mechanisms
- SSL/TLS compatibility for secure downloads

### Data Processing
- Automatic date format conversion
- Version control for data entries
- Deduplication of records
- Standardized column naming
- Support for Brazilian Portuguese character encoding

### Data Storage
- Organized dataset directory structure
- Automatic backup system with timestamps
- Historical data preservation (last 5 versions)
- Clean separation of current and historical data

### Reporting System
- Modern HTML reports with responsive design
- Real-time console logging with color coding
- Detailed execution metrics and timing information
- Historical report tracking
- Performance statistics

## 📊 Generated Files

### Datasets
- `datasets/Brazil_Stock_Trading_Consolidated.csv`: Latest consolidated insider trading data
- `datasets/Brazil_Stock_Trading_Individual.csv`: Latest individual insider trading data
- `datasets/history/`: Historical backups with timestamps

### Reports
- `reports/latest_report.html`: Current execution report
- `reports/history/`: Historical reports with timestamps
- `reports/run_history.json`: Execution history and statistics

## 🚀 Performance

- Parallel downloads: 4 concurrent downloads
- Typical execution times:
  - Download: ~1-2 seconds
  - Processing: ~0.7 seconds
  - Total execution: ~2-3 seconds

## 📋 Requirements

```bash
pip install -r requirements.txt
```

## 🛠️ Usage

```bash
python br_stock_trading.py
```

## 📈 Output

The script generates:

1. **Processed Datasets**
   - Consolidated insider trading data
   - Individual insider trading data
   - Automatic backups with timestamps

2. **HTML Reports**
   - Run information
   - Latest data available
   - Total records processed
   - New records since last run
   - Unique companies count

3. **Console Output**
   - Progress indicators
   - Performance metrics
   - Error messages (if any)
   - Success confirmation

## 🔄 Backup System

- Maintains the last 5 versions of each dataset
- Timestamps in format: YYYYMMDD_HHMMSS
- Automatic cleanup of older versions
- Easy rollback capability

## 📊 Report Features

- Modern, responsive design
- Clear metrics visualization
- Color-coded sections
- Mobile-friendly layout
- Historical tracking

## 🛡️ Error Handling

- Robust download retry mechanism
- Graceful failure recovery
- Detailed error logging
- Data integrity checks

## 🔒 Security

- HTTPS support
- SSL/TLS compatibility
- Secure file handling
- Clean temporary files

## 📝 Logging

- Color-coded console output
- Detailed progress tracking
- Performance metrics
- Error reporting

## 🗂️ Project Structure

```
.
├── br_stock_trading.py    # Main script
├── requirements.txt       # Dependencies
├── datasets/             # Data storage
│   ├── *.csv            # Current datasets
│   └── history/         # Historical backups
├── reports/             # Report storage
│   ├── latest_report.html   # Current report
│   ├── history/            # Historical reports
│   └── report_generator.py # Report generation logic
└── README.md            # Documentation
```

## 📚 Use Cases

### Compliance Monitoring
- Track insider trading compliance
- Monitor related-party transactions
- Ensure regulatory reporting
- Audit trail maintenance

### Corporate Governance
- Analyze insider trading patterns
- Assess board member activities
- Monitor controlling shareholders
- Evaluate transparency practices

### Market Analysis
- Study insider trading trends
- Analyze related-party transactions
- Assess market transparency
- Monitor regulatory compliance

### Research
- Academic studies on insider trading
- Corporate governance research
- Market transparency analysis
- Regulatory impact studies

## 🤝 Contributing

Feel free to submit issues and enhancement requests! We welcome contributions that help make this tool more valuable for monitoring CVM358 compliance and market transparency.

## 📜 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- CVM for providing the CVM358 data
- B3 (Brazilian Stock Exchange) for market infrastructure
- Contributors and maintainers
- Brazilian financial market community

## 📬 Contact

For questions, suggestions, or collaboration opportunities, please open an issue or submit a pull request. 