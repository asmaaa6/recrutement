# Extracteur de texte depuis PDF

import PyPDF2
from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_path):
    """
    Extrait le texte d'un fichier PDF
    
    Args:
        file_path: Chemin du fichier PDF
    
    Returns:
        str: Texte extrait
    """
    
    try:
        # Essayer avec pdfminer d'abord (meilleur résultat)
        text = extract_text(file_path)
        if text.strip():
            return text
    except Exception as e:
        print(f"Erreur pdfminer: {e}")
    
    try:
        # Fallback avec PyPDF2
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Erreur PyPDF2: {e}")
        return None

def extract_text_from_doc(file_path):
    """Extrait le texte d'un fichier .doc/.docx"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Erreur extraction DOC: {e}")
        return None

def extract_text_from_file(file_path):
    """Détecte le type de fichier et extrait le texte appropriement"""
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_doc(file_path)
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return None
    return None
