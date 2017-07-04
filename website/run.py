#!/usr/bin/env python
# Usage: ./run.py to start the server
from app import app
app.run(host='0.0.0.0', threaded=True, debug=True)
