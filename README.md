# Driving School Management System 🚗

[![CI/CD Status](https://github.com/arvinddchoudhary/driving_school_website/actions/workflows/django.yml/badge.svg)](https://github.com/arvinddchoudhary/driving_school_website/actions)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)

A robust **Full Stack Web Application** designed to digitize driving school operations. This project goes beyond standard CRUD operations by implementing a **containerized architecture** and **automated CI/CD pipelines**, demonstrating readiness for enterprise-grade deployment.

## 🚀 Features

### Core Functionality
* **MVT Architecture:** scalable backend logic using Django's Model-View-Template pattern.
* **Role-Based Access Control:** Distinct portals for Admins, Instructors, and Students.
* **Dynamic Booking System:** Real-time slot management for driving lessons.
* **Responsive UI:** Mobile-first design using Bootstrap 5.

### DevOps & Infrastructure
* **🐳 Containerization:** Fully dockerized application using `Dockerfile` and `docker-compose` for environment consistency.
* **🚀 Production Ready:** Configured with **Gunicorn** as the application server and **Nginx** as the reverse proxy.
* **🔄 CI/CD Pipelines:** Automated testing and linting (Flake8) configured via GitHub Actions.
* **🗄️ Database Management:** Seamless switch between SQLite (Dev) and PostgreSQL (Prod).

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python, Django 4.x |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap |
| **Database** | PostgreSQL / SQLite |
| **Containerization** | Docker, Docker Compose |
| **Server** | Nginx, Gunicorn |
| **CI/CD** | GitHub Actions |

## ⚙️ Installation & Setup

You can run this project locally using **Docker (Recommended)** or a manual Python environment.

### Option A: Docker Setup (Recommended)

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/arvinddchoudhary/driving_school_website.git](https://github.com/arvinddchoudhary/driving_school_website.git)
    cd driving_school_website
    ```

2.  **Build and Run containers:**
    ```bash
    docker-compose up -d --build
    ```

3.  **Apply Migrations (inside container):**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4.  **Create Superuser:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5.  **Access App:**
    * Application: `http://localhost:8000`
    * Admin Panel: `http://localhost:8000/admin`

---

### Option B: Manual Setup

1.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Database Setup:**
    ```bash
    python manage.py migrate
    ```

4.  **Run Server:**
    ```bash
    python manage.py runserver
    ```

## 🏗️ DevOps Architecture

The project follows a standard containerized workflow:

1.  **Web Container:** Runs the Django application via Gunicorn.
2.  **Nginx Container:** Handles static files and acts as a reverse proxy, forwarding requests to the Web container.
3.  **Database Container:** Hosts the PostgreSQL database (persisted via Docker Volumes).

### CI/CD Pipeline
The `.github/workflows/main.yml` file handles:
* **Linting:** Checks code quality with Flake8.
* **Testing:** Runs Django unit tests on every push to `main`.

## 📂 Project Structure

```text
driving_school_website/
│
├── .github/workflows/    # CI/CD Configurations
├── config/               # Nginx & Docker configurations
├── driving_school/       # Main Django App
├── static/               # Static assets
├── templates/            # HTML Templates
├── Dockerfile            # Image build instructions
├── docker-compose.yml    # Service orchestration
├── manage.py
└── requirements.txt