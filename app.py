from flask import Flask, request, send_file
import os
import fitz  # PyMuPDF
import pandas as pd
import PyPDF2
from pdf2docx import Converter

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# PDF to Excel Conversion
@app.route("/pdf-to-excel", methods=["POST"])
def pdf_to_excel():
    file = request.files["file"]
    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    excel_path = os.path.join(RESULT_FOLDER, file.filename.replace(".pdf", ".xlsx"))
    file.save(pdf_path)

    doc = fitz.open(pdf_path)
    data = []

    for page in doc:
        text = page.get_text("text")
        lines = text.split("\n")
        data.append(lines)

    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False, header=False)

    return send_file(excel_path, as_attachment=True)

# PDF to Word Conversion
@app.route("/pdf-to-word", methods=["POST"])
def pdf_to_word():
    file = request.files["file"]
    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    word_path = os.path.join(RESULT_FOLDER, file.filename.replace(".pdf", ".docx"))
    file.save(pdf_path)

    cv = Converter(pdf_path)
    cv.convert(word_path, start=0, end=None)
    cv.close()

    return send_file(word_path, as_attachment=True)

# Merge PDFs
@app.route("/merge-pdf", methods=["POST"])
def merge_pdf():
    files = request.files.getlist("files")
    merger = PyPDF2.PdfMerger()

    for file in files:
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)
        merger.append(pdf_path)

    merged_pdf_path = os.path.join(RESULT_FOLDER, "merged.pdf")
    merger.write(merged_pdf_path)

    return send_file(merged_pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
