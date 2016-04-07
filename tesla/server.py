#!/usr/bin/env python
from app import create_app
import socket_api

app = create_app()

if __name__ == "__main__":
    app.socketio.run(
        app,
        debug=app.config['DEBUG'],
        port=app.config['PORT']
    )
