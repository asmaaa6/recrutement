# Traitement du texte de CV

import re
import string
from collections import Counter

def process_cv_text(text):
    """
    Nettoie et traite le texte d'un CV
    
    Args:
        text: Texte brut du CV
    
    Returns:
        str: Texte traité
    """
    
    if not text:
        return ""
    
    # Convertir en minuscules
    text = text.lower()
    
    # Supprimer les caractères spéciaux excessifs
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def extract_keywords(text, num_keywords=20):
    """
    Extrait les mots-clés principaux d'un texte
    
    Args:
        text: Texte à analyser
        num_keywords: Nombre de mots-clés à retourner
    
    Returns:
        list: Liste des mots-clés
    """
    
    # Stop words communs en français
    stop_words = {
        'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'mais',
        'est', 'au', 'en', 'l', 'avec', 'pour', 'par', 'sur', 'ce', 'que',
        'qui', 'dans', 'a', 'à', 'été', 'sont', 'avoir', 'etre', 'se', 'son',
        'mon', 'ton', 'mes', 'tes', 'ses', 'nos', 'vos', 'leurs', 'je', 'tu',
        'il', 'elle', 'nous', 'vous', 'ils', 'elles'
    }
    
    # Tokenizer simple
    words = text.lower().split()
    
    # Filtrer les stop words et les mots courts
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Compter les occurrences
    word_counts = Counter(keywords)
    
    # Retourner les top keywords
    return [word for word, count in word_counts.most_common(num_keywords)]

def normalize_text(text):
    """Normalise le texte (accents, casse, etc.)"""
    import unicodedata
    
    # Supprimer les accents
    nfkd = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    
    return text

def extract_entities(text):
    """Extrait les entités nommées du texte"""
    # Expressions régulières pour certaines entités
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phones = re.findall(r'(?:\+33|0)[1-9](?:[0-9]{8}|[0-9]{9})', text)
    urls = re.findall(r'https?://[^\s]+', text)
    
    return {
        'emails': emails,
        'phones': phones,
        'urls': urls
    }
