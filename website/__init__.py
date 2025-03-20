from flask import Flask
from flask_login import LoginManager
from .extensions import db
from flask_mail import Mail
from flask_apscheduler import APScheduler
from .models import CampusBusBooking, MaijdeeBusBooking
from datetime import datetime


DB_NAME = "database.db"
mail = Mail()
scheduler = APScheduler()

def clear_booking_tables():
    """Clear all records from the booking tables."""
    try:
        from flask import current_app
        from .models import CampusBusBooking, MaijdeeBusBooking
        
        # Delete all records from both tables
        db.session.query(CampusBusBooking).delete()
        db.session.query(MaijdeeBusBooking).delete()
        db.session.commit()
        print(f"[{datetime.now()}] All booking records cleared successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"[{datetime.now()}] Error clearing booking tables: {str(e)}")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "supersecretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = ''  # Replace with your email
    app.config['MAIL_PASSWORD'] = ''  # Use an App Password, not your email password
    mail.init_app(app)

    # Initialize and configure the scheduler
    scheduler.init_app(app)
    scheduler.add_job(
        id='clear_bookings_job',
        func=clear_booking_tables,
        trigger='cron',
        hour=23,
        minute=25
    )
    scheduler.start()
    print("Scheduler started. Tables will be cleared daily at 22:00.")

    # Import models after initializing db
    from .models import User

    # Register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/", name="home")

    # Create database
    with app.app_context():
        db.create_all()
        print("Database created!")

    # Configure login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app