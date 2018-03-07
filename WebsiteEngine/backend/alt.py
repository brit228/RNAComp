import logging

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/posts', methods=['GET'])
def posts():
    page = request.args.get('page')
    posts = [{
            "Image": "https://cloud.netlifyusercontent.com/assets/344dbf88-fdf9-42bb-adb4-46f01eedd629/68dd54ca-60cf-4ef7-898b-26d7cbe48ec7/10-dithering-opt.jpg",
            "Title": "Test",
            "TextAbbr": "asbhiajklasdnjklsdnauioadklasblsdabnlasdnjkl",
            "Link": "https://cloud.netlifyusercontent.com/assets/344dbf88-fdf9-42bb-adb4-46f01eedd629/68dd54ca-60cf-4ef7-898b-26d7cbe48ec7/10-dithering-opt.jpg"
        }]
    if page == '0':
        return render_template('posts.html', posts=posts, main=True)
    elif page.isdigit():
        return app.render_template('posts.html', posts=posts, main=False)
    else:
        return server_error('No such page')

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    app.run()
