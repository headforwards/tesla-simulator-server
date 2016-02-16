#!/usr/bin/env python
from app import create_app

app = create_app()


if __name__ == "__main__":
    app.socketio.run(
        app,
        debug=app.config['DEBUG'],
        port=app.config['PORT']
    )
