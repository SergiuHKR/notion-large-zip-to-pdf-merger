# PDF Merger Tool

This tool processes large ZIP files containing PDF documents and merges them into smaller, manageable PDF files. It's particularly useful when dealing with large collections of PDFs that need to be organized into smaller chunks.

## Features

- Processes large ZIP files containing PDFs
- Merges PDFs into chunks of maximum 19MB each
- Handles memory efficiently using streaming
- Automatically cleans up temporary files
- Provides detailed logging of the process

## Prerequisites

- macOS (tested on MacBook Pro with Apple Silicon)
- Python 3.9 or later

## Installation

1. **Install Python**
   ```bash
   # Install Homebrew if you don't have it
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python using Homebrew
   brew install python@3.9
   ```

2. **Verify Python Installation**
   ```bash
   python3 --version
   ```

3. **Install Required Dependencies**
   ```bash
   # Navigate to the project directory
   cd pdf-merger
   
   # Install required packages
   pip3 install -r requirements.txt
   ```

## Project Structure

```
pdf-merger/
├── input/              # Place your ZIP files here
├── output/             # Merged PDFs will be saved here
├── process_large_zip.py # Main script
└── requirements.txt    # Python dependencies
```

## Usage

1. **Prepare Your Files**
   - Place your ZIP file containing PDFs in the `input` directory
   - The ZIP file should contain PDF files that you want to merge

2. **Run the Script**
   ```bash
   python3 process_large_zip.py
   ```

3. **Check Results**
   - Merged PDFs will be created in the `output` directory
   - Files will be named as `merged_1.pdf`, `merged_2.pdf`, etc.
   - Each merged PDF will be under 19MB in size

## How It Works

The script performs the following operations:

1. **Extraction**
   - Extracts PDF files from the ZIP archive one at a time
   - Uses temporary storage to minimize memory usage

2. **Processing**
   - Processes each PDF file individually
   - Keeps track of the total size of the current merge
   - Creates new merged PDFs when the size limit (19MB) is reached

3. **Output**
   - Creates merged PDFs in the output directory
   - Names files sequentially (merged_1.pdf, merged_2.pdf, etc.)
   - Ensures each output file is under 19MB

4. **Cleanup**
   - Automatically removes temporary files
   - Maintains a clean working environment

## Logging

The script provides detailed logging information:
- Number of PDF files found
- Progress of merging operations
- Warnings for files that exceed size limits
- Confirmation of saved files

## Notes

- Individual PDFs larger than 19MB will be skipped with a warning
- The script uses streaming to handle large files efficiently
- Temporary files are automatically cleaned up after processing

## Troubleshooting

If you encounter any issues:

1. **Python not found**
   - Make sure Python is installed correctly
   - Try using `python3` instead of `python`

2. **Missing dependencies**
   - Run `pip3 install -r requirements.txt` again
   - Check if you're in the correct directory

3. **Permission issues**
   - Make sure you have write permissions in the output directory
   - Try running with `sudo` if necessary

## Support

For any issues or questions, please open an issue in the repository. 