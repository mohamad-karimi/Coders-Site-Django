# Coders Site — Django LMS

<p align="center">
  A modern Learning Management System built with Django.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" />
  <img src="https://img.shields.io/badge/Django-5.x-green?logo=django" />
  <img src="https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## 📖 About

**Coders Site** is a full-featured Learning Management System (LMS) developed with **Django**.

The platform provides separate functionality for students and instructors, with course management, learning progress, authentication, blogging, reviews, and dashboards.

## ✨ Features

* 🔐 User authentication and role-based access
* 🎓 Course, section, and lesson management
* 👨‍🏫 Instructor dashboard
* 📚 Student dashboard
* 📈 Lesson and course progress tracking
* 🛒 Course enrollment and purchase system
* ⭐ Course ratings, reviews, and comments
* 📝 Blog with categories and tags
* 🔎 Course search, filtering, and pagination
* 🛡️ reCAPTCHA and security configurations
* ☁️ Cloudinary media storage
* 📱 Responsive Bootstrap interface

## 🛠️ Tech Stack

| Technology    | Usage                |
| ------------- | -------------------- |
| Python        | Backend              |
| Django        | Web Framework        |
| Bootstrap     | Frontend             |
| PostgreSQL    | Production Database  |
| SQLite        | Development Database |
| Cloudinary    | Media Storage        |
| CKEditor      | Rich Text Editor     |
| django-taggit | Tags                 |
| Gunicorn      | WSGI Server          |
| WhiteNoise    | Static Files         |

## 📁 Project Structure

```text
Coders-Site-Django/
├── authentication/    # User authentication
├── blog/              # Blog system
├── course/            # Courses and learning
├── dashboard/         # Student dashboard
├── instructor/        # Instructor features
├── website/           # Public website
├── coders/            # Django configuration
├── templates/
├── static/
├── manage.py
└── requirements.txt
```

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/TwoOfWands/Coders-Site-Django.git
cd Coders-Site-Django
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Create an admin account:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## ⚙️ Environment Variables

Create a `.env` file in the project root and configure the required environment variables.

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=your-database
DB_USER=your-user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

Additional configuration may be required for services such as **Cloudinary, email, and reCAPTCHA**.

> Never commit real credentials or secret keys to the repository.

## 🗄️ Database

The project uses Django's relational model system to connect users, instructors, courses, sections, lessons, enrollments, purchases, and learning progress.

The repository also includes a visual representation of the database models:

```text
myapp_models.png
```

## 🔄 Learning Flow

```text
Register
   ↓
Browse Courses
   ↓
Enroll / Purchase
   ↓
Start Learning
   ↓
Complete Lessons
   ↓
Track Progress
```

## 🔒 Security

The project includes Django security features such as:

* CSRF protection
* reCAPTCHA
* Environment-based secrets
* Content Security Policy
* Clickjacking protection
* Authentication controls

For production, make sure `DEBUG=False` and all sensitive credentials are properly configured.

## 📄 License

This project is licensed under the **MIT License**.

## 👨‍💻 Author

**TwoOfWands**

GitHub:
https://github.com/TwoOfWands/Coders-Site-Django

---

<p align="center">
  Built with ❤️ using Django
</p>
