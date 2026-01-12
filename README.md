# Worlds AI Bot - Backend API

Flask-based REST API backend for the Worlds AI Bot Learning Management System.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MongoDB (local or Atlas)
- pip

### Installation

```bash
# Clone the repository
cd worlds_ai_bot_flask_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your values

# Run the server
python app.py
```

Server runs at `http://localhost:5001`

---

## 📚 API Routes

### 🔐 Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/signup` | Register new user | No |
| POST | `/signin` | Login user | No |
| POST | `/signout` | Logout user | Yes |
| POST | `/reset-password-request` | Request password reset email | No |
| POST | `/reset-password` | Reset password with token | No |

### 👤 Profile

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/profile` | Get current user profile | Yes |
| PATCH | `/profile/edit` | Update current user profile | Yes |
| DELETE | `/profile/delete` | Delete user account | Yes |
| GET | `/show-profiles` | Get all users (admin) | Admin |
| GET | `/show-user/:id` | Get user by ID | Admin |
| PUT | `/update-user/:id` | Update user by ID | Admin |
| DELETE | `/delete-profile/:id` | Delete user by ID | Admin |

### 📚 Courses

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/show-courses` | Get all courses | No |
| GET | `/show-course/:id` | Get course by ID | No |
| POST | `/create-course` | Create new course | Admin |
| PUT | `/update-course/:id` | Update course | Admin |
| DELETE | `/delete-course/:id` | Delete course | Admin |
| POST | `/validate-coupon/:courseId` | Validate coupon code | Yes |

### 🎓 Bootcamps

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/all-bootcamps` | Get all bootcamps | No |
| GET | `/show-bootcamp/:id` | Get bootcamp by ID | No |
| POST | `/create-bootcamp` | Create new bootcamp | Admin |
| PUT | `/update-bootcamp/:id` | Update bootcamp | Admin |
| DELETE | `/delete-bootcamp/:id` | Delete bootcamp | Admin |

### 🗺️ Roadmaps

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/show-roadmaps` | Get all roadmaps | No |
| GET | `/show-roadmap/:id` | Get roadmap by ID | No |
| POST | `/create-roadmap` | Create new roadmap | Admin |
| PUT | `/update-roadmap/:id` | Update roadmap | Admin |
| DELETE | `/delete-roadmap/:id` | Delete roadmap | Admin |

### 📂 Roadmap Topics

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/show-road-topics` | Get all roadmap topics | No |
| GET | `/show-road-topic/:id` | Get roadmap topic by ID | No |
| POST | `/create-road-topic` | Create new roadmap topic | Admin |
| PUT | `/update-road-topic/:id` | Update roadmap topic | Admin |
| DELETE | `/delete-road-topic/:id` | Delete roadmap topic | Admin |

### 🎬 Recordings

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/show-recordings` | Get all recordings | No |
| GET | `/show-recording/:id` | Get recording by ID | No |
| POST | `/add-recording` | Create new recording | Admin |
| PUT | `/update-recordings/:id` | Update recording | Admin |
| DELETE | `/delete-recordings/:id` | Delete recording | Admin |

### 📹 Success Videos

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/show-videos` | Get all success videos | No |
| GET | `/show-video/:id` | Get video by ID | No |
| POST | `/create-video` | Create new video | Admin |
| PUT | `/update-video/:id` | Update video | Admin |
| DELETE | `/delete-video/:id` | Delete video | Admin |

### 🏢 Company Logos

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/show-companies` | Get all company logos | No |
| GET | `/show-company/:id` | Get company by ID | No |
| POST | `/create-logo` | Create new company logo | Admin |
| PUT | `/update-company/:id` | Update company | Admin |
| DELETE | `/delete-company/:id` | Delete company | Admin |

### 💼 Jobs

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/all-jobs` | Get all jobs | No |
| GET | `/show-job/:id` | Get job by ID | No |
| POST | `/create-job` | Create new job | Admin |
| PUT | `/update-job/:id` | Update job | Admin |
| DELETE | `/delete-job/:id` | Delete job | Admin |

### 🎤 Interview Questions

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/all-questions` | Get all interview topics | Yes |
| GET | `/show-questions/:id` | Get interview topic by ID | Yes |
| POST | `/create-questions` | Create new interview topic | Admin |
| PUT | `/update-questions/:id` | Update interview topic | Admin |
| DELETE | `/delete-questions/:id` | Delete interview topic | Admin |

### 💻 Coding Tests

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/all-tests` | Get all coding tests | Yes |
| GET | `/show-test/:id` | Get test by ID | Yes |
| POST | `/create-test` | Create new test | Admin |
| PUT | `/update-test/:id` | Update test | Admin |
| DELETE | `/delete-test/:id` | Delete test | Admin |

### 📋 Registrations

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/all-registers` | Get all registrations | Admin |
| POST | `/create-register` | Create new registration | No |
| DELETE | `/delete-register/:id` | Delete registration | Admin |

### 📧 Contact Info

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/all-contacts` | Get all contact info | No |
| GET | `/show-contact/:id` | Get contact by ID | No |
| POST | `/create-contact` | Create contact info | Admin |
| PUT | `/update-contact/:id` | Update contact info | Admin |
| DELETE | `/delete-contact/:id` | Delete contact info | Admin |

### 💬 User Feedbacks

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/all-feedbacks` | Get all user feedbacks | Admin |
| GET | `/show-feedback/:id` | Get feedback by ID | Admin |
| POST | `/create-feedback` | Submit feedback (contact form) | No |
| PUT | `/update-feedback/:id` | Update feedback status | Admin |
| DELETE | `/delete-feedback/:id` | Delete feedback | Admin |

### 📜 Privacy Policy

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/show-privacies` | Get all privacy policies | No |
| POST | `/create-privacy` | Create privacy policy | Admin |
| DELETE | `/delete-privacy/:id` | Delete privacy policy | Admin |

### 💳 Payments

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/profile/add-course` | Add course after payment | Yes |

---

## 🔒 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

**Include token in requests:**
```
Authorization: Bearer <your_jwt_token>
```

---

## 🚀 Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Using Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
```

---

## 📁 Project Structure

```
worlds_ai_bot_flask_backend/
├── app.py                 # Main application
├── config/
│   ├── config.py          # Configuration
│   └── database.py        # MongoDB connection
├── models/                # Database models
├── routes/                # API route handlers
├── middlewares/           # Auth middleware
├── requirements.txt       # Dependencies
└── .env.example           # Environment template
```

---

## 📝 License

MIT License - See LICENSE file for details.