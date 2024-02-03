# Importing necessary modules for file operations
import os
from werkzeug.utils import secure_filename

# Define the upload folder for resumes
UPLOAD_FOLDER = os.path.join('static', 'resume')
# Set of allowed file extensions for resumes
ALLOWED_EXTENSIONS = {"pdf"}

# Function to check if a file is allowed based on its extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to save the resume file
def save_resume(file):
    if file and allowed_file(file.filename):
        # Create the upload folder if it does not exist
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        resume_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(resume_path)

        return filename  
    else:
        return None