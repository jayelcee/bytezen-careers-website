from flask import Flask, render_template, jsonify
from database import db_session, Job 

app = Flask(__name__)

def load_jobs_from_db():
  jobs = db_session.query(Job).all()
  jobs_list = [
    {
      'id': job.id,
      'title': job.title,
      'location': job.location,
      'salary': f"{job.currency} {job.salary:,.2f}",
      'currency': job.currency,
      'responsibilities': job.responsibilities,
      'requirements': job.requirements
    } for job in jobs
  ]
  return jobs_list

@app.route("/")
def hello_bytezen():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs,company_name='ByteZen')

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.teardown_appcontext
def shutdown_session(exception=None):
  db_session.remove()

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)