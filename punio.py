__author__ = 'cristian'
from tkinter import *
import json
import serial
import time
from threading import Timer
from dialog import LayoutDialog
import configparser
from struct import unpack
import logging
import pyautogui
import os.path

try:
    import enum
except ImportError:
    import enum34 as enum

char_to_DGTXL = {
    '0': 0x01 | 0x02 | 0x20 | 0x08 | 0x04 | 0x10, '1': 0x02 | 0x04, '2': 0x01 | 0x40 | 0x08 | 0x02 | 0x10,
    '3': 0x01 | 0x40 | 0x08 | 0x02 | 0x04, '4': 0x20 | 0x04 | 0x40 | 0x02, '5': 0x01 | 0x40 | 0x08 | 0x20 | 0x04,
    '6': 0x01 | 0x40 | 0x08 | 0x20 | 0x04 | 0x10, '7': 0x02 | 0x04 | 0x01,
    '8': 0x01 | 0x02 | 0x20 | 0x40 | 0x04 | 0x10 | 0x08, '9': 0x01 | 0x40 | 0x08 | 0x02 | 0x04 | 0x20,
    'a': 0x01 | 0x02 | 0x20 | 0x40 | 0x04 | 0x10, 'b': 0x20 | 0x04 | 0x40 | 0x08 | 0x10, 'c': 0x01 | 0x20 | 0x10 | 0x08,
    'd': 0x10 | 0x40 | 0x08 | 0x02 | 0x04, 'e': 0x01 | 0x40 | 0x08 | 0x20 | 0x10, 'f': 0x01 | 0x40 | 0x20 | 0x10,
    'g': 0x01 | 0x20 | 0x10 | 0x08 | 0x04, 'h': 0x20 | 0x10 | 0x04 | 0x40, 'i': 0x02 | 0x04,
    'j': 0x02 | 0x04 | 0x08 | 0x10, 'k': 0x01 | 0x20 | 0x40 | 0x04 | 0x10, 'l': 0x20 | 0x10 | 0x08,
    'm': 0x01 | 0x40 | 0x04 | 0x10, 'n': 0x40 | 0x04 | 0x10, 'o': 0x40 | 0x04 | 0x10 | 0x08,
    'p': 0x01 | 0x40 | 0x20 | 0x10 | 0x02, 'q': 0x01 | 0x40 | 0x20 | 0x04 | 0x02, 'r': 0x40 | 0x10,
    's': 0x01 | 0x40 | 0x08 | 0x20 | 0x04, 't': 0x20 | 0x10 | 0x08 | 0x40, 'u': 0x08 | 0x02 | 0x20 | 0x04 | 0x10,
    'v': 0x08 | 0x02 | 0x20, 'w': 0x40 | 0x08 | 0x20 | 0x02, 'x': 0x20 | 0x10 | 0x04 | 0x40 | 0x02,
    'y': 0x20 | 0x08 | 0x04 | 0x40 | 0x02, 'z': 0x01 | 0x40 | 0x08 | 0x02 | 0x10, ' ': 0x00, '-': 0x40,
    '/': 0x20 | 0x40 | 0x04, '|': 0x20 | 0x10 | 0x02 | 0x04, '\\': 0x02 | 0x40 | 0x10
}


