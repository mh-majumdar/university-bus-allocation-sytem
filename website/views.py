from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Profile
from flask import Flask, render_template, request, flash, redirect
from flask_mail import Mail, Message
from . import db, mail  # Ensure mail is initialized in __init__.py
from .models import CampusBusBooking
from .models import MaijdeeBusBooking
import datetime
import math

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("index.html", user=current_user)

@views.route("/user_info", methods=["GET", "POST"])
@login_required
def user_info():
    # Get or create profile for current user
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
    
    if request.method == "POST":
        # Personal Information
        profile.fathers_name = request.form.get("fathers_name")
        profile.mothers_name = request.form.get("mothers_name")
        profile.date_of_birth = request.form.get("date_of_birth")
        profile.phone = request.form.get("phone")
        profile.guardians_name = request.form.get("guardians_name")
        profile.guardians_phone = request.form.get("guardians_phone")
        profile.hall_for_residence = request.form.get("hall_for_residence")
        profile.hall_for_roll = request.form.get("hall_for_roll")
        profile.blood_group = request.form.get("blood_group")
        profile.religion = request.form.get("religion")
        profile.nationality = request.form.get("nationality")
        profile.nid_number = request.form.get("nid_number")
        profile.gender = request.form.get("gender")
        profile.marital_status = request.form.get("marital_status")
        
        # Present Address
        profile.present_division = request.form.get("present_division")
        profile.present_district = request.form.get("present_district")
        profile.present_upazilla = request.form.get("present_upazilla")
        profile.present_post_office = request.form.get("present_post_office")
        profile.present_village = request.form.get("present_village")
        profile.present_house_name = request.form.get("present_house_name")
        profile.present_house_no = request.form.get("present_house_no")
        profile.present_road_no = request.form.get("present_road_no")
        
        # Permanent Address
        profile.permanent_division = request.form.get("permanent_division")
        profile.permanent_district = request.form.get("permanent_district")
        profile.permanent_upazilla = request.form.get("permanent_upazilla")
        profile.permanent_post_office = request.form.get("permanent_post_office")
        profile.permanent_village = request.form.get("permanent_village")
        profile.permanent_house_name = request.form.get("permanent_house_name")
        profile.permanent_house_no = request.form.get("permanent_house_no")
        profile.permanent_road_no = request.form.get("permanent_road_no")
        
        # Academic Information
        profile.academic_level = request.form.get("academic_level")
        profile.faculty = request.form.get("faculty")
        profile.department = request.form.get("department")
        profile.session = request.form.get("session")
        profile.year_term = request.form.get("year_term")
        profile.student_id = request.form.get("student_id")
        
        db.session.commit()
        flash("Profile information updated successfully!", "success")
        return render_template("profile_info.html", user=current_user, profile=profile)
    
    return render_template("profile_form.html", user=current_user, profile=profile)

@views.route("/edit_profile")
@login_required
def edit_profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    return render_template("profile_form.html", user=current_user, profile=profile)

@views.route("/view_profile")
@login_required
def view_profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
        flash("Please complete your profile information.", "info")
        return redirect(url_for("views.edit_profile"))
    
    return render_template("profile_info.html", user=current_user, profile=profile)

