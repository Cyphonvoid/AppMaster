import customtkinter
import threading
import time


class SudokuTimer:
    def __init__(self, parent, **arguments):

        self.parent = parent
        self.arguments = {**arguments}
        self._placement_manager = None

        self.FRAME_LAYOUT = {
            "bg_color": "transparent",
            "fg_color": "transparent",
            "width": 75
        }

        self.TIME_DISPLAYER_LAYOUT = {
            "bg_color": "transparent",
            "fg_color": "transparent",
            "text_color": "grey",
            "font": ("Arial", 15, "bold"),
            "text": "00:00"
        }

        self.frame = customtkinter.CTkFrame(master=self.parent, **self.FRAME_LAYOUT)
        self.dynamic_layout(self.frame, self.arguments)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.current = 0
        self.minutes = 0
        self.seconds = 0
        self.limit = 0
        self.timer_state = "stop"
        print("height", self.frame.winfo_height())

        self.time_displayer = customtkinter.CTkLabel(master=self.frame, **self.TIME_DISPLAYER_LAYOUT)
        self.time_displayer.grid(row=0, column=0)

        self.timer_thread = None
        self.thread = "resume"

    def __del__(self):
        self.stop()


    def start(self):
        self.thread = "resume"
        self.timer_thread = threading.Thread(target=self.start_timer_thread)
        self.timer_thread.start()

    def start_timer_thread(self):
        if self.thread == "exit":
            return

        total_seconds = 0
        if isinstance(self.limit, float):
            minutes = int(self.limit)
            seconds = self.limit - minutes

            total_seconds = (minutes * 60) + seconds

        elif isinstance(self.limit, int):
            total_seconds = self.limit * 60


        for seconds in range(0, total_seconds + 1):
            try:
                pass
            except Exception:
                return
            if self.thread == "exit":
                return

            if self.seconds % 60 == 0 and seconds > 0:
                self.minutes += 1
                self.seconds = 0

            if self.seconds < 10:
                str_sec = "0" + str(self.seconds)
            else:
                str_sec = "" + str(self.seconds)
            if self.minutes < 10:
                str_min = "0" + str(self.minutes)
            else:
                str_min = "" + str(self.minutes)
            self.time_displayer.configure(text=str_min + ":" + str_sec)

            time.sleep(1)
            self.seconds += 1

        self.stop()
        return


    def stop(self):
        self.thread = "exit"
        self.timer_state = "stop"

    def reset(self):
        self.minutes = 0
        self.seconds = 0
        self.time_displayer.configure(text="00" + ":" + "00")

    def set_time(self, minutes):
        self.limit = minutes


    def get_time(self):
        return self.minutes, self.seconds

    def dynamic_layout(self, obj, args, prefer=None):

        if prefer == "pack":
            obj.pack(**args)
            obj.pack_propagate(False)
            self._placement_manager = "pack"



        elif prefer == "grid":
            obj.grid(**args)
            obj.grid_propagate(False)
            self._placement_manager = "grid"


        elif prefer == "place":
            obj.place(**args)
            self._placement_manager = "place"

        else:
            print("Arguments aren't matching up with layout or prefer = None")

        try:
            obj.grid(**args)
            obj.grid_propagate(False)
            self._placement_manager = "grid"
            return
        except Exception:
            pass

        try:
            obj.pack(**args)
            obj.pack_propagate(False)
            self._placement_manager = "pack"
            return
        except Exception:
            pass

        try:
            obj.place(**args)
            self._placement_manager = "place"
            return
        except Exception:
            pass

    def show(self):
        if self._placement_manager == "grid":
            self.frame.grid(**self.arguments)
            self.frame.grid_propagate(False)

        elif self._placement_manager == "pack":
            self.frame.pack(**self.arguments)
            self.frame.pack_propagate(False)

        elif self._placement_manager == "place":
            self.frame.place(**self.arguments)


    def hide(self):
        if self._placement_manager == "grid":
            self.frame.grid_forget()
        elif self._placement_manager == "pack":
            self.frame.pack_forget()
        elif self._placement_manager == "place":
            self.frame.place_forget()