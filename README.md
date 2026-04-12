# CSV to QIF Converter

This project provides utilities to convert various financial transaction formats (CSV, PDF) into QIF format for easy import into Quicken.

## Supported Formats

### WEX
WEX transactions (CSV)

### Capital Group
Capital Group transactions (CSV)

### Coinbase
Coinbase transactions (PDF)

## Installation and Usage

### Using Docker (Recommended)

The easiest way to use this tool is via Docker, which ensures all dependencies are correctly configured.

1. **Build the image:**
   ```bash
   ./build.sh
   ```

2. **Run a conversion:**
   Use the `run_conversion.sh` script provided in the repository.
   ```bash
   ./run_conversion.sh <conversion_type> <input_file_path>
   ```
   **Example (WEX):**
   ```bash
   ./run_conversion.sh wex input/sample.csv
   ```
   **Example (Coinbase):**
   ```bash
   ./run_conversion.sh cbcc input/statement.pdf
   ```

### Running Locally

If you prefer to run it locally, ensure you have Python installed.

1. **Install dependencies:**
   ```bash
   pip install pdfplumber
   ```

2. **Run the scripts:**
   The scripts are located in the `src/` directory.
   ```bash
   python src/convert-wex.py input/sample.csv
   ```

## Project Structure

- `src/`: Contains the Python source code.
- `build.sh`: Script to build the Docker image.
- `run_conversion.sh`: Script to run conversions using Docker.
- `Dockerfile`: Instructions for building the Docker image.
