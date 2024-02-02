from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
from database import db_session, Job, JobApplicant
from file_saver import save_resume, UPLOAD_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_jobs_from_db(job_id=None):
  query = db_session.query(Job)
  if job_id is not None:
    job = query.filter(Job.id == job_id).first()
    return {
      'id': job.id,
      'title': job.title,
      'location': job.location,
      'salary': f"{job.currency} {job.salary:,.2f}",
      'currency': job.currency,
      'responsibilities': job.responsibilities.split('\n'), 
      'requirements': job.requirements.split('\n'), 
    } if job else None

  jobs = query.all()
  jobs_list = [
    {
      'id': job.id,
      'title': job.title,
      'location': job.location,
      'salary': f"{job.currency} {job.salary:,.2f}",
      'currency': job.currency,
      'responsibilities': job.responsibilities.split('\n'),
      'requirements': job.requirements.split('\n'),
    } for job in jobs
  ]
  return jobs_list

@app.route("/")
def bytezen():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs, company_name='ByteZen')

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/job/<int:job_id>")
def show_job(job_id):
  job = load_jobs_from_db(job_id=job_id)
  if job is not None:
    return render_template('jobpage.html', job=job)
  return "Job not found", 404

@app.route("/apply", methods=["POST"])
def apply_for_job():
  job_id = request.form.get('job_id')
  if job_id is None:
    return "Job ID is required", 400

  job = db_session.query(Job).get(job_id)
  if not job:
    return "Job not found", 404

  # Now you have the job, you can get the job title
  job_title = job.title
  
  # Retrieve form data
  name = request.form['name']
  email = request.form['email']
  linkedin = request.form.get('linkedin')  # .get() is used to handle optional fields
  education = request.form['education']
  experience = request.form['experience']

  # Process the resume file
  resume_file = request.files['resume']
  resume_filename = save_resume(resume_file)  # Make sure this is updated to just the filename
  if resume_filename is None:
    return "Invalid file format", 400

  # Create a new JobApplicant object and set its properties
  new_applicant = JobApplicant(
    job_id=job_id,
    job_title=job_title,
    name=name,
    email=email,
    linkedin=linkedin,
    education=education,
    experience=experience,
    resume=resume_filename,  # Store just the filename
    status='pending'
  )

  # Add the new object to the session and commit it
  db_session.add(new_applicant)
  db_session.commit()

  # Redirect to a new confirmation page with the applicant's id
  # Make sure this line is within the same block where new_applicant is defined
  return redirect(url_for('confirmation', applicant_id=new_applicant.id))

@app.route("/confirmation/<int:applicant_id>")
def confirmation(applicant_id):
  # Retrieve the applicant's data from the database
  applicant = db_session.query(JobApplicant).filter(JobApplicant.id == applicant_id).first()

  # Check if the applicant exists
  if applicant:
    return render_template("confirmation.html", applicant=applicant)
  else:
    return "Applicant not found", 404

@app.route('/resume/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.teardown_appcontext
def shutdown_session(exception=None):
  db_session.remove()

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
