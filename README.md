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

## 📁 Project Structure

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

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/nstu-transit.git
cd nstu-transit

