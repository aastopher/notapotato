import requests
import asyncio
import aiohttp
import os
from nicegui import ui

#### GLOBALS ####

# Define the URL of your API endpoint
api_url = os.environ.get('API_URL')

# Define and set ui color
theme_color = '#c3ac74'
ui.colors(secondary=theme_color)


#### FUNCTIONS ####

# async def get_image_from_api(url):
#     '''function to retrieve image data and create html tag'''

#     # Send a GET request to the API endpoint
#     response = requests.get(url)

#     # Get the base64-encoded image data and stuff in html data string
#     base64_img = f"data:image/png;base64,{response.json()['image']}"

#     # Create an HTML `img` tag with the base64-encoded image data
#     img_tag = f'<img src="{base64_img}">'

#     return img_tag

# async def get_image_from_api(url, max_retries=5):
#     '''function to retrieve image data and create html tag'''

#     retries = 0
#     while retries < max_retries:
#         # Send a GET request to the API endpoint
#         response = requests.get(url)

#         if response.ok:
#             # Get the base64-encoded image data and stuff in html data string
#             base64_img = f"data:image/png;base64,{response.json()['image']}"

#             # Create an HTML `img` tag with the base64-encoded image data
#             img_tag = f'<img src="{base64_img}">'

#             return img_tag
#         else:
#             # increment retries
#             retries += 1

#     raise ValueError(f"Failed to retrieve image after {max_retries} attempts")

async def get_image_from_api(url):
    '''function to retrieve image data and create html tag'''

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # Get the base64-encoded image data and stuff in html data string
            base64_img = f"data:image/png;base64,{(await response.json())['image']}"

            # Create an HTML `img` tag with the base64-encoded image data
            img_tag = f'<img src="{base64_img}">'

    return img_tag

# Define a button handler
async def button_handler():
    '''button handler collects returned image tags into a container'''

    ui.notify('Generating potato...')
    # Collect image tag
    img_tag = await get_image_from_api(api_url)

    # Stuff container
    with container:
        with ui.card().classes('justify-center'):
            ui.html(img_tag).classes('bg-transparent')


#### PAGE ####

# Create Title
with ui.element('span').style(f'background-color: {theme_color}').classes('w-full justify-center'):
    with ui.row().classes('w-full justify-center'):

        ui.label('Not a Potato') \
            .classes('text-h3 text-center') \
            .style('font-family: "Roboto", sans-serif; font-size: 500%; font-weight: 700; padding-bottom: 1rem; padding-top: 1rem; color: white')


# Create button with image flex row underneath
with ui.row().classes('w-full justify-center').style('padding-top: 1rem'):

    # Start async task and notify user
    ui.button('Generate Potato', on_click=button_handler) \
        .classes('items-center') \
        .props('unelevated color=secondary')
    
    # Define image container
    container = ui.row().classes('w-full justify-center flex-wrap').style('padding-top: 1rem')

ui.run(title='notapotato', favicon='./static/favicon.ico')