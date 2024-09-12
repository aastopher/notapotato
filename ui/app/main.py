import home
from components import base
from nicegui import ui
from cryptography.fernet import Fernet

key = Fernet.generate_key()

home.render()
base.logger.info("Home page rendered successfully.")

ui.run(title="notapotato", favicon="./static/favicon.ico", storage_secret=key)
base.logger.info("App started successfully!")