class ExampleApp(Tk):
    class Square():
        def __init__(self, name, center, square_id, reversed_id):
            self.name = name
            self.center = center
            self.square_id = square_id
            self.reversed_id = reversed_id

    def __init__(self):
        Tk.__init__(self)
        config = configparser.ConfigParser()

        if not os.path.isfile('config.ini'):
            config_file = open("config.ini", 'w+')
            config.add_section('BoardLayouts')
            config.add_section('DGT')
            config.set('DGT', 'port', 'enter the port here')
            config.write(config_file)
            config_file.close()

        config.read("config.ini")

        self.incoming_board_thread = Timer(0, self.get_board_msg_loop)
        self.dgt_port = StringVar()
        self.dgt_port.set(config.get('DGT', 'port'))
        self.serial = None
        self.x = self.y = 0
        self.board_started = False

        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """ BOARD VARIABLES """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        self.allow_draw = False
        self.board_columns = [{'name': 'a', 'xpos': 0},
                              {'name': 'b', 'xpos': 1},
                              {'name': 'c', 'xpos': 2},
                              {'name': 'd', 'xpos': 3},
                              {'name': 'e', 'xpos': 4},
                              {'name': 'f', 'xpos': 5},
                              {'name': 'g', 'xpos': 6},
                              {'name': 'h', 'xpos': 7}]

        self.board_rows = [{'name': '1', 'ypos': 7},
                           {'name': '2', 'ypos': 6},
                           {'name': '3', 'ypos': 5},
                           {'name': '4', 'ypos': 4},
                           {'name': '5', 'ypos': 3},
                           {'name': '6', 'ypos': 2},
                           {'name': '7', 'ypos': 1},
                           {'name': '8', 'ypos': 0}]

        self.flipped = BooleanVar()
        self.flipped.set(False)
        self.board_squares = []
        self.canvas_objs = []

        self.test_click_shown = False
        self.test_click_squares = []

        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """ MAIN CANVAS """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        self.canvas = Canvas(self)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """ TOP FRAME (TOOLBARS) """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        top_frame = Frame(self.canvas, bd=1, relief=RAISED)
        top_frame.pack(side=TOP, anchor=W, fill=X)
        top_frame.columnconfigure(0)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2)
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """ MAIN TOOLBAR """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """ BOARD CONFIG FRAME """
        self.toolbar = Frame(top_frame, bd=1, relief=RAISED)
        self.toolbar.grid(column=0, row=1)

        self.cfg_buttons = LabelFrame(self.toolbar, text="Config", padx=10, pady=7)
        self.cfg_buttons.grid(column=0, row=0)

        self.configure_button = Button(self.cfg_buttons,
                                       text='New Board Layout',
                                       command=self.on_config_button_click)
        self.configure_button.grid(column=0, row=0)

        self.saved_layouts = None
        self.reload_layout_menu()

        self.save_current_layout_button = Button(self.cfg_buttons,
                                                 text='Save Current Layout',
                                                 command=self.on_save_board_layout)
        self.save_current_layout_button.grid(column=2, row=0)

        self.test_squares_button = Button(self.cfg_buttons,
                                          text='Test Click Squares',
                                          command=self.on_test_squares)
        self.test_squares_button.grid(column=3, row=0)

        Label(self.cfg_buttons, text='Port Number: ').grid(column=4, row=0)
        self.port_text = Entry(self.cfg_buttons, textvariable=self.dgt_port)
        self.port_text.grid(column=5, row=0)

        Button(self.cfg_buttons, text='Save', command=self.on_save_port).grid(column=6, row=0)

        """ DGT ACTIONS FRAME """
        self.dgt_buttons = LabelFrame(self.toolbar, text="DGT Actions", padx=10, pady=10)
        self.dgt_buttons.grid(column=2, row=0)

        self.flip_button = Button(self.dgt_buttons,
                                  text='Flip Board',
                                  relief="raised",
                                  command=self.on_flip_clicked)
        self.flip_button.grid(column=0, row=0)

        sep = Label(self.dgt_buttons, text=' ')
        sep.grid(column=1, row=0)

        self.start_button = Button(self.dgt_buttons,
                                   text='Start',
                                   command=self.on_start_board)
        self.start_button.grid(column=2, row=0)

        self.stop_button = Button(self.dgt_buttons,
                                  text='Stop',
                                  command=self.on_stop_board)
        self.stop_button.grid(column=3, row=0)

        """ OTHER BUTTONS """
        self.other_buttons = LabelFrame(self.toolbar, text="Extras", padx=10, pady=10)
        self.other_buttons.grid(column=3, row=0)

        self.quit_button = Button(self.other_buttons,
                                  text='Quit',
                                  command=on_closing)
        self.quit_button.grid(column=0, row=0)

        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """ GRID SETUP TOOLBAR """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        self.grid_setup_toolbar = Frame(top_frame, bd=1, relief=RAISED)

        self.draw_grid_commands = Frame(self.grid_setup_toolbar, bd=0)
        self.draw_grid_commands.pack(fill=X)

        self.done_button = Button(self.draw_grid_commands,
                                  text='Done',
                                  command=self.on_done_button_click)
        self.done_button.grid(column=0, row=0)
        self.undo_button = Button(self.draw_grid_commands,
                                  text='Undo',
                                  command=self.on_undo_clicked)
        self.undo_button.grid(column=1, row=0)

        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """ STATUS BAR """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        status_bar = Frame(self.canvas, bd=1, relief=RAISED)
        status_bar.pack(side=BOTTOM, anchor=W, fill=X)
        self.msg = StringVar()
        board_output_label = Label(status_bar, textvariable=self.msg, bd=1, relief=SUNKEN, anchor=W)
        board_output_label.pack(fill=X)
        self.msg.set('Nothing to say')

    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    """ MOUSE EVENTS """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    def on_button_press(self, event):
        if not self.allow_draw:
            return

        self.x = event.x
        self.y = event.y

    def on_button_release(self, event):
        if not self.allow_draw:
            return

        x0, y0 = (self.x, self.y)
        x1, y1 = (event.x, event.y)
        self.draw_board(x0, y0, x1, y1)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    """ BUTTONS EVENTS """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    def on_save_port(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        config.set('DGT', 'port', self.dgt_port.get())
        cfgfile = open("config.ini", 'w+')
        config.write(cfgfile)
        cfgfile.close()

        self.msg.set('"{}" port saved'.format(self.dgt_port.get()))

    def on_test_squares(self):
        if not self.board_squares:
            self.msg.set('No layout selected!')
            return

        if self.test_click_shown:
            self.attributes('-alpha', 1)
            for obj in self.test_click_squares:
                self.canvas.delete(obj)
        else:
            self.attributes('-alpha', 0.5)
            for square in self.board_squares:
                self.test_click_squares.append(self.canvas.create_text(square['center'], text=square['name']))

        self.test_click_shown = not self.test_click_shown

    def on_flip_clicked(self):
        if self.flip_button.config('relief')[-1] == 'sunken':
            self.flip_button.config(relief="raised")
        else:
            self.flip_button.config(relief="sunken")
        self.flipped.set(not self.flipped.get())

    def on_save_board_layout(self):
        if not self.board_squares:
            self.msg.set('No layout selected!')
            return

        d = LayoutDialog(self)
        layout_name = d.result

        if layout_name:
            config = configparser.ConfigParser()
            config.read("config.ini")

            config.set('BoardLayouts', layout_name, json.dumps([x for x in self.board_squares]))

            cfgfile = open("config.ini", 'w+')
            config.write(cfgfile)
            cfgfile.close()

            self.msg.set('"{}" layout correctly saved'.format(layout_name))

        self.reload_layout_menu()

    def on_undo_clicked(self):
        self.reset_board()
        self.board_squares = []

    def on_config_button_click(self):
        self.reset_board()

        self.toolbar.grid_forget()
        self.attributes("-alpha", 0.5)
        self.allow_draw = True
        self.show_grid_commands()

    def on_done_button_click(self):

        self.attributes("-alpha", 1)
        self.allow_draw = False
        self.hide_grid_commands()
        self.toolbar.grid(column=0, row=1)

    def on_start_board(self):
        if not self.board_squares:
            self.msg.set('No layout selected!')
            return

        self.board_started = True
        self.init_dgt()
        self.msg.set('Board communication started')

    def on_stop_board(self):
        self.board_started = False
        self.msg.set('Board communication stopped')

    def on_layout_clicked(self, selected_item):
        config = configparser.ConfigParser()
        config.read("config.ini")
        selected_layout = config.get('BoardLayouts', selected_item)
        self.board_squares = json.loads(selected_layout)
        self.msg.set('"{}" layout loaded'.format(selected_item))

    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    """ FUNCTIONS """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    def reload_layout_menu(self):
        if self.saved_layouts:
            self.saved_layouts.grid_forget()

        layouts = self.load_board_layouts()
        self.current_layout = StringVar()
        if layouts:
            self.saved_layouts = OptionMenu(self.cfg_buttons,
                                            self.current_layout,
                                            *layouts,
                                            command=self.on_layout_clicked)
            self.saved_layouts.grid(column=1, row=0)

    def show_grid_commands(self):
        self.grid_setup_toolbar.grid(column=1, row=2)

    def hide_grid_commands(self):
        self.grid_setup_toolbar.grid_forget()

    def load_board_layouts(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config.options('BoardLayouts')

    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    """ DRAW BOARD """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""

    def draw_board(self, x0, y0, x1, y1):
        column_width = x1 - x0
        row_height = y1 - y0

        x_pos = 'xpos'
        y_pos = 'ypos'

        square_id = 0
        reversed_square_id = 63

        for y in range(0, 8):
            for x in range(0, 8):
                col_name = [col for col in self.board_columns if col[x_pos] == x]
                row_name = [row for row in self.board_rows if row[y_pos] == y]

                square_name = col_name[0]['name'] + row_name[0]['name']
                square_x0 = x0 + column_width * x
                square_y0 = y0 + row_height * y
                square_x1 = x1 + column_width * x
                square_y1 = y1 + row_height * y
                square_center = (square_x0 + column_width / 2,
                                 square_y0 + row_height)

                self.canvas_objs.append(self.canvas.create_rectangle(square_x0,
                                                                     square_y0,
                                                                     square_x1,
                                                                     square_y1,
                                                                     tags=square_name))

                self.board_squares.append(self.Square(name=square_name,
                                                      center=square_center,
                                                      square_id=square_id,
                                                      reversed_id=reversed_square_id).__dict__)
                square_id += 1
                reversed_square_id -= 1

    def reset_board(self):
        for obj in self.canvas_objs + self.test_click_squares:
            self.canvas.delete(obj)

        self.test_click_squares = []
        self.board_squares = []

    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    """ CLICK CLICK CLICK """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""

    def send_click_to_square(self, square_id):
        if not self.board_started:
            return

        if self.flipped.get():
            square_to_click = [x for x in self.board_squares if x['reversed_id'] == square_id]
        else:
            square_to_click = [x for x in self.board_squares if x['square_id'] == square_id]

        if square_to_click:
            square_to_click = square_to_click[0]
        else:
            self.msg.set('Unable to find square to click!')
            return

        x, y = square_to_click.get('center')

        try:
            self.msg.set('Trying to click on "{}"'.format(square_to_click['name']))
            time.sleep(0.01)
            pyautogui.mouseDown(x, y)
            time.sleep(0.01)
            pyautogui.mouseUp(x, y)
        except Exception as e:
            self.msg.set(str(e))

    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    """ DGT MANAGEMENT """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    def init_dgt(self):
        if self.serial or not self.dgt_port.get():
            return

        try:
            self.serial = serial.Serial(self.dgt_port.get(),
                                        stopbits=serial.STOPBITS_ONE,
                                        parity=serial.PARITY_NONE,
                                        bytesize=serial.EIGHTBITS,
                                        timeout=2)

            if not self.incoming_board_thread:
                self.incoming_board_thread = Timer(0, self.get_board_msg_loop)
            self.incoming_board_thread.start()

            self.write_board_command([0x4b])
            self.write_board_command([0x4d])
            self.write_board_command([0x52])

        except Exception as e:
            self.msg.set(str(e))

    def get_board_msg_loop(self):
        while True:
            try:
                c = None
                if self.serial:
                    c = self.serial.read(1)
                if c:
                    self.read_board_message(head=c)
                else:
                    time.sleep(0.1)
            except serial.SerialException:
                pass
            except TypeError:
                pass

    def process_board_message(self, message_id, message):
        if message_id == 142:
            self.send_click_to_square(message[0])  # Ask for the board when a piece moved

    def read_board_message(self, head=None):
        header_len = 3
        if head:
            header = head + self.serial.read(header_len - 1)
        else:
            header = self.serial.read(header_len)

        pattern = '>' + 'B' * header_len
        header = unpack(pattern, header)

        message_id = header[0]
        message_length = (header[1] << 7) + header[2] - 3

        if message_length:
            message = unpack('>' + str(message_length) + 'B', self.serial.read(message_length))
            self.process_board_message(message_id, message)
            return message_id

    def write_board_command(self, message):
        mes = message[3] if message[0] == 0x2b else message[0]
        logging.debug('->DGT board [%s], length %i', mes, len(message))

        array = []
        for v in message:
            if type(v) is int:
                array.append(v)
            elif isinstance(v, enum.Enum):
                array.append(v.value)
            elif type(v) is str:
                for c in v:
                    array.append(char_to_DGTXL[c.lower()])
            else:
                logging.error('Type not supported [%s]', type(v))

        while True:
            if not self.serial:
                self.setup_serial()
            try:
                self.serial.write(bytearray(array))
                break
            except ValueError:
                logging.error('Invalid bytes sent {0}'.format(message))
                break
            except serial.SerialException as e:
                logging.error(e)
                self.serial.close()
                self.serial = None
            except IOError as e:
                logging.error(e)
                self.serial.close()
                self.serial = None


""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""

def on_closing():
    app.destroy()


def is_number(char):
    try:
        int(char)
        return True
    except:
        return False

app = ExampleApp()
app.state('zoomed')
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()

