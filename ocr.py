import os
import fitz  # PyMuPDF
import pytesseract
from PyPDF2 import PdfMerger
from tqdm import tqdm

# Paths
pdf_path = "spain+almaut.pdf"       # Input PDF
output_folder = "pages1"    # Temp folder for images
os.makedirs(output_folder, exist_ok=True)

# Convert PDF to images using PyMuPDF (no Poppler needed!)
print("Converting PDF pages to images...")
pdf_document = fitz.open(pdf_path)
image_files = []

for page_num in tqdm(range(len(pdf_document)), desc="Extracting pages", unit="page"):
    page = pdf_document[page_num]
    # Render page to image at 300 DPI (good for OCR)
    mat = fitz.Matrix(300/72, 300/72)  # 300 DPI scaling
    pix = page.get_pixmap(matrix=mat)
    img_path = os.path.join(output_folder, f"page_{page_num+1}.png")
    pix.save(img_path)
    image_files.append(img_path)

pdf_document.close()

# OCR each page to PDF
from PIL import Image
print("\nPerforming OCR on pages...")
ocr_pdfs = []
for i, img_path in enumerate(tqdm(image_files, desc="OCR processing", unit="page")):
    pdf_file = os.path.join(output_folder, f"ocr_page_{i+1}.pdf")
    # Use image_to_pdf_or_hocr to create searchable PDF
    pdf_bytes = pytesseract.image_to_pdf_or_hocr(img_path, lang="urd", extension="pdf")
    with open(pdf_file, "wb") as f:
        f.write(pdf_bytes)
    ocr_pdfs.append(pdf_file)

# Merge all PDF pages into one final PDF
print("\nMerging PDF pages...")
merger = PdfMerger()
for pdf in tqdm(ocr_pdfs, desc="Merging PDFs", unit="page"):
    merger.append(pdf)

final_pdf = "final_output2.pdf"
merger.write(final_pdf)
merger.close()

print(f"\n✓ Done! Searchable Urdu PDF saved as {final_pdf}")
