-- Schéma de Base de Données MySQL pour RecrutAI
-- À exécuter pour initialiser la base de données

-- Créer la base de données
CREATE DATABASE IF NOT EXISTS recrutement;
USE recrutement;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'candidate',
    first_name VARCHAR(80),
    last_name VARCHAR(80),
    phone VARCHAR(20),
    profile_picture VARCHAR(255),
    bio TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table des offres d'emploi
CREATE TABLE IF NOT EXISTS offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recruiter_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description LONGTEXT NOT NULL,
    requirements TEXT,
    company VARCHAR(200) NOT NULL,
    location VARCHAR(200),
    job_type VARCHAR(50),
    min_salary FLOAT,
    max_salary FLOAT,
    min_experience INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    status VARCHAR(20) DEFAULT 'open',
    required_skills VARCHAR(500),
    preferred_skills VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deadline TIMESTAMP DEFAULT (DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 30 DAY)),
    FOREIGN KEY (recruiter_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_recruiter (recruiter_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table des CVs
CREATE TABLE IF NOT EXISTS cvs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_size INT,
    file_type VARCHAR(10),
    raw_text LONGTEXT,
    processed_text LONGTEXT,
    full_name VARCHAR(200),
    email VARCHAR(120),
    phone VARCHAR(20),
    location VARCHAR(200),
    skills TEXT,
    education TEXT,
    experience TEXT,
    languages TEXT,
    certifications TEXT,
    analysis_score FLOAT DEFAULT 0.0,
    is_analyzed BOOLEAN DEFAULT FALSE,
    analysis_date TIMESTAMP,
    years_experience FLOAT,
    last_position VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_is_analyzed (is_analyzed)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table des candidatures
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    offer_id INT NOT NULL,
    cv_id INT,
    status VARCHAR(50) DEFAULT 'pending',
    cv_score FLOAT DEFAULT 0.0,
    match_score FLOAT DEFAULT 0.0,
    overall_score FLOAT DEFAULT 0.0,
    recruiter_notes TEXT,
    candidate_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    interview_date TIMESTAMP,
    interview_notes TEXT,
    interview_score FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (offer_id) REFERENCES offers(id) ON DELETE CASCADE,
    FOREIGN KEY (cv_id) REFERENCES cvs(id) ON DELETE SET NULL,
    UNIQUE KEY unique_user_offer (user_id, offer_id),
    INDEX idx_user (user_id),
    INDEX idx_offer (offer_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table des conversations chatbot
CREATE TABLE IF NOT EXISTS conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    message_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Créer les index supplémentaires pour les performances
CREATE INDEX idx_application_user ON applications(user_id);
CREATE INDEX idx_application_offer ON applications(offer_id);
CREATE INDEX idx_offers_recruiter ON offers(recruiter_id);
