# CUSTOM PACKAGES IMPORTS
from System import *
from .DesignStyles import *
from PIL import Image
import json
import importlib

class GameSelector(ComponentManager):
    CLASS_OBJECT_ID = 12931

    @staticmethod
    def assign_classlevel_id():
        GameSelector.CLASS_OBJECT_ID += 2
        return GameSelector.CLASS_OBJECT_ID

    def __init__(self, parent, **grid_arguments):
        ComponentManager.__init__(self)
        self.set_classname("GameSelector1234")
        self.original_grid_arguments = {**grid_arguments}
        self.parent = parent

        # Store icons
        self.game_icons = []
        self.filepaths = {}

        # Json declaration here
        self.download_file = open("Downloads/AppDownloads.json", "r")
        self.app_json_filepaths = json.load(self.download_file)
        self.download_file.close()

        # Icon-related variables
        self.number_of_games = 0
        self.max_games_per_row = 2
        self.current_column_number = 0
        self.current_row_number = 0
        self.game_selected = customtkinter.StringVar()
        self.game_description = {}

        self.button_size = (150, 80)

        # ************************************* NEW NEW NEW**************************

        # NOTE: Programmable socket declaration, just an object that stores commands
        self.socketGS = Socket()
        # ****************************************************************************

        # Setup main page frame
        self.main_frame = customtkinter.CTkFrame(parent, **MAIN_MENU_FRAME_LAYOUT)
        self.main_frame.columnconfigure((0, 2, 4), weight=1)
        self.main_frame.columnconfigure((1, 3), weight=2)
        self.main_frame.rowconfigure((0, 1), weight=1)
        self.main_frame.grid(**grid_arguments)
        self.max_column_span = 4
        self.max_row_span = 4
        self.main_frame.grid_propagate(False)

        # Responsive layout variables
        self.main_frame.bind("<Configure>", self.responsive_layout)
        self.layout_states = {
            "small": "small",
            "medium": "medium",
            "large": "large"
        }
        self.current_state = None

        ######## DEFAULT WIDGETS ########
        # Featured Game Panel - TOP-LEFT
        self.featured_game_frame = customtkinter.CTkFrame(self.main_frame, **FEATURED_APP_FRAME_LAYOUT)
        self.featured_box_frame = customtkinter.CTkFrame(self.featured_game_frame, fg_color=BACKGROUND_COLOR, corner_radius=15)
        self.featured_text = customtkinter.CTkLabel(self.featured_box_frame, fg_color="transparent", text="Featured", text_color=SECONDARY_TEXT_COLOR, font=("Arial", 17))
        self.featured_game_text = customtkinter.CTkLabel(self.featured_game_frame, text="TIC-TAC-TOE", fg_color="transparent", text_color=MAIN_TEXT_COLOR, font=("Arial", 37))

        self.featured_game_text.pack(anchor="w", side="bottom", **COMMON_PADDING)
        self.featured_box_frame.pack(anchor="w", side="bottom", **COMMON_PADDING, ipadx=7, ipady=7)
        self.featured_text.pack(expand=True)

        # Library Panel - TOP-RIGHT
        self.box_frame = customtkinter.CTkScrollableFrame(self.main_frame, **APP_SELECTOR_WINDOW_FRAME_LAYOUT)
        for new_column in range(self.max_games_per_row):
            self.box_frame.grid_columnconfigure(new_column, weight=1)

        # Weather panel - BOTTOM-LEFT
        self.weather_frame = customtkinter.CTkFrame(self.main_frame, **WEATHER_FRAME_LAYOUT)

        # Game Information Panel - BOTTOM-RIGHT
        self.description_box_frame = customtkinter.CTkFrame(self.main_frame, **APP_SELECTED_INFORMATION_FRAME_LAYOUT)
        self.description_box_frame.pack_propagate(False)

        # Additional Panel for Large Sizes
        self.additional_box_frame = customtkinter.CTkFrame(self.main_frame, **APP_SELECTED_INFORMATION_FRAME_LAYOUT)

        self.text_frame = customtkinter.CTkFrame(self.description_box_frame, fg_color=MAIN_MENU_COLOR)
        self.game_label = customtkinter.CTkLabel(self.text_frame, text="", textvariable=self.game_selected, font=(BUTTON_FONT, 28))
        self.game_label.pack(side="left", padx=20, pady=20)
        self.text_frame.pack(fill="x")

        self.description_text = customtkinter.CTkTextbox(self.description_box_frame, fg_color=MAIN_MENU_COLOR, text_color="white", font=(BUTTON_FONT, 20), wrap="word")
        self.description_text.pack(**COMMON_PADDING, fill="x")
        self.description_text.configure(state="disabled")

        self.play_button = customtkinter.CTkButton(self.description_box_frame, text="PLAY", fg_color=MAIN_MENU_COLOR, font=(BUTTON_FONT_BOLD, 20), command=self.display_selected_game)
        self.play_button.pack(**COMMON_PADDING, side="bottom", anchor="se")

        self.get_apps()

    def enable_small_layout(self):
        if self.current_state == self.layout_states["small"]:
            return
        self.clear_widgets()

        self.button_size = (200, 100)
        self.update_button_sizes(self.button_size)

        self.box_frame.grid(column=0, row=0, columnspan=self.max_column_span, sticky="nsew", padx=10)
        self.redisplay_all_buttons()

        self.description_box_frame.grid(column=0, row=1, columnspan=self.max_column_span, sticky="nsew", **COMMON_PADDING)

    def enable_medium_layout(self):
        if self.current_state == self.layout_states["medium"]:
            return
        self.clear_widgets()

        self.button_size = (150, 80)

        self.featured_game_frame.grid(column=0, row=0, columnspan=4, sticky="nsew", pady=10)

        self.box_frame.grid(column=4, row=0, columnspan=2, sticky="nsew", padx=10)
        self.redisplay_all_buttons()

        self.weather_frame.grid(column=0, row=1, columnspan=2, sticky="nsew", **COMMON_PADDING)
        self.description_box_frame.grid(column=2, row=1, columnspan=3, sticky="nsew", **COMMON_PADDING)

    def enable_large_layout(self):
        if self.current_state == self.layout_states["large"]:
            return
        self.clear_widgets()

        self.button_size = (200, 90)

        self.featured_game_frame.grid(column=0, row=0, columnspan=3, sticky="nsew", pady=10, padx=(0, 10))
        self.additional_box_frame.grid(column=3, row=0, sticky="nsew", pady=10, padx=(10, 0))
        self.box_frame.grid(column=4, row=0, sticky="nsew", padx=10)
        self.redisplay_all_buttons()
        self.weather_frame.grid(column=0, row=1, columnspan=2, sticky="nsew", **COMMON_PADDING)
        self.description_box_frame.grid(column=2, row=1, columnspan=3, sticky="nsew", **COMMON_PADDING)

    def responsive_layout(self, event):
        largest_breaking_point = 1200
        mid_breaking_point = 700

        width = event.width

        if width >= largest_breaking_point:
            self.enable_large_layout()
            self.current_state = self.layout_states["large"]

        elif width >= mid_breaking_point:
            self.enable_medium_layout()
            self.current_state = self.layout_states["medium"]

        else:
            self.enable_small_layout()
            self.current_state = self.layout_states["small"]

    # Dynamic icon adding, only needs name_of_game, icon_image, and description of game via string
    def add_icon_button(self, name_of_game, game_description, icon_image=None):
        # icon_image = customtkinter.CTkImage(Image.open("ApplicationUI/Assets/Icon.png"), size=self.button_size)
        button = customtkinter.CTkButton(self.box_frame, image=icon_image, text="", **GAME_ICON_LAYOUT, command=lambda: self.button_selected(button, name_of_game))

        self.game_description[name_of_game] = game_description
        self.display_button(button)
        self.game_icons.append(button)

    def update_button_sizes(self, size):
        for button in self.game_icons:
            button.configure(width=size[0], height=size[1])

    # Dictionaries retrieval functions are either .keys(), .values(), or .items()
    def get_apps(self):
        for key, value in self.app_json_filepaths["downloads"].items():
            game_name = key
            game_description = value["description"]
            self.filepaths[game_name] = value["path"]
            self.add_icon_button(game_name, game_description, icon_image=None)

    def display_button(self, button):
        # Find appropriate location
        if self.number_of_games % self.max_games_per_row == 0 and self.number_of_games != 0:
            self.current_row_number += 1
        if self.number_of_games != 0:
            self.current_column_number += 1

        grid_size = self.box_frame.grid_size()

        if grid_size[0] != 0:
            column = self.current_column_number % grid_size[0]
        else:
            column = 0

        button.configure(width=self.button_size[0], height=self.button_size[1])
        button.grid(row=self.current_row_number, column=column, pady=5, padx=4)

        self.number_of_games += 1

    def redisplay_all_buttons(self):
        self.current_row_number = 0
        self.current_column_number = 0
        self.number_of_games = 0
        for button in self.game_icons:
            button.grid_forget()
        for button in self.game_icons:
            self.display_button(button)

    def button_selected(self, button, name_of_game):
        self.game_selected.set(name_of_game)

        for index in self.game_icons:
            index.configure(fg_color=GAME_ICON_LAYOUT["fg_color"])
            index.configure(hover_color=GAME_ICON_LAYOUT["hover_color"])

        button.configure(fg_color="white")
        button.configure(hover_color="white")

        self.description_text.configure(state="normal")
        self.description_text.delete("0.0", "end")
        self.description_text.insert("0.0", self.game_description[name_of_game])

    def clear_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.grid_forget()

    def display_selected_game(self):
        if self.game_selected.get() == "":
            print("No game selected")
            return

        filepath = self.filepaths[self.game_selected.get()]

        try:
            #Updated __import__ to import_module, appearently using __import__ is bad practice, functionality is the same
            app_module = importlib.import_module(filepath)

            if hasattr(app_module, "launch"):
                app_module.launch(self.parent)
            else:
                print("Launch function not found in specific module.")
                
        except ImportError:
            print("Error importing module:", filepath)

        except Exception as e:
            print("Error launching app:", e)

        self.disable()

    # Overloaded enable function from component manager
    def enable(self):
        self.main_frame.grid(**self.original_grid_arguments)

    # Overloaded disable function from component manager
    def disable(self):
        self.main_frame.grid_forget()

    # Requests
    def handle_request(self, message, extra=None):
        if message == "enable":
            self.enable() 

        elif message == "disable":
            self.disable()