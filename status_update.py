# Importing necessary modules from Flask and the database
from flask import request, jsonify
from database import db_session, JobApplicant

# Function to update the status of a job applicant
def update_applicant_status():
    try:
        # Fetch applicant ID and new status from the request
        applicant_id = request.form.get('applicant_id')
        new_status = request.form.get('new_status')

        # Query the database for the specific applicant
        applicant = db_session.query(JobApplicant).get(applicant_id)

        if applicant:
            # Update the status and commit the changes to the database
            applicant.status = new_status
            db_session.commit()
            return jsonify({'success': True, 'message': 'Status updated successfully.'})
        else:
            return jsonify({'success': False, 'message': 'Applicant not found.'})

    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred during the update.'})