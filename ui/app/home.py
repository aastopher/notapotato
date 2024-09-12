import aiohttp
from components import base
from nicegui import ui, Client

def render():
    
    @ui.page('/')
    async def page(client: Client):
        """Render home page"""

        await client.connected()
        base.logger.info("client connected.")

        # action bar
        base.action_bar()
        base.init_style()
        base.logger.info("action bar & style initialized.")

        # Define the URL of your API endpoint
        api_url = 'http://fastapi:8000/potato'

        async def get_image_from_api(url):
            '''function to retrieve image data and create html tag'''
            base.logger.info("requesting potato generation...")
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

            # ui.notify('Generating potato...')
            notification = ui.notification(timeout=None, type='info')
            notification.message = f'Generating potato...'
            notification.spinner = True

            base.logger.info("generating potato...")
            try:
                # Collect image tag
                img_tag = await get_image_from_api(api_url)
                # Stuff container
                with container:
                    with ui.card().classes('justify-center').style("background-color: white;"):
                        ui.html(img_tag).classes('bg-transparent')
                base.logger.info("potato generated successfully!")
                notification.spinner = False
                notification.dismiss()
            except Exception as e:
                base.logger.error(f'potato failed to generate: {e}')
                notification.message = f'potato failed to generate.'
                notification.spinner = False
                notification.type = 'warning'
                notification.close_button = True

        # welcome message
        with ui.row().classes('w-full justify-center').style('padding-top: 1rem'):
            ui.html('<center>Welcome to Not a Potato!</center>')\
                .style(base.font_style_base(size=125, color=base.colors['primary']))
            
        # Create button with image flex row underneath
        with ui.row().classes('w-full justify-center').style('padding-top: 1rem'):

            # Start async task and notify user
            ui.button('Generate Potato', on_click=button_handler) \
                .classes('items-center') \
                .props('unelevated color=secondary')
            # Define image container
            container = ui.row().classes('w-full justify-center flex-wrap').style('padding-top: 1rem')
