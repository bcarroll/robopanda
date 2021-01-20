import logging
from bin._logging import logger, handler, werkzeug_handler, sqlalchemy_handler
from flask import Flask
from flask import request
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template
from flask import flash
from flask import escape
from flask import jsonify

from flask_bootstrap import Bootstrap

from functools import wraps

from bin.vision.webstreaming import generate_video_frame

# use PAM authentication - https://stackoverflow.com/questions/26313894/flask-login-using-linux-system-credentials
from simplepam import authenticate

logging.Formatter('[%(asctime)s][%(levelname)s][%(thread)s][%(name)s] %(message)s')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WowWeeRoboPanda'
Bootstrap(app)

################################################
# Setup logging
app.logger.addHandler(handler)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logger.level)
werkzeug_logger.addHandler(werkzeug_handler)

sqlalchemy_logger = logging.getLogger('sqlalchemy')
sqlalchemy_logger.setLevel(logger.level)
sqlalchemy_logger.addHandler(sqlalchemy_handler)

##########################################################
# Error pages
@app.errorhandler(403)
def forbidden(error):
    logger.debug('Returning 403 error page')
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def page_not_found(error):
    logger.debug('Returning 404 error page')
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    logger.debug('Returning 500 error page')
    return render_template('errors/500.html'), 500
##########################################################

def require_login(f):
    '''
    Decorator for routes that require a logged in session
    '''
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'username' in session:
            return( f(*args, **kwargs) )
        else:
            return(render_template('login.html'))
    return (wrapped)

@app.route('/')
@require_login
def index():
    return( render_template('index.html') )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(str(username), str(password)):
            session['username'] = request.form['username']
            logger.info(str(username) + ' successfully logged in')
            return ( redirect(url_for('index')) )
        else:
            logger.info('Login failed for ' + str(username))
            flash('Invalid username/password', 'error')
            return(render_template('login.html'))
    else:
        return(render_template('login.html'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return( redirect(url_for('index')) )

@app.route("/video_feed")
@require_login
def video_feed():
    # return the response generated along with the specific media type (mime type)
    return Response(generate_video_frame(), mimetype = "multipart/x-mixed-replace; boundary=frame")


