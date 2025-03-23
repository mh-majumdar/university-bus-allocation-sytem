# 🚌 NSTU Transit

**NSTU Transit** is a web-based bus management system tailored for Noakhali Science and Technology University (NSTU). This platform helps students and administrators manage campus transportation efficiently — from viewing schedules to booking seats.

---

## 🚀 Features

- 🔐 Secure user authentication
- 🗓️ Bus schedule view
- 🎫 Real-time seat booking and cancellation
- 📊 Admin dashboard to manage buses, routes, and users
- 📬 Booking history and updates
- 📱 Mobile-friendly responsive UI

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQL, SQLAlchemy
- **Deployment:** Render

---

## 🏗️ Project Architecture


                    ┌──────────────────────┐
                    │     Browser (User)   │
                    └─────────┬────────────┘
                              │ HTTP Request
                              ▼
                     ┌─────────────────┐
                     │   Flask Server  │
                     └─────────────────┘
                              │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
   Authentication       Business Logic     Template Rendering
     (auth.py)              (views.py)           (Jinja2)

                              │
                              ▼
                    ┌──────────────────┐
                    │     Database     │
                    │     SQLite       │
                    └──────────────────┘
---

## NSTU-Transit/
├── website/
│   ├── __init__.py          # App configuration
│   ├── auth.py              # Login, register, logout routes
│   ├── views.py             # Main app views
│   ├── models.py            # Database models
│   ├── static/              # CSS, JS, assets
│   └── templates/           # HTML (Jinja2 templates)
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       └── ...
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
└── README.md

---

## ⚙️ Installation

1. Clone the repository

git clone https://github.com/your-username/bus-management-system.git  
cd bus-management-system

2. Create a virtual environment

python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Run the application

python app.py

5. Visit the app

Open your browser and go to http://127.0.0.1:5000/




