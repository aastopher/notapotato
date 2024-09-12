import aiohttp
from components import base
from nicegui import ui, Client


def render() -> None:
    """Render the main page for the Not a Potato app."""

    @ui.page("/")
    async def page(client: Client) -> None:
        """
        Render the home page and handle client connections.

        Args:
            client (Client): The client object representing the connected user session.
        """
        await client.connected()
        base.logger.info("Client connected.")

        # Render the action bar and initialize styles
        base.action_bar()
        base.init_style()
        base.logger.info("Action bar & style initialized.")

        # Define the URL of your API endpoint
        api_url: str = "http://fastapi:8000/potato"

        async def get_image_from_api(url: str) -> str:
            """
            Retrieve image data from the API and generate an HTML `img` tag.

            Args:
                url (str): The URL of the API endpoint to fetch the image.

            Returns:
                str: An HTML string with a base64-encoded image tag.
            """
            base.logger.info("Requesting potato generation...")
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    # Get the base64-encoded image data from the API response
                    base64_img = (
                        f"data:image/png;base64,{(await response.json())['image']}"
                    )
                    # Create an HTML `img` tag with the base64-encoded image data
                    img_tag = f'<img src="{base64_img}">'
            return img_tag

        async def button_handler() -> None:
            """
            Button handler to trigger the image generation and update the UI with the image.

            This function sends a request to the API to generate the image, shows a notification while the image is being generated,
            and displays the resulting image in the UI.
            """
            notification = ui.notification(timeout=None, type="info")
            notification.message = "Generating potato..."
            notification.spinner = True

            base.logger.info("Generating potato...")
            try:
                # Collect the image tag from the API
                img_tag = await get_image_from_api(api_url)

                # Display the generated image in the container
                with container:
                    with ui.card().classes("justify-center").style(
                        "background-color: white;"
                    ):
                        ui.html(img_tag).classes("bg-transparent")

                base.logger.info("Potato generated successfully!")
                notification.spinner = False
                notification.dismiss()
            except Exception as e:
                base.logger.error(f"Potato failed to generate: {e}")
                notification.message = "Potato failed to generate."
                notification.spinner = False
                notification.type = "warning"
                notification.close_button = True

        # Welcome message
        with ui.row().classes("w-full justify-center").style("padding-top: 1rem"):
            ui.html("<center>Welcome to Not a Potato!</center>").style(
                base.font_style_base(size=125, color=base.colors["primary"])
            )

        # Create button with an image container underneath
        with ui.row().classes("w-full justify-center").style("padding-top: 1rem"):
            # Start async task and notify user
            ui.button("Generate Potato", on_click=button_handler).classes(
                "items-center"
            ).props("unelevated color=secondary")

            # Define image container for holding generated potato images
            container = (
                ui.row()
                .classes("w-full justify-center flex-wrap")
                .style("padding-top: 1rem")
            )
