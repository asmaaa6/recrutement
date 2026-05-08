# Calcul de scores

def calculate_cv_quality_score(cv_info):
    """
    Calcule un score de qualité du CV (0-1)
    
    Args:
        cv_info: Dictionnaire avec les infos extraites du CV
    
    Returns:
        float: Score entre 0 et 1
    """
    
    score = 0.0
    max_score = 0.0
    
    # Présence de compétences (0.3)
    max_score += 0.3
    if cv_info.get('skills'):
        score += min(0.3, len(cv_info['skills']) * 0.015)
    
    # Présence d'éducation (0.2)
    max_score += 0.2
    if cv_info.get('education'):
        score += min(0.2, len(cv_info['education']) * 0.1)
    
    # Présence d'expérience (0.25)
    max_score += 0.25
    if cv_info.get('experience'):
        score += min(0.25, len(cv_info['experience']) * 0.125)
    
    # Complétude des infos personnelles (0.15)
    max_score += 0.15
    contact_info = cv_info.get('contact_info', {})
    if contact_info.get('emails'):
        score += 0.075
    if contact_info.get('phones'):
        score += 0.075
    
    # Langues (0.1)
    max_score += 0.1
    if cv_info.get('languages'):
        score += min(0.1, len(cv_info['languages']) * 0.05)
    
    return min(1.0, score)

def normalize_score(raw_score, min_val=0, max_val=1):
    """Normalise un score entre min et max"""
    if max_val == min_val:
        return 0.5
    return (raw_score - min_val) / (max_val - min_val)

def calculate_compatibility_percentage(score):
    """Convertit un score (0-1) en pourcentage"""
    return int(score * 100)
