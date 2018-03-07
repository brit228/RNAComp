import logging
import datetime

from flask import Flask, jsonify, request, render_template
import flask_cors
from google.cloud import datastore
import google.auth.transport.requests
import google.oauth2.id_token

ds = datastore.Client(project='rnacompute')
HTTP_REQUEST = google.auth.transport.requests.Request()

app = Flask(__name__)
flask_cors.CORS(app)

@app.route('/posts', methods=['GET'])
def posts():
    page = request.args.get('page')
    query = ds.query(kind='posts')
    query.order = ['-TimeDate']
    if page == '0':
        posts = dict(query.fetch(limit=3))
        return render_template('posts.html', posts=posts, main=True)
    elif page.isdigit():
        posts = dict(query.fetch(limit=10, offset=int(page)*10-10))
        return render_template('posts.html', posts=posts, main=False)
    else:
        return 'Unauthorized', 401

@app.route('/jobs', methods=['GET'])
def jobs():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401
    user = claims['sub']
    jstatus = request.args.get('status')
    page = request.args.get('page')
    if page.isdigit() == False:
        return 'Unauthorized', 401
    if int(page) < 1:
        return 'Unauthorized', 401
    query = ds.query(kind='jobs')
    query.add_filter('Status', '=', jstatus)
    if jstatus == 'pending':
        query.order = ['TimeDate']
    else:
        query.add_filter('User', '=', user)
        query.order = ['-TimeDate']
    jobs = dict(query.fetch(limit=10, offset=int(page)*10-10))
    for job in jobs:
        job['Walltime'] = str(datetime.timedelta(seconds=job['Walltime']))
        job['Submit'] = str(job['Submit'])
        job['Start'] = str(job['Start'])
        job['End'] = str(job['End'])
    return render_template('jobs.html', jobs=jobs, status=jtype)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    app.run()
