import customtkinter 
from .DesignStyles import *


#All the utility functions that are needed as tools for anything
def add_button_via_pack(parent, **button_arguments):
    valid_pack_arguments = {key: value for key, value in button_arguments.items() if key in VALID_PACK_PARAMS}
    valid_button_arguments = {key: value for key, value in button_arguments.items() if not key in VALID_PACK_PARAMS}
    new_button = customtkinter.CTkButton(parent, **valid_button_arguments)
    new_button.pack(**valid_pack_arguments)
    return new_button


def add_label_via_pack(parent, **button_arguments):
    valid_pack_arguments = {key: value for key, value in button_arguments.items() if key in VALID_PACK_PARAMS}
    valid_button_arguments = {key: value for key, value in button_arguments.items() if not key in VALID_PACK_PARAMS}
    new_button = customtkinter.CTkLabel(parent, **valid_button_arguments)
    new_button.pack(**valid_pack_arguments)
    return new_button

def add_button_via_grid(parent, **button_arguments):
    valid_grid_arguments = {key: value for key, value in button_arguments.items() if key in VALID_PACK_PARAMS}
    valid_button_arguments = {key: value for key, value in button_arguments.items() if not key in VALID_PACK_PARAMS}
    new_button = customtkinter.CTkButton(parent, **valid_button_arguments)
    new_button.grid(**valid_grid_arguments)
    return new_button

