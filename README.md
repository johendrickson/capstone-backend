# Plant Pal – Backend 🌱

This is the backend service for **Plant Pal**, my Ada Developers Academy capstone project.  

It handles plant data management, AI integration, user accounts, weather alerts, and email reminders.

- **Main Capstone Repository:** [Plant Pal Main – Project Scope + Information](https://github.com/johendrickson/capstone)
- **Frontend Repository:** [Plant Pal Frontend – React + TypeScript interface](https://github.com/johendrickson/capstone-frontend)

---

## Features

- **RESTful API** – Endpoints for plant CRUD operations, user accounts, and settings.
- **Gemini AI Integration** – Auto-generates plant information based on a scientific name.
- **Weather Alerts** – Detects extreme weather (heat waves, frost, cold snaps, dry heat) and sends email alerts.
- **Watering Reminders** – Sends user-defined email reminders.
- **Geocoding Support** – Automatically converts ZIP codes to latitude/longitude for accurate weather forecasts.
- **Email Notifications** – Integrated with cron jobs for automated alerts.

---

## Tech Stack

- **Language:** Python
- **Framework:** Flask
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **AI Integration:** Google Gemini API
- **Weather Data:** Open-Meteo API
- **Email Sending:** Flask-Mail + SMTP
- **Task Scheduling:** Cron jobs

---

## Environment Variables & API Keys

This project uses several environment variables to connect to external services (database, email, weather API, AI API, geocoding, etc.).  

For **security reasons**, sensitive values such as API keys, passwords, and database credentials **should never** be committed to the repository. Instead:  

- Store these values in a local `.env` file for local development.  
- Add the keys as **GitHub Repository Secrets** for deployment and CI/CD workflows.  
- Do not post these values publicly, even in screenshots or documentation.

Example `.env` file structure (values are placeholders):

```env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_NAME=your_db_name

EMAIL_USER=your_email
EMAIL_PASSWORD=your_email_password

OPENWEATHER_API_KEY=your_weather_api_key
GEMINI_API_KEY=your_gemini_api_key
LOCATIONIQ_API_KEY=your_locationiq_api_key
```

---

## Local Setup

1. **Clone the Repository**
```bash
   git clone https://github.com/your-username/plant-pal-backend.git
   cd plant-pal-backend
```

2. Create and Activate a Virtual Environment
```bash
  python -m venv venv
  source venv/bin/activate   # macOS/Linux
  venv\Scripts\activate      # Windows
```

3. Install Dependencies
```bash
  pip install -r requirements.txt
```

4. Set Up Environment Variables

    Create a .env file in the project root.

    Copy the variables listed in the Environment Variables section.

    Fill in your own secret values (from secure storage).

5. Run Database Migrations
(Only if you are initializing the database locally)
```bash
  flask db upgrade
```

6. Start the Development Server
```bash
  flask run
```
