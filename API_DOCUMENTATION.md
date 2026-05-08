# API REST - RecrutAI

Documentation de l'API REST pour la plateforme RecrutAI.

## 🔑 Authentication

Tous les endpoints sauf `/auth/login` et `/auth/signup` nécessitent une authentification.

```
Header: Authorization: Bearer {token}
```

## 📚 Endpoints

### Authentication (`/auth`)

#### Register
```
POST /auth/register
Content-Type: application/json

{
  "username": "john.doe",
  "email": "john@example.com",
  "password": "securepassword",
  "role": "candidate"  // or "recruiter"
}

Response: 201
{
  "id": 1,
  "username": "john.doe",
  "email": "john@example.com",
  "role": "candidate"
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}

Response: 200
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "john.doe",
    "role": "candidate"
  }
}
```

#### Logout
```
POST /auth/logout
Authorization: Bearer {token}

Response: 200
{
  "message": "Successfully logged out"
}
```

### CVs (`/api/cvs`)

#### Upload CV
```
POST /api/cvs/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: <pdf_file>

Response: 201
{
  "id": 1,
  "filename": "resume.pdf",
  "file_size": 245000,
  "uploaded_at": "2026-03-29T10:30:00Z",
  "analysis_status": "pending"
}
```

#### Get CV Analysis
```
GET /api/cvs/{cv_id}/analysis
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "full_name": "Jean Dupont",
  "email": "jean@example.com",
  "phone": "+33123456789",
  "skills": ["Python", "Flask", "SQL", "JavaScript"],
  "education": [
    {
      "degree": "Licence Informatique",
      "school": "Université Paris",
      "year": 2018
    }
  ],
  "experience": [
    {
      "position": "Developer",
      "company": "TechCorp",
      "duration": "2020-2026"
    }
  ],
  "languages": ["Français", "Anglais"],
  "analysis_score": 0.85,
  "quality_score": 0.80
}
```

#### Get User's CVs
```
GET /api/cvs
Authorization: Bearer {token}

Response: 200
[
  {
    "id": 1,
    "filename": "resume.pdf",
    "uploaded_at": "2026-03-29T10:30:00Z",
    "analysis_score": 0.85
  }
]
```

### Offers (`/api/offers`)

#### List Offers
```
GET /api/offers?page=1&limit=10&status=open
Authorization: Bearer {token}

Response: 200
{
  "total": 150,
  "page": 1,
  "offers": [
    {
      "id": 1,
      "title": "Senior Python Developer",
      "company": "TechCorp",
      "location": "Paris",
      "job_type": "CDI",
      "description": "...",
      "required_skills": ["Python", "Flask", "SQL"],
      "min_experience": 3,
      "salary_range": {
        "min": 45000,
        "max": 60000
      },
      "posted_at": "2026-03-20T08:00:00Z",
      "deadline": "2026-04-20T23:59:59Z"
    }
  ]
}
```

#### Get Offer Details
```
GET /api/offers/{offer_id}
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "title": "Senior Python Developer",
  "company": "TechCorp",
  ...
  "applications_count": 45,
  "recruiter": {
    "id": 10,
    "name": "HR Manager"
  }
}
```

#### Create Offer (Recruiter only)
```
POST /api/offers
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Senior Python Developer",
  "description": "Looking for...",
  "company": "TechCorp",
  "location": "Paris",
  "job_type": "CDI",
  "required_skills": ["Python", "Flask", "SQL"],
  "min_experience": 3,
  "salary_min": 45000,
  "salary_max": 60000,
  "deadline": "2026-04-20"
}

Response: 201
{
  "id": 1,
  "title": "Senior Python Developer",
  ...
}
```

### Applications (`/api/applications`)

#### Apply for Offer
```
POST /api/applications
Authorization: Bearer {token}
Content-Type: application/json

{
  "offer_id": 1,
  "cv_id": 1,
  "message": "Je suis intéressé par cette offre..."
}

Response: 201
{
  "id": 1,
  "offer_id": 1,
  "status": "pending",
  "submitted_at": "2026-03-29T11:00:00Z"
}
```

#### Get User Applications
```
GET /api/applications?status=pending
Authorization: Bearer {token}

Response: 200
[
  {
    "id": 1,
    "offer_id": 1,
    "offer_title": "Senior Python Developer",
    "status": "pending",
    "match_score": 0.85,
    "submitted_at": "2026-03-29T11:00:00Z"
  }
]
```

