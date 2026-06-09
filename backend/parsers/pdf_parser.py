"""
pdf_parser.py - Extract raw text from PDF resumes using PyMuPDF + pdfplumber fallback
"""
import fitz          # PyMuPDF
import pdfplumber


def extract_text_from_pdf(filepath: str) -> str:
    """
    Primary: PyMuPDF (fast, handles most PDFs).
    Fallback: pdfplumber (better for table-heavy / complex-layout PDFs).
    """
    text = _extract_with_pymupdf(filepath)
    if len(text.strip()) < 100:
        text = _extract_with_pdfplumber(filepath)
    return text.strip()


def _extract_with_pymupdf(filepath: str) -> str:
    text_parts = []
    try:
        doc = fitz.open(filepath)
        for page in doc:
            text_parts.append(page.get_text("text"))
        doc.close()
    except Exception as e:
        print(f"[PyMuPDF] Error: {e}")
    return "\n".join(text_parts)


def _extract_with_pdfplumber(filepath: str) -> str:
    text_parts = []
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception as e:
        print(f"[pdfplumber] Error: {e}")
    return "\n".join(text_parts)
