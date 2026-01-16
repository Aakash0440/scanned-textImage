import sys
import os
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QProgressBar, QTextEdit, QComboBox, QMessageBox
)
from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtCore import Qt
import fitz  # PyMuPDF
import pytesseract
from PyPDF2 import PdfMerger

DPI = 300

# ================= OCR FUNCTIONS ==================

def pdf_to_images(pdf_path, output_dir, dpi=300, progress_callback=None):
    os.makedirs(output_dir, exist_ok=True)
    pdf = fitz.open(pdf_path)
    image_paths = []
    scale = dpi / 72
    matrix = fitz.Matrix(scale, scale)

    for page_num in range(len(pdf)):
        page = pdf[page_num]
        pix = page.get_pixmap(matrix=matrix)
        img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(img_path)
        image_paths.append(img_path)
        if progress_callback:
            progress_callback(page_num + 1, len(pdf), f"Converted page {page_num + 1}/{len(pdf)}")
    pdf.close()
    return image_paths

def images_to_searchable_pdfs(image_paths, output_dir, lang, progress_callback=None):
    ocr_pdfs = []
    for i, img_path in enumerate(image_paths):
        pdf_path = os.path.join(output_dir, f"ocr_page_{i + 1}.pdf")
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(img_path, lang=lang, extension="pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)
        ocr_pdfs.append(pdf_path)
        if progress_callback:
            progress_callback(i + 1, len(image_paths), f"OCR done for page {i + 1}/{len(image_paths)}")
    return ocr_pdfs

def merge_pdfs(pdf_list, output_pdf, progress_callback=None):
    merger = PdfMerger()
    for i, pdf in enumerate(pdf_list):
        merger.append(pdf)
        if progress_callback:
            progress_callback(i + 1, len(pdf_list), f"Merging page {i + 1}/{len(pdf_list)}")
    merger.write(output_pdf)
    merger.close()

# ================= GUI ==================

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌌 Futuristic OCR Pipeline")
        self.setGeometry(300, 100, 700, 500)
        self.setStyleSheet("background-color: #1e1e2f; color: #00ffff;")

        layout = QVBoxLayout()

        font = QFont("Consolas", 10)

        # Input PDF
        self.pdf_label = QLabel("📄 Select Input PDF")
        self.pdf_label.setFont(font)
        layout.addWidget(self.pdf_label)

        self.pdf_button = QPushButton("Browse PDF")
        self.pdf_button.setFont(font)
        self.pdf_button.setStyleSheet("background-color: #2e2e3f; color: #00ffff;")
        self.pdf_button.clicked.connect(self.select_pdf)
        layout.addWidget(self.pdf_button)

        # Output Folder
        self.out_label = QLabel("📂 Select Output Folder")
        self.out_label.setFont(font)
        layout.addWidget(self.out_label)

        self.out_button = QPushButton("Browse Folder")
        self.out_button.setFont(font)
        self.out_button.setStyleSheet("background-color: #2e2e3f; color: #00ffff;")
        self.out_button.clicked.connect(self.select_output)
        layout.addWidget(self.out_button)

        # Language Dropdown
        self.lang_label = QLabel("🌐 Select OCR Language")
        self.lang_label.setFont(font)
        layout.addWidget(self.lang_label)

        self.lang_dropdown = QComboBox()
        self.lang_dropdown.setFont(font)
        self.lang_dropdown.addItems(["eng", "urd", "ara"])
        layout.addWidget(self.lang_dropdown)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00ffff;
                border-radius: 5px;
                text-align: center;
                color: #00ffff;
            }
            QProgressBar::chunk {
                background-color: #00ffff;
            }
        """)
        layout.addWidget(self.progress)

        # Status Log
        self.status = QTextEdit()
        self.status.setFont(QFont("Courier", 9))
        self.status.setReadOnly(True)
        self.status.setStyleSheet("background-color: #2e2e3f; color: #00ffff;")
        layout.addWidget(self.status)

        # Start Button
        self.start_button = QPushButton("Start OCR 🛰️")
        self.start_button.setFont(font)
        self.start_button.setStyleSheet("background-color: #2e2e3f; color: #00ffff;")
        self.start_button.clicked.connect(self.start_ocr)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        # Paths
        self.pdf_path = ""
        self.output_dir = ""

    def select_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if path:
            self.pdf_path = path
            self.status.append(f"📄 Selected PDF: {path}")

    def select_output(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.output_dir = path
            self.status.append(f"📂 Selected Output Folder: {path}")

    def update_progress(self, current, total, message):
        percent = int((current / total) * 100)
        self.progress.setValue(percent)
        self.status.append(message)
        QApplication.processEvents()

    def start_ocr(self):
        if not self.pdf_path or not self.output_dir:
            QMessageBox.warning(self, "⚠️ Missing Info", "Please select both input PDF and output folder.")
            return

        lang = self.lang_dropdown.currentText()
        final_pdf = os.path.join(self.output_dir, "final_output.pdf")

        def run_pipeline():
            try:
                self.status.append(f"\n🔹 Starting OCR Pipeline with language '{lang}'\n")
                images = pdf_to_images(self.pdf_path, self.output_dir, DPI, self.update_progress)
                ocr_pdfs = images_to_searchable_pdfs(images, self.output_dir, lang, self.update_progress)
                merge_pdfs(ocr_pdfs, final_pdf, self.update_progress)
                self.status.append(f"\n✅ Done! Saved: {final_pdf}")
                QMessageBox.information(self, "🎉 Success", f"OCR finished! File saved at:\n{final_pdf}")
            except Exception as e:
                QMessageBox.critical(self, "❌ Error", str(e))

        threading.Thread(target=run_pipeline).start()

# ================= MAIN ==================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec())
