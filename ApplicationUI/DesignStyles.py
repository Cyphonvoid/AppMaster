import customtkinter
from PIL import Image

BACKGROUND_COLOR = "#0E0E0E"  # Grey/Blue
SECONDARY_COLOR = "#282828"   # Greyish
#THIRD_COLOR = "#111111"        # Dark grey/black
#THIRD_COLOR = "#E0DFCB"

THIRD_COLOR = "#62606A"
HOVER_EFFECT_COLOR = "#58565F"

BUTTON_COLOR = "#0E0E0E"
BOX_COLOR = "#111111"
SECOND_BOX_COLOR = "#454545"
BUTTON_FONT = "Arial Bold"
BUTTON_FONT_BOLD = "Arial Bold"

MAIN_TEXT_COLOR = "white"
SECONDARY_TEXT_COLOR = "#D51989" # Pink
ACCENT_TEXT_COLOR = "#00FDFB"    # Cyan


MAIN_PANEL_RADIUS = 20

COMMON_PADDING = {
    "padx": 10,
    "pady": 10
}

GENERIC_BUTTON_LAYOUT = {
    "hover_color": "grey",
    "fg_color": "transparent",
    "font": (BUTTON_FONT, 16),
}


# DELETE LATER
USERNAME_TITLE_LAYOUT = {
    "fg_color": BOX_COLOR,
    "font": (BUTTON_FONT_BOLD, 16),
    "corner_radius": MAIN_PANEL_RADIUS
}


VALID_PACK_PARAMS = ["side", "fill", "expand", "anchor", "ipadx", "ipady", "padx", "pady"]
VALID_GRID_PARAMS = ["column", "row", "rowspan", "columnspan"]


### ROOT WINDOW ###
#WINDOW_BACKGROUND_COLOR = "#44424a"
WINDOW_BACKGROUND_COLOR = "#1E1F22"


### MAIN MENU ###
MAIN_MENU_COLOR = "black"

MAIN_MENU_FRAME_LAYOUT = {
    "fg_color": "transparent"
}

FEATURED_APP_FRAME_LAYOUT = {
    "corner_radius": MAIN_PANEL_RADIUS,
    "fg_color": MAIN_MENU_COLOR
}

APP_SELECTOR_WINDOW_FRAME_LAYOUT = {
    "corner_radius": MAIN_PANEL_RADIUS,
    "fg_color": "transparent"
}

APP_SELECTED_INFORMATION_FRAME_LAYOUT = {
    "corner_radius": MAIN_PANEL_RADIUS,
    "fg_color": MAIN_MENU_COLOR
}

WEATHER_FRAME_LAYOUT = {
    "corner_radius": MAIN_PANEL_RADIUS,
    "fg_color": MAIN_MENU_COLOR
}

GAME_ICON_LAYOUT = {
    "corner_radius": MAIN_PANEL_RADIUS,
    "fg_color": MAIN_MENU_COLOR,
    "hover_color": "grey"
}



### SIDEBAR ###
SIDEBAR_COLOR = "#111111"
SIDEBAR_SUB_COLOR = SECONDARY_COLOR

SIDEBAR_BUTTON_LAYOUT = {
    "hover_color": "grey",
    "fg_color": "transparent",
    "font": (BUTTON_FONT, 16),
}

SIDEBAR_PANEL_LAYOUT = {
    "border_width": 0,
    "corner_radius": MAIN_PANEL_RADIUS,
    "fg_color": SIDEBAR_COLOR,
    "border_color": "#303030",
    "bg_color": "transparent"
}

PLAY_CIRCLE_ICON = customtkinter.CTkImage(Image.open("ApplicationUI/Assets/Icons/play-circle.png"))
PACKAGE_ICON = customtkinter.CTkImage(Image.open("ApplicationUI/Assets/Icons/package (1).png"))
HELP_CIRCLE_ICON = customtkinter.CTkImage(Image.open("ApplicationUI/Assets/Icons/help-circle (1).png"))
SETTINGS_ICON = customtkinter.CTkImage(Image.open("ApplicationUI/Assets/Icons/settings.png"))
LOG_OUT_ICON = customtkinter.CTkImage(Image.open("ApplicationUI/Assets/Icons/log-out (1).png"))
POWER_ICON = customtkinter.CTkImage(Image.open("ApplicationUI/Assets/Icons/power.png"))


### LOGIN BOX ###
LOGIN_PRIMARY_COLOR = "black"          #Black
LOGIN_SECONDARY_COLOR = "#D51989"      #Pink
LOGIN_HOVER_COLOR = "#980E87"          #Dark Pink
CREATE_ACCOUNT_HOVER_COLOR = "#D51989" #Darker pink
LOGIN_BUTTON_PRESS_COLOR = "#05EAEB"   #Neon blue

LOGIN_FRAME_LAYOUT = {
    "fg_color": LOGIN_PRIMARY_COLOR,
    "bg_color": LOGIN_SECONDARY_COLOR,
    "corner_radius": 2,
    "border_color": LOGIN_SECONDARY_COLOR,
    "border_width": 3
}

LOGIN_TITLE_TEXT_LAYOUT = {
    "text_color": LOGIN_SECONDARY_COLOR,
    "font": ("Impact", 26)
}

ENTRY_FIELD_LAYOUT = {
    "border_color": "black",
    "bg_color": "black",
    "corner_radius": 0
}

LOGIN_BUTTON_LAYOUT = {
    "fg_color": LOGIN_SECONDARY_COLOR,
    "bg_color": LOGIN_PRIMARY_COLOR,
    "corner_radius": MAIN_PANEL_RADIUS,
    "hover_color": LOGIN_HOVER_COLOR,
    "text_color": LOGIN_PRIMARY_COLOR,
    "font": ("Roboto", 15, "bold")
}


### TIC-TAC-TOE ###
TTT_BOARD_LINE_COLOR = "grey"
TTT_BOARD_COLOR = "black"
TTT_BUTTON_COLOR = "#282828"
TTT_SUB_COLOR = "#282828"

TTT_BOARD_BACKGROUND_LAYOUT = {
    "corner_radius": MAIN_PANEL_RADIUS,
    "border_width": 1,
    "fg_color": TTT_BOARD_COLOR,
    "bg_color": "transparent"
}

TTT_GAMEBOARD_LAYOUT = {
    "fg_color": TTT_BOARD_COLOR,
    "border_width": 2,
    "corner_radius": MAIN_PANEL_RADIUS,
    "border_color": TTT_BOARD_LINE_COLOR
}

TTT_RIGHT_PANEL_LAYOUT = {
    "corner_radius": MAIN_PANEL_RADIUS,
    "border_width": 1,
    "fg_color": TTT_BOARD_COLOR,
    "width": 250
}

TTT_RIGHT_PANEL_SUB_BOX_LAYOUT = {
    "corner_radius": MAIN_PANEL_RADIUS,
    "border_width": 1,
    "fg_color": TTT_SUB_COLOR,
    "height": 20,
    "width": 250,
    "bg_color": "transparent"
}




##############################################
########## END OF COMPONENT STYLING ##########
##############################################