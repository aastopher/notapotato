from nicegui import ui, app
from loguru import logger

# configure logger
logger.add(
    "logs/main.log", 
    rotation="25 MB", 
    retention="30 days",
    colorize=True, 
    format="{time} | {level} | {name}:{function}:{line} - {message}", 
    level="INFO"
)

#### THEME ###

# init theme colors
colors = {
    'primary': '#D4A373',   # Light brown, representing the outer skin of a potato
    'secondary': '#A67C52', # A medium brown, complementing the primary color
    'accent': '#6B4F2F',    # Dark brown, like the soil where potatoes grow
    'dark': '#4A3621',      # A darker shade of brown for depth
    'info': '#B58C60'       # A lighter brown, adding some contrast and balance
}


def init_style():

    ui.colors(primary=colors['primary'], 
        secondary=colors['secondary'], 
        accent=colors['accent'], 
        dark=colors['dark'],
        info=colors['info'])


    #init dark mode
    app.storage.general['is_dark_mode'] = app.storage.general.get('is_dark_mode', False)

    # fix dark mode panel color
    ui.query('.q-tab-panels').style('background-color: transparent')
    ui.query('.q-stepper').style('background-color: transparent')

    ui.add_css('''
        .q-notification__actions {
            color: white;
        }
    ''')

    bg_color = colors["dark"] if app.storage.general['is_dark_mode'] else "white"
    ui.query('.q-page').style(f'background-color: {bg_color};')

# init font style
def font_style_base(size: int = 100, weight: int = 700, color: str = 'white', styles: str = ''):
    '''Helper function for defining variations of the base font style.'''
    return f'font-family: "Roboto", sans-serif; font-size: {size}%; font-weight: {weight}; color: {color}; {styles}'

#### CUSTOM COMPONENTS

class DarkModeButton(ui.button):
    def __init__(self, dark_mode, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dark_mode = dark_mode
        self._state = app.storage.general['is_dark_mode']
        self.props('unelevated round').classes('mr-2')
        self.on('click', self.toggle)

    def toggle(self) -> None:
        """Toggle the dark mode state."""
        self._state = not self._state
        self.dark_mode.value = self._state
        app.storage.general['is_dark_mode'] = self._state
        self.update()

    def update(self) -> None:
        if self._state:
            ui.query('.q-page').style(f'background-color: {colors["dark"]};')
        else:
            ui.query('.q-page').style('background-color: white;')
        super().update()

class Tooltip(ui.tooltip):
    def __init__(self, text, transition_show='', transition_hide='', button_pos='', tip_pos='', offset=None, **kwargs):
        super().__init__(text, **kwargs)
        self.props(f'transition-show="{transition_show}" transition-hide="{transition_hide}" anchor="{tip_pos}" self="{button_pos}" :offset="{offset}"')
        self.classes('bg-secondary')

#### COMPONENTS

def action_bar(engine: str = None):
    '''Action bar component.'''
    
    # init dark mode
    app.storage.general['is_dark_mode'] = app.storage.general.get('is_dark_mode', True)
    dark_mode = ui.dark_mode(value=app.storage.general['is_dark_mode'])

    # init title
    title = f'notapotato - {engine}' if engine else 'notapotato'

    # init header & title
    with ui.header().props('color=primary').classes('flex items-center justify-between w-full'):
        
        # main menu
        with ui.button(icon='menu').props('unelevated'):
            with ui.menu() as menu:
                # ui.menu_item('Home', lambda: ui.open('/'))
                # ui.menu_item('UFC', lambda: ui.open('/ufc'))
                # ui.menu_item('Boxing', lambda: ui.open('/boxing'))
                ui.separator()
                ui.menu_item('Close', on_click=menu.close)
                
        ui.label(title).style(font_style_base(size=150)).classes('flex-none')  # align left

        # right-aligned container for buttons
        with ui.row().classes('items-center justify-end flex-auto'):                    
            # dark mode toggle
            DarkModeButton(dark_mode, icon='invert_colors')


async def notify_async(*args, **kwargs):
    '''Async notify wrapper.'''
    ui.notify(*args, **kwargs)