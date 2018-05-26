# -*- encoding: UTF-8 -*-
import logging
from flaskagram import app

debug = True

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run(debug=debug)

if __name__ == '__main__':
    app.run(debug=debug)