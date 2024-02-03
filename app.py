# Importing necessary modules from Flask and other files
from flask import (
    Flask, render_template, jsonify, request, redirect, url_for, 
    send_from_directory, session, flash,
)
from database import db_session, Job, JobApplicant
from file_saver import save_resume, UPLOAD_FOLDER
from status_update import update_applicant_status
import os

# Initialize the Flask application
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Setting secret key from environment variable

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
    email = request.form["email"]
    linkedin = request.form.get("linkedin") 
    education = request.form["education"]
    experience = request.form["experience"]

    resume_file = request.files["resume"]
    resume_filename = save_resume(resume_file)  # Save the resume file
    if resume_filename is None:
        return "Invalid file format", 400  # Validate resume file format

    # Create a new job applicant record
    new_applicant = JobApplicant(
        job_id=job_id,
        job_title=job_title,
        name=name,
        email=email,
        linkedin=linkedin,
        education=education,
        experience=experience,
        resume=resume_filename,
        status="Pending",  # Set initial status as Pending
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
