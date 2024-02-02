import os
from werkzeug.utils import secure_filename

# Set the folder where files will be saved
UPLOAD_FOLDER = os.path.join('static', 'resume')
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
  return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_resume(file):
  if file and allowed_file(file.filename):
    # Make sure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
      os.makedirs(UPLOAD_FOLDER)

    # Secure the filename before storing it
    filename = secure_filename(file.filename)

    # Create the full path for the file
    resume_path = os.path.join(UPLOAD_FOLDER, filename)

    # Save the file to the filesystem
    file.save(resume_path)

    # Return only the filename, not the path
    return filename  # Changed from resume_path to filename

  else:
    # Return None if the file wasn't allowed
    return None