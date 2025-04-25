# Largest Number in PDF

This repository contains a simple Python script for extracting the largest numeric value from a PDF document.

## Prerequisites

- **Python 3.7+** installed on your system. Check your version:
  ```bash
  python3 --version
  ```
- **pip** (the Python package installer) should be available.

## Installation

1. **Clone the repository**

   Replace `<your-username>` with your GitHub username:
   ```bash
   git clone https://github.com/<your-username>/largest-number-in-pdf.git
   cd largest-number-in-pdf
   ```

2. **Install dependencies**
   ```bash
   python3 -m pip install --upgrade pip
   python3 -m pip install -r requirements.txt
   ```

   The `requirements.txt` includes:
   ```text
   pymupdf
   ```

## Usage

1. **Download the PDF** you want to analyze and place it in the root of the cloned repository.

2. **Run the script**:
   ```bash
   python3 extract_largest_number.py <path/to/your.pdf>
   ```

   For example, if your file is named `conductorAI.pdf`:
   ```bash
   python3 extract_largest_number.py conductorAI.pdf
   ```

3. **Output**

   The script will print the largest literal number found in the document to the console.

## Notes

- The script uses [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) to extract text from the PDF.
- Ensure the PDF file is not password-protected.

---

Thank you for your time and consideration! 

