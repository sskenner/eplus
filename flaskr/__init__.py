import os

from flask import Flask
from selenium import webdriver

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden be instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World'

    @app.route('/process')
    def process():

        # chrome_options = ChromeOptions()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=1366x768")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument(
        #     "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
        driver = webdriver.Chrome()
        driver.get("https://www.google.com")
        driver.save_screenshot("screenshot.png")
        return 'Printed'

    # register the database commands
    from . import db
    db.init_app(app)

    # apply the blueprints to the app
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
