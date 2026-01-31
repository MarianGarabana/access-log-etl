# Access Log ETL

Parameterized Python script that performs an ETL process on web server access logs
using **regex**, **argparse**, and **pandas**.

The script extracts structured fields from raw log files, filters by HTTP status code,
and writes the results to a CSV file.

---

## Features
- Command-line interface with `argparse`
- Robust regex-based parsing
- Graceful handling of malformed lines
- Optional verbosity for debugging
- CSV output via pandas

---

## Usage

```bash
python access_log_processor.py access_logs.txt results.csv --status 200 --verbose
