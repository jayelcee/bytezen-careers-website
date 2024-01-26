from flask import Flask, render_template, jsonify
from database import db_session, Job 

app = Flask(__name__)

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
    # Store applicant information to database
    return "Application submitted", 200

@app.teardown_appcontext
def shutdown_session(exception=None):
  db_session.remove()

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
