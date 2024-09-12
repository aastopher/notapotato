import home
from components import base
from nicegui import ui
from cryptography.fernet import Fernet

key = Fernet.generate_key()

# init home
home.render()
base.logger.info("home rendered.")

ui.run(title='notapotato', favicon='./static/favicon.ico', storage_secret=key)
base.logger.info("app started successfully!")