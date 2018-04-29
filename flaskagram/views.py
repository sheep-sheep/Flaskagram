# -*- encoding: UTF-8 -*-


from flaskagram import app


@app.route('/')
def index():
    return 'This is Flaskagram'
