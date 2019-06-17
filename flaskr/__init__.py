import os

from flask import Flask
## auto dependancies
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

    # # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World'

    @app.route('/process')
    def process():

        # chrome_options = ChromeOptions()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=1366x768")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument(
        #     "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
        # driver = webdriver.Chrome()
        # driver.get("https://www.google.com")
        # driver.save_screenshot("screenshot.png")

        # > TODO:[DEV/PRD] set MANUAL & AUTO
        # # MANUAL
        # callerADInfo = input("Caller Windows Account Info: ")
        # phoneInfo = input("Type Phone: ")

        ## AUTO
        callerADInfo = "kenners"
        # phoneInfo = "123 456 7899"

        # > TODO:[DEV/PRD] set url
        # # DEV
        base_url = "https://nychhcuat.service-now.com/new_call.do?sys_id=-1&sysparm_stack=new_call_list.do"
        # PROD
        # base_url = "https://nychh.service-now.com/new_call.do?sys_id=-1&sysparm_stack=new_call_list.do"

        # > TODO: set webdriver location & login

        # # hole
        # driver = webdriver.Firefox()
        # # driver = webdriver.Chrome("/usr/local/bin/chromedriver")
        # userNameField = driver.find_element(By.ID,"userNameInput")
        # userNameField.send_keys("CORP\kenners")
        # passwordField = driver.find_element_by_id("passwordInput")
        # passwordField.send_keys("$%RTfgvb0318")
        # driver.find_element_by_id("submitButton").click()

        # hhc
        driver = webdriver.Chrome(
            "C:\\ProgramData\\chocolatey\\lib\\chromedriver"
            "\\tools\\chromedriver.exe")

        driver.get(base_url)

        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "gsft_main")))

        time.sleep(
            5)  ## TODO: use explicit conditions instead of implicit wait https://selenium-python.readthedocs.io/waits.html

        callerField = driver.find_element_by_id("sys_display.new_call.caller")
        callerField.send_keys(callerADInfo)
        callerField.send_keys(Keys.RETURN)
        # time.sleep(5)
        # phoneField = driver.find_element_by_id("new_call.u_business_phone")
        # phoneField.clear()
        # phoneField.send_keys(phoneInfo)
        # phoneField.send_keys(Keys.RETURN)

        text = "Beeping Call"
        driver.find_element_by_partial_link_text(text).click()

        time.sleep(2)

        # > TODO:[DEV/PRD] set button
        # #DEV
        # driver.find_element_by_id("sysverb_insert_bottom").send_keys(Keys.NULL)

        # PROD
        driver.find_element_by_id("sysverb_insert").send_keys(Keys.NULL)

        # TODO: setup flask for user input

        return 'Ticket created'

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
