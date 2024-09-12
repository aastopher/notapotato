from nicegui import ui, app
from loguru import logger

# Configure logger
logger.add(
    "logs/main.log",
    rotation="25 MB",
    retention="30 days",
    colorize=True,
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    level="INFO",
)

#### THEME ###

# Init theme colors
colors = {
    "primary": "#D4A373",  # Light brown, representing the outer skin of a potato
    "secondary": "#A67C52",  # A medium brown, complementing the primary color
    "accent": "#6B4F2F",  # Dark brown, like the soil where potatoes grow
    "dark": "#4A3621",  # A darker shade of brown for depth
    "info": "#B58C60",  # A lighter brown, adding some contrast and balance
}


def init_style() -> None:
    """
    Initialize the theme and styles for the UI.

    This function sets up the color theme, initializes dark mode settings, and applies custom
    styles for UI elements like panels and steppers.
    """
    ui.colors(
        primary=colors["primary"],
        secondary=colors["secondary"],
        accent=colors["accent"],
        dark=colors["dark"],
        info=colors["info"],
    )

    # Initialize dark mode
    app.storage.general["is_dark_mode"] = app.storage.general.get("is_dark_mode", False)

    # Fix dark mode panel color
    ui.query(".q-tab-panels").style("background-color: transparent")
    ui.query(".q-stepper").style("background-color: transparent")

    # Add custom CSS for notifications
    ui.add_css(
        """
        .q-notification__actions {
            color: white;
        }
    """
    )

    # Set background color based on dark mode
    bg_color = colors["dark"] if app.storage.general["is_dark_mode"] else "white"
    ui.query(".q-page").style(f"background-color: {bg_color};")


def font_style_base(
    size: int = 100, weight: int = 700, color: str = "white", styles: str = ""
) -> str:
    """
    Helper function to define base font style.

    Args:
        size (int): Font size as a percentage.
        weight (int): Font weight.
        color (str): Font color.
        styles (str): Additional CSS styles.

    Returns:
        str: A formatted string containing the font-family, size, weight, color, and styles.
    """
    return f'font-family: "Roboto", sans-serif; font-size: {size}%; font-weight: {weight}; color: {color}; {styles}'


#### CUSTOM COMPONENTS


class DarkModeButton(ui.button):
    def __init__(self, dark_mode: ui.dark_mode, *args, **kwargs) -> None:
        """
        Custom button to toggle dark mode.

        Args:
            dark_mode (ui.dark_mode): The dark mode object to control.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.dark_mode = dark_mode
        self._state = app.storage.general["is_dark_mode"]
        self.props("unelevated round").classes("mr-2")
        self.on("click", self.toggle)

    def toggle(self) -> None:
        """Toggle the dark mode state and update the UI accordingly."""
        self._state = not self._state
        self.dark_mode.value = self._state
        app.storage.general["is_dark_mode"] = self._state
        self.update()

    def update(self) -> None:
        """Update the UI background color based on the current dark mode state."""
        if self._state:
            ui.query(".q-page").style(f'background-color: {colors["dark"]};')
        else:
            ui.query(".q-page").style("background-color: white;")
        super().update()


class Tooltip(ui.tooltip):
    def __init__(
        self,
        text: str,
        transition_show: str = "",
        transition_hide: str = "",
        button_pos: str = "",
        tip_pos: str = "",
        offset: int = None,
        **kwargs,
    ) -> None:
        """
        Custom tooltip component with enhanced customization options.

        Args:
            text (str): The tooltip text to display.
            transition_show (str): Transition effect when showing the tooltip.
            transition_hide (str): Transition effect when hiding the tooltip.
            button_pos (str): Position of the button relative to the tooltip.
            tip_pos (str): Position of the tooltip relative to the button.
            offset (int, optional): Offset distance for tooltip placement.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(text, **kwargs)
        self.props(
            f'transition-show="{transition_show}" transition-hide="{transition_hide}" anchor="{tip_pos}" self="{button_pos}" :offset="{offset}"'
        )
        self.classes("bg-secondary")


#### COMPONENTS


def action_bar(engine: str = None) -> None:
    """
    Create an action bar component for the UI, including a title and a dark mode toggle button.

    Args:
        engine (str, optional): Optional engine name to display in the title.
    """
    # Initialize dark mode state
    app.storage.general["is_dark_mode"] = app.storage.general.get("is_dark_mode", True)
    dark_mode = ui.dark_mode(value=app.storage.general["is_dark_mode"])

    # Set title, including engine name if provided
    title = f"notapotato - {engine}" if engine else "notapotato"

    # Create header with title and dark mode toggle
    with ui.header().props("color=primary").classes(
        "flex items-center justify-between w-full"
    ):
        # Main menu
        with ui.button(icon="menu").props("unelevated"):
            with ui.menu() as menu:
                ui.separator()
                ui.menu_item("Close", on_click=menu.close)

        ui.label(title).style(font_style_base(size=150)).classes(
            "flex-none"
        )  # align left

        # Right-aligned container for buttons
        with ui.row().classes("items-center justify-end flex-auto"):
            # Dark mode toggle button
            DarkModeButton(dark_mode, icon="invert_colors")


async def notify_async(*args, **kwargs) -> None:
    """
    Asynchronous wrapper for the notification system.

    Args:
        *args: Variable length argument list for notification content.
        **kwargs: Arbitrary keyword arguments for notification configuration.
    """
    ui.notify(*args, **kwargs)
