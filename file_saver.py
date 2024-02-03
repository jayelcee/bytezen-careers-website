import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static', 'resume')
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
  return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_resume(file):
  if file and allowed_file(file.filename):
    if not os.path.exists(UPLOAD_FOLDER):
      os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(file.filename)

    resume_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(resume_path)

    return filename  

  else:
    return None