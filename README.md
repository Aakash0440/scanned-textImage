📄 Universal PDF OCR Tool (Multi-Language, Searchable PDF)

This project converts scanned PDFs into fully searchable PDFs using Tesseract OCR.
It supports any language supported by Tesseract (Urdu, English, Arabic, Hindi, Persian, etc.) and works without Poppler, making it especially easy to use on Windows.

✨ Features

🌍 Multi-language OCR support (any Tesseract language)

🖼️ High-quality OCR using 300 DPI rendering

🔍 Generates searchable PDFs

📑 Merges all pages into a single output file

🚀 No Poppler dependency

📊 Progress bars for long documents

🧩 Clean, modular, reusable code

🛠️ Technologies Used

Python 3

PyMuPDF (fitz) – Convert PDF pages to images

Tesseract OCR – Text recognition

PyPDF2 – Merge PDFs

Pillow (PIL) – Image handling

tqdm – Progress indicators

📋 Prerequisites (IMPORTANT)
1️⃣ Install Python

Make sure Python 3.8+ is installed.

Check:

python --version

2️⃣ Install Tesseract OCR (Required)
🔹 Windows

Download Tesseract from:

https://github.com/UB-Mannheim/tesseract/wiki

Install it

Add Tesseract to system PATH

Default path example:

C:\Program Files\Tesseract-OCR\


Verify:

tesseract --version

3️⃣ Install Language Data for Tesseract

Install the language(s) you want to OCR.

Examples:

eng → English

urd → Urdu

ara → Arabic

hin → Hindi

fas → Persian

Check installed languages:

tesseract --list-langs


If a language is missing, download its .traineddata file and place it in:

tessdata/

📦 Python Dependencies

Install required Python packages:

pip install pymupdf pytesseract PyPDF2 pillow tqdm

📂 Project Structure
.
├── input.pdf            # Your scanned PDF
├── ocr_pages/           # Temporary images & OCR pages
│   ├── page_1.png
│   ├── ocr_page_1.pdf
│   └── ...
├── final_output.pdf     # Final searchable PDF
├── ocr_pipeline.py      # Main script
└── README.md

⚙️ Configuration

Edit these variables in ocr_pipeline.py:

INPUT_PDF = "input.pdf"
FINAL_PDF = "final_output.pdf"
LANG = "eng"       # Change language here
DPI = 300          # OCR quality

🌍 Language Examples
LANG = "eng"   # English
LANG = "urd"   # Urdu
LANG = "ara"   # Arabic
LANG = "hin"   # Hindi
LANG = "fas"   # Persian
LANG = "spa"   # Spanish

▶️ How to Run

Place your scanned PDF in the project folder

Rename it to match INPUT_PDF

Run the script:

python ocr_pipeline.py


Output will be saved as:

final_output.pdf


✅ The output PDF will be fully searchable.

🧠 How It Works

PDF → Images

Each page is rendered at 300 DPI using PyMuPDF

Images → Searchable PDF

Tesseract OCR extracts text in the selected language

Merge Pages

All OCR pages are combined into one PDF

📌 Tips for Best Results

Use 300 DPI or higher for scanned books

Ensure the PDF is not already searchable

Clean scans = better OCR accuracy

Large PDFs may take time ⏳

🚀 Future Improvements

CLI arguments (argparse)

Batch OCR for multiple PDFs

Automatic language detection

Temporary file cleanup

GUI version (Tkinter / PyQt)

Parallel OCR for speed

👤 Author

Aakash Ali
Python OCR Utility
Focus: PDFs, OCR, multilingual text processing
