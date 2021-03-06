import logging

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/posts')
def posts():
    return render_template('posts.html')
@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/account')
def account():
    return render_template('account.html')
@app.route('/messages')
def messages():
    return render_template('messages.html')
@app.route('/files')
def files():
    return render_template('files.html')
@app.route('/jobs')
def jobs():
    return render_template('jobs.html')
@app.route('/train')
def train():
    return render_template('training.html')
@app.route('/container')
def container():
    return render_template('container.html')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run()