#### Update Application Status (Recruiter only)
```
PATCH /api/applications/{app_id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "accepted",
  "notes": "Excellent match!"
}

Response: 200
{
  "id": 1,
  "status": "accepted",
  "updated_at": "2026-03-29T12:30:00Z"
}
```

### Matching (`/api/matching`)

#### Get Match Score
```
GET /api/matching/{cv_id}/offer/{offer_id}
Authorization: Bearer {token}

Response: 200
{
  "global_score": 0.87,
  "skills_score": 0.90,
  "experience_score": 0.85,
  "textual_score": 0.82,
  "matched_skills": ["Python", "Flask", "SQL"],
  "missing_skills": ["Docker"],
  "recommendation": "Excellente correspondance - À interviewer en priorité"
}
```

#### Get Top Candidates for Offer (Recruiter only)
```
GET /api/offers/{offer_id}/top-candidates?limit=5
Authorization: Bearer {token}

Response: 200
[
  {
    "candidate_id": 5,
    "name": "Jean Dupont",
    "global_score": 0.87,
    "matched_skills": ["Python", "Flask"],
    "application_id": 42
  }
]
```

### Chatbot (`/api/chatbot`)

#### Send Message
```
POST /api/chatbot/message
Authorization: Bearer {token}
Content-Type: application/json

{
  "message": "Quel est le processus de recrutement?",
  "conversation_id": 1
}

Response: 200
{
  "response": "Notre processus comprend 4 étapes...",
  "conversation_id": 1,
  "timestamp": "2026-03-29T11:15:00Z"
}
```

#### Get Conversation History
```
GET /api/chatbot/conversations/{conversation_id}
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "user_id": 1,
  "messages": [
    {
      "sender": "user",
      "text": "Bonjour",
      "timestamp": "2026-03-29T11:00:00Z"
    },
    {
      "sender": "bot",
      "text": "Bienvenue!",
      "timestamp": "2026-03-29T11:00:05Z"
    }
  ]
}
```

### Dashboard (`/api/dashboard`)

#### Get Candidate Stats
```
GET /api/dashboard/candidate
Authorization: Bearer {token}

Response: 200
{
  "total_applications": 8,
  "pending": 2,
  "accepted": 1,
  "rejected": 1,
  "average_score": 0.76,
  "applications": [...]
}
```

#### Get Recruiter Stats
```
GET /api/dashboard/recruiter
Authorization: Bearer {token}

Response: 200
{
  "active_offers": 5,
  "total_applications": 156,
  "average_match_score": 0.72,
  "top_candidates": [...],
  "weekly_applications": [45, 52, 48, 51, 49, 53, 50]
}
```

## 🔍 Query Parameters

### Pagination
```
?page=1&limit=20
```

### Filtering
```
?status=pending
?job_type=CDI
?min_salary=40000&max_salary=60000
```

### Sorting
```
?sort=created_at&order=desc
?sort=match_score&order=desc
```

## ❌ Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid Request",
  "message": "Missing required field: email",
  "code": "INVALID_REQUEST"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Authentication token is missing or invalid",
  "code": "UNAUTHORIZED"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "You don't have permission to access this resource",
  "code": "FORBIDDEN"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found",
  "code": "NOT_FOUND"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

## 📊 Rate Limiting

- General: 100 requêtes/minute
- Upload: 10 requêtes/minute
- Matching: 50 requêtes/minute

## 🔐 CORS

Origins autorisés:
```
- http://localhost:3000
- http://localhost:5000
- https://recrutai.com
```

## 📝 Exemples cURL

### Upload CV
```bash
curl -X POST http://localhost:5000/api/cvs/upload \
  -H "Authorization: Bearer {token}" \
  -F "file=@resume.pdf"
```

### Apply for Offer
```bash
curl -X POST http://localhost:5000/api/applications \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "offer_id": 1,
    "cv_id": 1,
    "message": "Je suis intéressé"
  }'
```

### Get Match Score
```bash
curl -X GET http://localhost:5000/api/matching/1/offer/1 \
  -H "Authorization: Bearer {token}"
```

---

**Version:** 1.0  
**Dernière mise à jour:** 29 Mars 2026
