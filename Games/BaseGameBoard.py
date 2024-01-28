import customtkinter
from PIL import ImageTk

DEFAULT_FRAME_LAYOUT = {
    "border_color": "grey",
    "border_width": 2,
    "corner_radius": 20
}

class BaseGameBoard:
    def __init__(self, parent, grid_size_num, background, line_thickness = 1, gap = 0, **arguments):
        # Frame to hold game + visualization
        self.game_frame = customtkinter.CTkFrame(parent, fg_color=background, **DEFAULT_FRAME_LAYOUT)
        self.game_frame.pack(**arguments)

        self.original_pack_arguments = arguments
        self.canvas = customtkinter.CTkCanvas(self.game_frame, background=background, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.parent = parent
        self.grid_size_num = grid_size_num
        self.canvas_width = None
        self.canvas_height = None
        self.box_width = None
        self.box_height = None
        self.previous_size = None
        self.game_frame_previous_size = None
        self.GRID_SIZE = grid_size_num
        self.resize_id = None

        self.thickness = line_thickness
        self.gap = gap

        self.num_symbols = 0

        self.board_state = False

        # Map keyword to symbol
        self.allowed_symbols = {}

        self.existing_symbol_locations = {}
        self.existing_canvas_locations = {}
        self.existing_symbols = []

        self.canvas_vertical_lines = []
        self.canvas_horizontal_lines = []

        # Updating size of symbols and widgets
        self.update_previous_size(self.parent.winfo_width())

        # Resizing window bindings
        self.canvas.bind("<Configure>", lambda event: self.draw_grid(self.thickness, self.gap))

        # Bind window resize event to adjust game_frame's size
        self.game_frame.bind("<Configure>", self.on_window_resize)

        self.game_flag = customtkinter.CTkLabel(parent, text="", fg_color="transparent", font=("arial", 1))

    def draw_grid(self, thickness, gap, event=None):
        self.canvas.delete("grid_line")  # Remove previously drawn lines
        self.canvas_vertical_lines.clear()
        self.canvas_horizontal_lines.clear()

        for i in range(self.grid_size_num):
            self.canvas_width = self.canvas.winfo_width()
            self.canvas_height = self.canvas.winfo_height()
            self.box_width = self.canvas_width // self.grid_size_num
            self.box_height = self.canvas_height // self.grid_size_num

            x = i * self.box_width
            y = i * self.box_height

            horizontal_line = None
            vertical_line = None

            # Draw horizontal line
            if i != 0: horizontal_line = self.canvas.create_line(0, y, self.canvas_width, y, tags="grid_line", fill="grey")
            # Draw vertical line
            if i != 0: vertical_line = self.canvas.create_line(x, 0, x, self.canvas_height, tags="grid_line", fill="grey")

            if gap > 0:
                self.canvas_horizontal_lines.append(horizontal_line)
                self.canvas_vertical_lines.append(vertical_line)

        if gap == 0:
            return

        for index in range(gap, len(self.canvas_vertical_lines), gap):
            self.canvas.itemconfig(self.canvas_vertical_lines[index], width=thickness)

        for index in range(gap, len(self.canvas_horizontal_lines), gap):
            self.canvas.itemconfig(self.canvas_horizontal_lines[index], width=thickness)



    def update_previous_size(self, new_size):
        self.game_frame_previous_size = new_size



    def on_window_resize(self, event):
        # Get the current size of the main_frame
        width = self.parent.winfo_width()
        height = self.parent.winfo_height()

        # Calculate the maximum square size
        size = min(width - 20, height - 20)

        #print("width: ", width)
        #print("height: ", height)

        # No need to adjust size if unnecessary
        if size == self.previous_size:
            return

        #print("size: ", size)
        #print("previous: ", size)
        #print()

        # Update the game_frame's size
        self.game_frame.configure(width=size, height=size)
        self.canvas.configure(width=size, height=size)
        self.update_size_info()
        self.update_previous_size(size)

        # Do not redraw symbols if there is an existing id (Prevent lag)
        if self.resize_id:
            self.canvas.after_cancel(self.resize_id)

        # Redraw symbols after window inactivity
        self.canvas.delete("symbol")
        self.resize_id = self.canvas.after(350, self.redraw_symbols)

    def redraw_symbols(self):
        # Reset resize id for proper window inactivity
        self.resize_id = None
        self.existing_canvas_locations.clear()

        for location, symbol_image in self.existing_symbol_locations.items():
            self.insert_symbol(location[0], location[1], symbol_image)

    def insert_symbol(self, grid_x, grid_y, symbol=None):
        """
        :param grid_x: integer
        :param grid_y: integer
        :param symbol: Image or String
        :return: None
        """
        if (grid_x, grid_y) in self.existing_symbol_locations and isinstance(symbol, str):
            print(f"Symbol {symbol} already exists at x: {grid_x}, y: {grid_y}")
            return

        center_x = (grid_x * self.box_width) + self.box_width // 2
        center_y = (grid_y * self.box_height) + self.box_height // 2

        if isinstance(symbol, str):
            symbol_image = self.allowed_symbols[symbol].copy()
        else:
            symbol_image = symbol

        symbol_image = symbol_image.resize((self.box_height - 25, self.box_width - 25))

        formatted_image = ImageTk.PhotoImage(image=symbol_image)
        self.existing_symbols.append(formatted_image)

        # Using list indexing for image because it doesn't work when using formatted_image directly
        obj = self.canvas.create_image(center_x, center_y, image=self.existing_symbols[-1], anchor="center", tags="symbol")

        self.existing_symbol_locations[(grid_x, grid_y)] = symbol_image
        self.existing_canvas_locations[(grid_x, grid_y)] = obj
        self.num_symbols += 1





    def update_size_info(self):
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.box_width = self.canvas_width // self.grid_size_num
        self.box_height = self.canvas_height // self.grid_size_num


    def update_symbol(self, symbol_name, image_file_path):
        self.allowed_symbols[symbol_name] = image_file_path


    def remove_symbol(self, grid_x, grid_y, symbol=None):
        if (grid_x, grid_y) not in self.existing_canvas_locations:
            print(f"Symbol {symbol} does not exist at x: {grid_x}, y: {grid_y}")
            return

        self.num_symbols -= 1
        self.canvas.delete(self.existing_canvas_locations[(grid_x, grid_y)])

        # Clearing key-value pair from dictionary
        del self.existing_canvas_locations[(grid_x, grid_y)]
        del self.existing_symbol_locations[(grid_x, grid_y)]


    def raise_game_flag(self):
        self.game_flag.pack()

    def lower_game_flag(self):
        self.game_flag.pack_forget()

    def get_game_flag(self):
        return self.game_flag

    def flip_state(self, state: bool):
        if not isinstance(state, bool):
            raise TypeError("State must be boolean")
        self.board_state = state

    def get_default_object(self):
        return self.game_frame

    def get_game_board(self):
        return self.game_frame

    def get_game_canvas(self):
        return self.canvas

    def get_state(self):
        return self.board_state

    def reset_board(self):
        self.num_symbols = 0
        self.existing_symbols.clear()
        self.existing_symbol_locations.clear()
        self.canvas.delete("symbol")

    def enable(self):
        self.canvas.grid(**self.original_pack_arguments)

    def disable(self):
        self.canvas.grid_forget()