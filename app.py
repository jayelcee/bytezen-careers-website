# Importing necessary modules from Flask and other files
from flask import (
    Flask, render_template, jsonify, request, redirect, url_for, 
    send_from_directory, session, flash,
)
import psycopg2
from database import db_session, Job, JobApplicant
from file_saver import save_resume, UPLOAD_FOLDER
from status_update import update_applicant_status
import os
import random
import string

# Initialize the Flask application
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Setting secret key from environment variable

# Route to load applicants from the database
@app.route('/load_applicants')
def load_applicants_route():
    applicants = load_applicants()
    return jsonify({"applicants": applicants})

# Function to load applicants from the database
def load_applicants():
    # Retrieve only applicants whose status is 'Accepted'
    applicants = db_session.query(JobApplicant).filter(JobApplicant.status == 'Accepted').all()
    applicants_data = []
    for job_applicants in applicants:
        job_id = job_applicants.job_id
        job = db_session.query(Job).filter(Job.id == job_id).first()
        if job:
            salary = f"{job.currency} {job.salary:,.2f}"
        else:
            salary = "N/A"
        applicant_data = {
            "id": job_applicants.id,
            "job_id": job_id,
            "job_title": job_applicants.job_title,
            "name": job_applicants.name,
            "age": job_applicants.age,
            "birthday": job_applicants.birthday,
            "phone_number": job_applicants.phone_number,
            "email": job_applicants.email,
            "address": job_applicants.address,
            "gender": job_applicants.gender,
            "nationality": job_applicants.nationality,
            "status": job_applicants.status,
            "username": job_applicants.username,
            "is_deleted": job_applicants.is_deleted,
            "salary": salary  # Add salary to the applicant data
        }
        applicants_data.append(applicant_data)
    return applicants_data


# Route to add an applicant
@app.route("/applicants")
def applicants():
    applicants = load_applicants()  # Load applicants from the database
    return render_template("applicants.html", applicants=applicants)

# Database connection function
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='bytezen_careers_db',
            user='bytezen_careers_db_user',
            password='tQMQEPV4eK0QB8AvL7EhTDVS2YrmXRQt',
            host='dpg-cmp6tqol5elc73fn9e20-a.singapore-postgres.render.com',
            port='5432'
        )
        return conn
    except psycopg2.Error as e:
        error_message = f"Error connecting to the database: {str(e)}"
    print(error_message)
    return None

# Route to delete an applicant
@app.route('/delete_applicant', methods=['POST'])
def delete_applicant():
    applicant_id = request.form.get('id')
    if applicant_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Update the is_deleted field to 1 for the given applicant ID instead of deleting the row
        cursor.execute('UPDATE job_applicants SET is_deleted = 1 WHERE id = %s', (applicant_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'No Applicant ID provided'})

@app.route('/update_applicant', methods=['GET', 'POST'])
def update_applicant():
    if request.method == 'POST':
        applicant_id = request.args.get('id')
        if not applicant_id:
            return jsonify({'success': False, 'message': 'Applicant ID is required'}), 400

        # Extract form data
        name = request.form.get('name')
        age = request.form.get('age')
        birthday = request.form.get('birthday')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        address = request.form.get('address')
        gender = request.form.get('gender')
        nationality = request.form.get('nationality')
        username = request.form.get('username')
        password = request.form.get('password')

        # Find the applicant in the database
        applicant = db_session.query(JobApplicant).filter_by(id=applicant_id).first()
        if not applicant:
            return jsonify({'success': False, 'message': 'Applicant not found'}), 404

        # Update applicant details
        applicant.name = name
        applicant.age = age
        applicant.birthday = birthday
        applicant.phone_number = phone_number
        applicant.email = email
        applicant.address = address
        applicant.gender = gender
        applicant.nationality = nationality
        applicant.username = username
        applicant.password = password

        # Commit the changes to the database
        db_session.commit()

        return jsonify({'success': True})

    elif request.method == 'GET':
        applicant_id = request.args.get('id')
        if applicant_id:
            return render_template('update_applicant.html', applicant_id=applicant_id)
        else:
            return "Applicant ID is required", 400


@app.route('/get_applicant_details')
def get_applicant_details():
    applicant_id = request.args.get('id')
    if applicant_id:
        applicant = db_session.query(JobApplicant).filter_by(id=applicant_id).first()
        if applicant:
            return jsonify({
                "name": applicant.name,
                "age": applicant.age,
                "birthday": applicant.birthday,
                "job_title": applicant.job_title,
                "phone_number": applicant.phone_number,
                "email": applicant.email,
                "address": applicant.address,
                "gender": applicant.gender,
                "nationality": applicant.nationality,
                "username": applicant.username,
                "password": applicant.password
            })
        else:
            return jsonify({"error": "Applicant not found"}), 404
    else:
        return jsonify({"error": "Applicant ID is required"}), 400



# Function to load jobs from the database
def load_jobs_from_db(job_id=None):
    query = db_session.query(Job)
    if job_id is not None:
        # Fetch a specific job using its ID
        job = query.filter(Job.id == job_id).first()
        return (
            {
                # Structuring job data if job is found
                "id": job.id,
                "title": job.title,
                "location": job.location,
                "salary": f"{job.currency} {job.salary:,.2f}",
                "currency": job.currency,
                "responsibilities": job.responsibilities.split("\n"),
                "requirements": job.requirements.split("\n"),
            }
            if job
            else None
        )
    # Fetch all jobs if no specific job ID is provided
    jobs = query.all()
    jobs_list = [
        {
            # Structuring each job data
            "id": job.id,
            "title": job.title,
            "location": job.location,
            "salary": f"{job.currency} {job.salary:,.2f}",
            "currency": job.currency,
            "responsibilities": job.responsibilities.split("\n"),
            "requirements": job.requirements.split("\n"),
        }
        for job in jobs
    ]
    return jobs_list

