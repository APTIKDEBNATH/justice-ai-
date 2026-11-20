"""
Document Ingestion & Clause Segmentation Engine
Supports PDF, DOCX, and TXT legal agreements with intelligent clause splitting.
"""

import io
import re
from typing import Dict, Any, List, Optional
import pypdf
import docx


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts raw text from PDF file bytes."""
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        extracted_pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_pages.append(f"--- [Page {i+1}] ---\n{text}")
        return "\n\n".join(extracted_pages)
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extracts raw text from DOCX file bytes."""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    except Exception as e:
        return f"Error parsing DOCX: {str(e)}"


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Routes file parsing based on extension."""
    lower_name = filename.lower()
    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif lower_name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        # Fallback to UTF-8 text decode
        try:
            return file_bytes.decode("utf-8", errors="replace")
        except Exception:
            return str(file_bytes)


def segment_clauses(text: str) -> List[Dict[str, str]]:
    """
    Splits legal contract text into structured clauses/sections based on common
    numbering patterns (e.g. '1. Definitions', 'Section 4. Indemnification', 'Article V').
    """
    if not text:
        return []

    # Regex pattern for section/article/clause headers
    pattern = r"(?m)^(?:(?:Section|Article|Clause|Item)\s+\d+(?:\.\d+)*[:\.\s\-]+[^\n]+|\d+\.\s+[A-Z][^\n]+)"
    matches = list(re.finditer(pattern, text))
    
    clauses = []
    if not matches:
        # Fallback: split by double newlines into logical paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
        for i, para in enumerate(paragraphs[:30]):
            title = para.split("\n")[0][:60]
            clauses.append({"title": f"Paragraph {i+1}: {title}...", "content": para})
        return clauses

    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        header = matches[i].group(0).strip()
        body = text[start:end].strip()
        
        # Clean title
        title_line = header.split("\n")[0].strip()
        clauses.append({
            "title": title_line[:80],
            "content": body
        })

    return clauses


def extract_document_metadata(text: str) -> Dict[str, Any]:
    """Extracts summary statistics and preliminary flags from the contract text."""
    words = re.findall(r"\b\w+\b", text)
    word_count = len(words)
    estimated_read_time_mins = max(1, round(word_count / 200))

    # Detect Governing Law mention
    gov_law_match = re.search(
        r"(?:governed\s+by|laws\s+of|jurisdiction\s+of)\s+([A-Za-z\s,]{4,40})",
        text,
        re.IGNORECASE
    )
    detected_gov_law = gov_law_match.group(1).strip() if gov_law_match else "Not explicitly specified"

    # Detect Dispute Resolution
    dispute_match = re.search(
        r"(arbitration|mediation|courts?\s+of\s+[A-Za-z\s,]+|exclusive\s+jurisdiction)",
        text,
        re.IGNORECASE
    )
    detected_dispute = dispute_match.group(0).strip() if dispute_match else "Standard court litigation"

    return {
        "word_count": word_count,
        "estimated_read_time_mins": estimated_read_time_mins,
        "detected_gov_law": detected_gov_law,
        "detected_dispute": detected_dispute
    }