@views.route("/to_campus", methods=["GET", "POST"])
@login_required
def to_campus():
    if request.method == "POST":
        # Debugging print statements
        print("Form submitted!")  
        print("Raw Form Data:", request.form)

        departure_time = request.form.get("startTime")
        destination = request.form.get("stopLocation")

        print(f"Departure Time: {departure_time}, Destination: {destination}")

        if not departure_time or not destination:
            flash("Please select both departure time and destination.", "danger")
            return render_template("campus.html", user=current_user)

        # Check if booking is being made at least 45 minutes before departure
        now = datetime.datetime.now()

        try:
            departure_time_obj = datetime.datetime.strptime(departure_time, "%I:%M %p").time()
            departure_datetime = datetime.datetime.combine(now.date(), departure_time_obj)

            if departure_datetime < now:
                tomorrow = now.date() + datetime.timedelta(days=1)
                departure_datetime = datetime.datetime.combine(tomorrow, departure_time_obj)

            if (departure_datetime - now).total_seconds() < 45 * 60:
                flash("Booking must be completed at least 45 minutes before the scheduled departure time.", "danger")
                return render_template("campus.html", user=current_user)

        except ValueError as e:
            flash(f"Invalid time format: {str(e)}", "danger")
            return render_template("campus.html", user=current_user)

        # Create a new bus booking
        new_booking = CampusBusBooking(
            user_id=current_user.id,
            departure_time=departure_time,
            destination=destination
        )

        print(f"New Booking Created: {new_booking}")

        # Add to database and commit
        try:
            db.session.add(new_booking)
            db.session.commit()
            print("Booking saved to database!")  # Debug message
            flash("Your bus booking has been confirmed!", "success")
            return redirect(url_for("views.campus_booking_confirmation", booking_id=new_booking.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Database error: {str(e)}", "danger")
            print("Database error:", str(e))  # Debug message
            return render_template("campus.html", user=current_user)

    return render_template("campus.html", user=current_user)

@views.route("/campus_booking_confirmation/<int:booking_id>")
@login_required
def campus_booking_confirmation(booking_id):
    booking = CampusBusBooking.query.get_or_404(booking_id)
    
    # Ensure users can only view their own bookings
    if booking.user_id != current_user.id:
        flash("You don't have permission to view this booking.", "danger")
        return redirect(url_for("views.to_campus"))  # Changed to to_campus to match the form
    
    return render_template("campus_booking_confirmation.html", booking=booking, user=current_user)



@views.route("/to_maijdee", methods=["GET", "POST"])
@login_required
def to_maijdee():
    if request.method == "POST":
        departure_time = request.form.get("startTime")
        destination = request.form.get("stopLocation")

        if not departure_time or not destination:
            flash("Please select both departure time and destination.", "danger")
            return render_template("maijdee.html", user=current_user)

        now = datetime.datetime.now()
        try:
            departure_time_obj = datetime.datetime.strptime(departure_time, "%I:%M %p").time()
            departure_datetime = datetime.datetime.combine(now.date(), departure_time_obj)

            if departure_datetime < now:
                tomorrow = now.date() + datetime.timedelta(days=1)
                departure_datetime = datetime.datetime.combine(tomorrow, departure_time_obj)

            if (departure_datetime - now).total_seconds() < 45 * 60:
                flash("Booking must be completed at least 45 minutes before departure.", "danger")
                return render_template("maijdee.html", user=current_user)

        except ValueError as e:
            flash(f"Invalid time format: {str(e)}", "danger")
            return render_template("maijdee.html", user=current_user)

        new_booking = MaijdeeBusBooking(
            user_id=current_user.id,
            departure_time=departure_time,
            destination=destination
        )

        try:
            db.session.add(new_booking)
            db.session.commit()
            flash("Your bus booking has been confirmed!", "success")
            return redirect(url_for("views.maijdee_booking_confirmation", booking_id=new_booking.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Database error: {str(e)}", "danger")

    return render_template("maijdee.html", user=current_user)


@views.route("/maijdee_booking_confirmation/<int:booking_id>")
@login_required
def maijdee_booking_confirmation(booking_id):
    booking = MaijdeeBusBooking.query.get_or_404(booking_id)
    
    # Ensure users can only view their own bookings
    if booking.user_id != current_user.id:
        flash("You don't have permission to view this booking.", "danger")
        return redirect(url_for("views.to_maijdee"))  # Changed to to_campus to match the form
    
    return render_template("maijdee_booking_confirmation.html", booking=booking, user=current_user)


@views.route('/booking_history')
@login_required
def booking_history():
    # Get user profile data
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    
    # Get all bookings for the current user
    bookings = CampusBusBooking.query.filter_by(user_id=current_user.id).order_by(CampusBusBooking.booking_time.desc()).all()
    maijdee_bookings = MaijdeeBusBooking.query.filter_by(user_id=current_user.id).order_by(MaijdeeBusBooking.booking_time.desc()).all()
    
    # Calculate if bookings can be cancelled (for example, only if booking is still "Confirmed")
    for booking in bookings:
        booking.can_cancel = booking.status == "Confirmed"
    
    for booking in maijdee_bookings:
        booking.can_cancel = booking.status == "Confirmed"
    
    return render_template('booking_history.html', profile=profile, bookings=bookings,  maijdee_bookings= maijdee_bookings )

@views.route('/cancel_booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = CampusBusBooking.query.get_or_404(booking_id)
    maijdee_booking = MaijdeeBusBooking.query.get_or_404(booking_id)
    
    # Verify that the booking belongs to the current user
    if booking.user_id != current_user.id:
        flash('You are not authorized to cancel this booking', 'danger')
        return redirect(url_for('booking_history'))
    
    # Only allow cancellation if booking is still in "Confirmed" status
    if booking.status != "Confirmed":
        flash('This booking cannot be cancelled', 'warning')
        return redirect(url_for('views.booking_history'))
    
    # Update the booking status
    booking.status = "Cancelled"
    db.session.commit()
    
    flash('Your booking has been successfully cancelled', 'success')
    return redirect(url_for('views.booking_history'))



@views.route("/bus_allocation")
@login_required
def bus_allocation():
     # Check if user has admin privileges
    if not current_user:
        flash("You don't have permission to access this page.", "danger")
        return redirect(url_for("views.home"))
    
    # Get all confirmed campus bookings
    campus_bookings = CampusBusBooking.query.filter_by(status="Confirmed").all()
    
    # Get all confirmed maijdee bookings
    maijdee_bookings = MaijdeeBusBooking.query.filter_by(status="Confirmed").all()
    
    # Process campus bookings
    campus_schedule = {}
    for booking in campus_bookings:
        # Group by departure time
        if booking.departure_time not in campus_schedule:
            campus_schedule[booking.departure_time] = {
                'total_students': 0,
                'destinations': {}
            }
        
        # Count students by destination
        if booking.destination not in campus_schedule[booking.departure_time]['destinations']:
            campus_schedule[booking.departure_time]['destinations'][booking.destination] = 0
        
        campus_schedule[booking.departure_time]['destinations'][booking.destination] += 1
        campus_schedule[booking.departure_time]['total_students'] += 1
    
    # Calculate required buses for campus (40 students per bus, rounded up)
    for time_slot in campus_schedule:
        total_students = campus_schedule[time_slot]['total_students']
        campus_schedule[time_slot]['buses_required'] = math.ceil(total_students / 40)
    
    # Process maijdee bookings
    maijdee_schedule = {}
    for booking in maijdee_bookings:
        # Group by departure time
        if booking.departure_time not in maijdee_schedule:
            maijdee_schedule[booking.departure_time] = {
                'total_students': 0,
                'destinations': {}
            }
        
        # Count students by destination
        if booking.destination not in maijdee_schedule[booking.departure_time]['destinations']:
            maijdee_schedule[booking.departure_time]['destinations'][booking.destination] = 0
        
        maijdee_schedule[booking.departure_time]['destinations'][booking.destination] += 1
        maijdee_schedule[booking.departure_time]['total_students'] += 1
    
    # Calculate required buses for maijdee (40 students per bus, rounded up)
    for time_slot in maijdee_schedule:
        total_students = maijdee_schedule[time_slot]['total_students']
        maijdee_schedule[time_slot]['buses_required'] = math.ceil(total_students / 40)
    
    # Calculate overall statistics
    total_campus_students = sum(schedule['total_students'] for schedule in campus_schedule.values())
    total_maijdee_students = sum(schedule['total_students'] for schedule in maijdee_schedule.values())
    total_students = total_campus_students + total_maijdee_students
    
    total_campus_buses = sum(schedule['buses_required'] for schedule in campus_schedule.values())
    total_maijdee_buses = sum(schedule['buses_required'] for schedule in maijdee_schedule.values())
    total_buses = total_campus_buses + total_maijdee_buses
    
    # Sort schedules by time for better display
    sorted_campus_schedule = dict(sorted(campus_schedule.items()))
    sorted_maijdee_schedule = dict(sorted(maijdee_schedule.items()))
    
    return render_template(
        "allocation.html",
        user=current_user,
        campus_schedule=sorted_campus_schedule,
        maijdee_schedule=sorted_maijdee_schedule,
        total_students=total_students,
        total_buses=total_buses,
        total_campus_students=total_campus_students,
        total_campus_buses=total_campus_buses,
        total_maijdee_students=total_maijdee_students,
        total_maijdee_buses=total_maijdee_buses
    )

@views.route("/transport_poll")
@login_required
def transport_poll():
    return render_template("poll.html", user=current_user)

@views.route("/complain", methods=["GET", "POST"])
@login_required
def complain():
    if request.method == "POST":
        name = request.form.get("name")
        department = request.form.get("department")
        session = request.form.get("session")
        bus_category = request.form.get("bus_category")
        message = request.form.get("message")

        recipient_email = "mh.majumdar1952@gmail.com"  # Update with your email
        subject = f"New Bus Complaint from {name}"

        message_body = f"""
        Name: {name}
        Department: {department}
        Session: {session}
        Bus Category: {bus_category}

        Complaint Message:
        {message}
        """

        try:
            msg = Message(subject, sender="", recipients=[recipient_email])
            msg.body = message_body
            mail.send(msg)
            flash("Complaint submitted successfully!", "success")
        except Exception as e:
            flash(f"Error sending complaint: {str(e)}", "danger")

        return redirect(url_for("views.complain"))

    return render_template("complain.html", user=current_user)




