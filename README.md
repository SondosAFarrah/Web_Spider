# Web Server Technology Scanner and Spidering Tool

## Overview
This Python script is designed to analyze web server technologies, crawl websites, and compare discovered URLs against a predefined list of default files. It helps in identifying publicly accessible default files, which may pose security risks.

## Features
- Detects web server technology by analyzing HTTP response headers.
- Crawls websites recursively to discover internal links.
- Compares found URLs against a predefined list of default files.
- Generates a hashed cross-matrix comparison of URLs.
- Saves results to a text file for further analysis.

## Requirements
Ensure you have the following dependencies installed:
```bash
pip install requests beautifulsoup4 pandas
```

## How It Works
1. **Detect Web Server Technology**: The script sends a request to the target URL and extracts the `Server` header.
2. **Load Default File List**: Based on the detected server, it loads a predefined list of default files.
3. **Crawl the Website**: Extracts internal links up to a given depth.
4. **Compare URLs**: Matches discovered URLs against the default file list.
5. **Generate Cross Matrix**: Creates a hash-based comparison matrix.
6. **Save Results**: Outputs findings to `spidering_results.txt`.

## Usage
Run the script and enter the target URL when prompted:
```bash
python script.py
```
Example input:
```
Enter target URL (e.g., http://example.com):
```

## Output
Results are saved in `spidering_results.txt` containing:
- Default URLs Found
- Non-Default URLs Found
- Cross Matrix Comparison

## Disclaimer
This tool is intended for ethical use only. Always obtain proper authorization before scanning a website.



