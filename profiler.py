#!flask/bin/python
from werkzeug.contrib.profiler import ProfilerMiddleware
from MyDanceMoves import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [150])
app.run(debug=True, host="0.0.0.0")