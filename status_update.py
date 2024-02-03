from flask import request, jsonify
from database import db_session, JobApplicant

def update_applicant_status():
    try:
        applicant_id = request.form.get('applicant_id')
        new_status = request.form.get('new_status')

        applicant = db_session.query(JobApplicant).get(applicant_id)

        if applicant:
            applicant.status = new_status
            db_session.commit()
            return jsonify({'success': True, 'message': 'Status updated successfully.'})
        else:
            return jsonify({'success': False, 'message': 'Applicant not found.'})

    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred during the update.'})
