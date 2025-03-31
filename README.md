# CVM358 - Brazilian Stock Trading Data Extractor

This project extracts and processes Brazilian stock trading data from the CVM (Comissão de Valores Mobiliários) website, specifically focusing on the VLMO (Valores Mobiliários) dataset.

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
- `datasets/Brazil_Stock_Trading_Consolidated.csv`: Latest consolidated trading data
- `datasets/Brazil_Stock_Trading_Individual.csv`: Latest individual trading data
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
   - Consolidated trading data
   - Individual trading data
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

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📜 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- CVM for providing the data
- Contributors and maintainers 