import requests
import asyncio
from nicegui import ui

async def get_image_from_api(url):
    '''function to retrieve image data and create html tag'''

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Get the base64-encoded image data and stuff in html data string
    base64_img = f"data:image/png;base64,{response.json()['image']}"

    # Create an HTML `img` tag with the base64-encoded image data
    img_tag = f'<img src="{base64_img}">'

    return img_tag

# Define the URL of your API endpoint
api_url = "http://fastapi:8000/potato"
# api_url = "http://127.0.0.1:8000/potato"

# Define and set ui color
theme_color = '#c3ac74'
ui.colors(secondary=theme_color)


# Create Title
with ui.element('span').style(f'background-color: {theme_color}').classes('w-full justify-center'):
    with ui.row().classes('w-full justify-center'):

        ui.label('Not a Potato') \
            .classes('text-h3 text-center') \
            .style('font-family: "Trebuchet MS", sans-serif; font-size: 500%; font-weight: 800; padding-bottom: 1rem; padding-top: 1rem; color: white')

# Define a button handler
async def button_handler():
    '''button handler collects returned image tags into a container'''
    # Sleep so notification has time to execute
    await asyncio.sleep(0.01)

    # Collect image tag
    img_tag = await get_image_from_api(api_url)

    # Stuff container
    with container:
        with ui.card().classes('justify-center'):
            ui.html(img_tag).classes('bg-transparent')


# Create button with image flex row underneath
with ui.row().classes('w-full justify-center').style('padding-top: 1rem'):

    # Start async task and notify user
    ui.button('Generate Potato', on_click=lambda: asyncio.create_task(button_handler()) and ui.notify('Generating potato...')) \
        .classes('items-center') \
        .props('unelevated color=secondary')
    
    # Define image container
    container = ui.row().classes('w-full justify-center flex-wrap').style('padding-top: 1rem')

ui.run()