# Route for the home page
@app.route("/")
def bytezen():
    jobs = load_jobs_from_db()  # Load all jobs for display
    return render_template("home.html", jobs=jobs, company_name="ByteZen")

# Route for listing jobs in JSON format
@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)  # Return jobs in JSON format

# Route for showing a specific job
@app.route("/job/<int:job_id>")
def show_job(job_id):
    job = load_jobs_from_db(job_id=job_id)
    if job is not None:
        return render_template("jobpage.html", job=job)  # Show job details page
    return "Job not found", 404  # Job not found error

# Password generator for applicants
def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# Route for applying to a job
@app.route("/apply", methods=["POST"])
def apply_for_job():
    job_id = request.form.get("job_id")
    if job_id is None:
        return "Job ID is required", 400  # Validation for job ID

    # Fetch the job details from the database
    job = db_session.query(Job).get(job_id)
    if not job:
        return "Job not found", 404  # Job not found error

    job_title = job.title

    # Extract applicant details from the form
    name = request.form["name"]
    age = request.form["age"]
    birthday = request.form["birthday"]
    phone_number = request.form["phone_number"]
    email = request.form["email"]
    address = request.form["address"]
    linkedin = request.form.get("linkedin") 
    education = request.form["education"]
    experience = request.form["experience"]
    gender = request.form["gender"]
    nationality = request.form["nationality"]

    resume_file = request.files["resume"]
    resume_filename = save_resume(resume_file)  # Save the resume file
    if resume_filename is None:
        return "Invalid file format", 400  # Validate resume file format

    # Generate username and password for the applicant
    username = f"{name.replace(' ', '').lower()}{random.randint(100, 999)}"
    password = generate_password()

    # Create a new job applicant record
    new_applicant = JobApplicant(
        job_id=job_id,
        job_title=job_title,
        name=name,
        age=age,
        birthday=birthday,
        phone_number=phone_number,
        email=email,
        address=address,
        linkedin=linkedin,
        education=education,
        experience=experience,
        gender=gender,
        nationality=nationality,
        resume=resume_filename,
        status="Pending",  # Set initial status as Pending
        username=username,
        password=password
    )

    # Add new applicant to the database and commit changes
    db_session.add(new_applicant)
    db_session.commit()

    # Redirect to the confirmation page with the applicant's ID
    return redirect(url_for("confirmation", applicant_id=new_applicant.id))

# Route for the confirmation page after application
@app.route("/confirmation/<int:applicant_id>")
def confirmation(applicant_id):
    # Fetch applicant details from the database
    applicant = db_session.query(JobApplicant).filter(JobApplicant.id == applicant_id).first()

    if applicant:
        return render_template("confirmation.html", applicant=applicant)  # Show confirmation page
    else:
        return "Applicant not found", 404  # Applicant not found error

# Route for serving uploaded files (like resumes)
@app.route("/resume/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Route for the applicant tracking page
@app.route("/applicant-tracking")
def applicant_tracking():
    return render_template("applicant_tracking.html")

# Route for admin login
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        # Fetch username and password from the form
        username = request.form["username"]
        password = request.form["password"]

        # Check credentials against environment variables
        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
            session["logged_in"] = True
            return redirect(url_for("admin_monitoring"))  # Redirect to admin monitoring page if login is successful
        else:
            flash("Invalid credentials. Please try again.")
            return redirect(url_for("admin_login"))

    return render_template("admin_login.html")  # Show admin login page

# Route for applicant login
@app.route("/applicant-login", methods=["GET", "POST"])
def applicant_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        applicant = db_session.query(JobApplicant).filter_by(username=username, password=password).first()
        if applicant:
            session["applicant_id"] = applicant.id
            return redirect(url_for("applicant_status"))
        else:
            flash("Invalid credentials. Please try again.")
            return redirect(url_for("applicant_login"))

    return render_template("applicant_login.html")

# Route for applicant status
@app.route("/applicant-status")
def applicant_status():
    applicant_id = session.get("applicant_id")
    if not applicant_id:
        return redirect(url_for("applicant_login"))

    applicant = db_session.query(JobApplicant).get(applicant_id)
    return render_template("applicant_status.html", applicant=applicant)

# Route for applicant logout
@app.route("/logout")
def logout():
    session.pop("applicant_id", None)
    return redirect(url_for("bytezen"))

# Route for admin monitoring
@app.route("/admin-monitoring")
def admin_monitoring():
    if not session.get("logged_in"):
        return redirect(url_for("admin_login"))  # Redirect to login if not logged in

    # Fetch all applicants from the database
    applicants = db_session.query(JobApplicant).all()
    return render_template("admin_monitoring.html", applicants=applicants)  # Show admin monitoring page

# Route for updating applicant status
@app.route("/update-status", methods=["POST"])
def update_status():
    return update_applicant_status()  # Call the function to update status

# Route for checking applicant status
@app.route("/check_status", methods=["POST"])
def check_status():
    name = request.form.get("name")

    if not name:
        return jsonify({"success": False, "message": "Name is required"})  # Validate name input

    # Fetch applicants with names matching the input
    applicants = db_session.query(JobApplicant).filter(JobApplicant.name.ilike(f'%{name}%')).all()

    if applicants:
        matching_applicants = []
        for applicant in applicants:
            matching_applicants.append({
                "name": applicant.name,
                "job_title": applicant.job_title,
                "status": applicant.status
            })
        return jsonify({"success": True, "applicants": matching_applicants})  # Return matching applicants
    else:
        return jsonify({"success": False, "message": "No matching applicants found"})  # No matching applicants

# Teardown context to remove database session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
