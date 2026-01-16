import os
import fitz  # PyMuPDF
import pytesseract
from PyPDF2 import PdfMerger
from tqdm import tqdm
from PIL import Image

# ===================== CONFIG =====================

INPUT_PDF = "input.pdf"          # Input scanned PDF
OUTPUT_DIR = "ocr_pages"         # Temporary output folder
FINAL_PDF = "final_output.pdf"   # Final searchable PDF
LANG = "eng"                     # Tesseract language code (e.g. eng, urd, ara)

DPI = 300                        # OCR quality (recommended: 300)

# ==================================================


def pdf_to_images(pdf_path, output_dir, dpi=300):
    """
    Convert PDF pages to high-resolution images
    """
    os.makedirs(output_dir, exist_ok=True)
    pdf = fitz.open(pdf_path)
    image_paths = []

    scale = dpi / 72
    matrix = fitz.Matrix(scale, scale)

    for page_num in tqdm(range(len(pdf)), desc="Converting PDF to images", unit="page"):
        page = pdf[page_num]
        pix = page.get_pixmap(matrix=matrix)
        img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(img_path)
        image_paths.append(img_path)

    pdf.close()
    return image_paths


def images_to_searchable_pdfs(image_paths, output_dir, lang):
    """
    Perform OCR on images and convert them to searchable PDFs
    """
    ocr_pdfs = []

    for i, img_path in enumerate(tqdm(image_paths, desc="Running OCR", unit="page")):
        pdf_path = os.path.join(output_dir, f"ocr_page_{i + 1}.pdf")

        pdf_bytes = pytesseract.image_to_pdf_or_hocr(
            img_path,
            lang=lang,
            extension="pdf"
        )

        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        ocr_pdfs.append(pdf_path)

    return ocr_pdfs


def merge_pdfs(pdf_list, output_pdf):
    """
    Merge multiple PDFs into one
    """
    merger = PdfMerger()

    for pdf in tqdm(pdf_list, desc="Merging PDFs", unit="page"):
        merger.append(pdf)

    merger.write(output_pdf)
    merger.close()


def main():
    print("\n📄 Starting OCR Pipeline")
    print(f"Language: {LANG}")
    print(f"Input PDF: {INPUT_PDF}\n")

    images = pdf_to_images(INPUT_PDF, OUTPUT_DIR, DPI)
    ocr_pdfs = images_to_searchable_pdfs(images, OUTPUT_DIR, LANG)
    merge_pdfs(ocr_pdfs, FINAL_PDF)

    print(f"\n✅ Done! Searchable PDF saved as: {FINAL_PDF}")


if __name__ == "__main__":
    main()
