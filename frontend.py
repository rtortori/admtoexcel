import sys
import logging
import os
import re
import logging
from flask import Flask, render_template, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from admtoexcel import convert

# App variables
appname = 'admtoexcel'
UPLOAD_FOLDER = './userupload'
ALLOWED_EXTENSIONS = set(['json'])
policy_file_pattern = 'policies\.json'
clusters_file_pattern = 'clusters\.json'
dynamic_adm = False

# Logging

# Custom logger
def logger(name, logfile):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(logfile, mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger


log = logger(appname, '{}/{}.log'.format(os.getcwd(), appname))

# Application Object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Secret Key
app.config['SECRET_KEY'] = b'\xdb\xe6\xb2x\xd4\x8a!\xaa\xc6Mu\xac\xfd(&P\x08\xc18\x8c\xb6\xc0\xcd|'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Log when application starts
log.info('{} has just started.'.format(appname))

# View Functions


@app.route('/', methods=['GET', 'POST'])
def index():
    # Process form. We expect the policies.json and clusters.json as well as the ADM type
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        if request.form.get("dynamic_adm"):
            global dynamic_adm
            dynamic_adm = True
        # If one of the files is not matching the pattern a 404 is returned
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            if re.search(policy_file_pattern, filename):
                policy_file = filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            elif re.search(clusters_file_pattern, filename):
                cluster_file = filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return render_template('failure.html')
        # Convert the ADM into Excel
        file_to_send = convert(dynamic_adm, policy_file, cluster_file)
        # Return the excel file to the client with the right name
        return send_file(file_to_send, as_attachment=True)
    # Home page
    return render_template('index.html')

# For Kubernetes readiness probes
@app.route('/ready')
def ready():
    return "I'm ready"

# For Kubernetes liveness probes
@app.route('/health')
def health():
    return "I'm alive"

# Errors handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def int_err(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
