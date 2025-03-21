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

```text
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
## 🏗️ Folder Architecture
NSTU-Transit/
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

## 🏗️ Home Page

![Home](https://github.com/user-attachments/assets/80a55427-ed01-4888-ac39-aed6ec74e4f4)


