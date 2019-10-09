from honeybadger import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

app = application = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
