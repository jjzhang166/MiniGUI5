#
# Mini and Pseudo GUI based on command line (under Linux for now).
#
# Written by whuCanon, last modified on 2016/03/29.
#
# To use this module,you need meet the following condition: 
# 1.  Laptop computer;  (otherwise you need change the keyboardDevName)
# 2.  Running on root under Linux;
# 3.  X Window(simple window environment) on your system;
# 4.  Python >= 2.7;
# 5.  Installed evdev python lib.
#
# If you find bugs or have some good advises or questions, 
# please contact me at my github repository (https://github.com/whuCanon/MiniGUI).
#

'''A mini-GUI module which is based on terminal environment

This module provides a pseudo GUI on terminal. You can use this just as other
GUI which based on real screen. The only difference between them is the pixel
here is replaced by characters. But you can use different character on the pixel.

This module exports the following class and functions:
    Canvas:     The base class to draw a virtual screen onto display.
        draw_line:  Draw a string flatly or uprightly.
        draw_image: Draw a text image at virtual screen.
        update:     update the virtual screen onto display * times per second.
    Tablet:     A subclass of Canvas to draw text on large pattern.
        draw_text:  Draw a string on large pattern.
    setKeyHandler:  Set a keyboard event handler function thread.

Some public attributes:
    (Canvas)REFRESH_PERIOD:  The refresh period of the virtual screen.
    (Tablet)FONT_WIDTH:      The font width of large characters.
    (Tablet)FONT_HEIGHT:     The font height of large characters.
    (Tablet)dict:            The dictionary of char to large char.
    keyboardDevName:         The keyboard device's name on your system.

To use this module, firstly you need create a new Canvas(for painting),
or Tablet(for writting) as global variate.
For Canvas, you can use draw_line() to draw a string line to the virtual screen,
or you can use draw_image() to draw a text image to the virtual screen.
for Tablet, you can use draw_text() to draw a series of large character to the virtual screen.
After draw*(), you need to use update() to print your virtual screen to the real screen.

You should notice that the big character you can "draw_text()" are limited to the Tablet's dict.
Of course you can add your own big character to the dict, but remember don't be out of range.

'''

import os
import math
import time
import thread
from select import select
from evdev import ecodes
from evdev import InputDevice

keyboardDevName = "AT Translated Set 2 keyboard"

class Canvas:
    ''' The class of virtual screen. You must create a Canvas 
        or its subclass object with its width and height. 
        example: canvas = MiniGUI.Canvas(width, height) '''

    REFRESH_PERIOD = 0.05

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.tupMatrix = {}

    # print the virtual screen to real screen
    def draw(self):
        tmp_str = ""
        for y in range(self.height):
            tmp_str = ""
            for x in range(self.width):
                if self.tupMatrix.has_key((x, y)):
                    tmp_str += self.tupMatrix[(x, y)]
                else:
                    tmp_str += " "
            print tmp_str

    def draw_line(self, text, pos, isUpright = False):
        ''' 
        You can use this function to draw a string as a line 
        at any position uprightly or flatly. The position 
        example: canvas.draw_line("the text you want to print",
                 [position_x, position_y])
        '''
        cursor_pos = pos
        for ch in text:
            self.tupMatrix[tuple(cursor_pos)] = ch
            if isUpright:
                cursor_pos[1] += 1
            else:
                cursor_pos[0] += 1

    def draw_image(self, text, pos, angle = 0):
        '''
        You can use this function to draw a text image at any position.

        example: canvas.draw_image("the text of image in type matrix", pos,
                 rotation's_angle)
        '''
        image_dict = {}
        image_width = 0
        image_height = 0
        cursor_pos = [pos[0], pos[1]]
        tmp_width = 0
        for ch in text:
            if ch != '&' and ch != '\r' and ch != '\n':
                image_dict[tuple(cursor_pos)] = ch
                cursor_pos[0] += 1
                tmp_width += 1
            else:
                cursor_pos[1] += 1
                cursor_pos[0] = pos[0]
                image_height += 1
                if tmp_width > image_width:
                    image_width = tmp_width
                tmp_width = 0
        if angle != 0:
            self.rotate(image_dict, image_width, image_height, pos, angle)
        self.tupMatrix.update(image_dict)

    def rotate(self, image_dict, width, height, pos, angle):
        ''' rotate the image '''
        tmp_dict = {}
        tmp_dict.update(image_dict)
        o_pos = [pos[0] + width / 2, pos[1] + height / 2]
        for point in tmp_dict:
            o_x = point[0] - o_pos[0]
            o_y = point[1] - o_pos[1]
            o_x_ = round(o_x * math.cos(angle) - o_y * math.sin(angle))
            o_y_ = round(o_x * math.sin(angle) + o_y * math.cos(angle))
            del image_dict[point]
            image_dict[(o_x_ + o_pos[0], o_y_ + o_pos[1])] = tmp_dict[point]

    def clear(self):
        ''' clear the virtual screen per frame '''
        self.tupMatrix.clear()

    def update(self):
        ''' update and print the real screen '''
        tmp_dict = {}
        tmp_dict.update(self.tupMatrix)
        for key in tmp_dict:
            if key[0] < 0 or key[0] > self.width or key[1] < 0 or key[1] > self.height:
                del self.tupMatrix[key]
                self.tupMatrix[(key[0] % self.width, key[1] % self.height)] = tmp_dict[key]
        del tmp_dict
        for i in range(self.height):
            self.tupMatrix[(0, i)] = '|'
            self.tupMatrix[(self.width - 1), i] = '|'
        for i in range(self.width):
            self.tupMatrix[(i, 0)] = '='
            self.tupMatrix[(i, self.height - 1)] = '='
        os.system('clear')
        self.draw()
        self.clear()
        time.sleep(self.REFRESH_PERIOD)


class Tablet(Canvas):
    ''' usage: tablet = MiniGUI.Tablet(rows, columns) '''
    FONT_WIDTH = 9      # the max width of the character
    FONT_HEIGHT = 10    # the max height of the character
    # some character's type matrix, you can add yourself
    dict = {
        'A': "\n   #     \n   ##    \n  # #    \n  #  #   \n  ####   \n #    #  \n###  ### \n", \
        'B': "\n######   \n #    #  \n ######  \n #     # \n #     # \n #     # \n#######  \n", \
        'C': "\n   ####  \n  #    # \n #       \n #       \n #       \n  #    # \n   ####  \n", \
        'D': "\n######   \n #    #  \n #     # \n #     # \n #     # \n #    #  \n######   \n", \
        'E': "\n######   \n #    #  \n #       \n ####    \n #       \n #    #  \n######   \n", \
        'F': "\n ####### \n  #      \n  #   #  \n  #####  \n  #   #  \n  #      \n ###     \n", \
        'G': "\n   ####  \n  #   #  \n #       \n #       \n #   ##  \n #    #  \n  #####  \n", \
        'H': "\n###  ### \n #    #  \n #    #  \n ######  \n #    #  \n #    #  \n###  ### \n", \
        'I': "\n #####   \n   #     \n   #     \n   #     \n   #     \n   #     \n #####   \n", \
        'J': "\n  #####  \n    #    \n    #    \n    #    \n    #    \n#   #    \n ###     \n", \
        'K': "\n##  ##   \n #  #    \n # #     \n ##      \n # #     \n #  #    \n##  ##   \n", \
        'L': "\n###      \n #       \n #       \n #       \n #       \n #    #  \n#######  \n", \
        'M': "\n ## ##   \n#######  \n#  #  #  \n#  #  #  \n#  #  #  \n#  #  #  \n#  #  #  \n", \
        'N': "\n##   ### \n ##   #  \n # #  #  \n #  # #  \n #   ##  \n #    #  \n###   #  \n", \
        'O': "\n  ###    \n #   #   \n#     #  \n#     #  \n#     #  \n #   #   \n  ###    \n", \
        'P': "\n######   \n #    #  \n #    #  \n #####   \n #       \n #       \n###      \n", \
        'Q': "\n  ###    \n #   #   \n#     #  \n#     #  \n#   # #  \n #   #   \n  ### ## \n", \
        'R': "\n######   \n #    #  \n #    #  \n #####   \n ###     \n #  #    \n###  ##  \n", \
        'S': "\n  #####  \n #    #  \n ##      \n   ##    \n     ##  \n #    #  \n #####   \n", \
        'T': "\n#######  \n   #     \n   #     \n   #     \n   #     \n   #     \n  ###    \n", \
        'U': "\n###  ### \n #    #  \n #    #  \n #    #  \n #    #  \n #    #  \n  ####   \n", \
        'V': "\n###  ### \n #    #  \n #    #  \n ##  #   \n  #  #   \n  #  #   \n   ##    \n", \
        'W': "\n## # ##  \n # # #   \n # # #   \n # # #   \n # # #   \n  ###    \n  # #    \n", \
        'X': "\n###  ### \n #    #  \n  #  #   \n   ##    \n   ##    \n  #  #   \n##    ## \n", \
        'Y': "\n### ###  \n #   #   \n #   #   \n  # #    \n   #     \n   #     \n  ###    \n", \
        'Z': "\n ######  \n#    #   \n    #    \n   #     \n  #      \n #    #  \n######   \n", \
        ' ': "\n         \n         \n         \n         \n         \n         \n         \n"
    }

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        Canvas.__init__(self, cols * self.FONT_WIDTH + 1, rows * self.FONT_HEIGHT + 1)

    def draw_text(self, text, pos = [0, 0]):
        ''' usage: tablet.draw_text("this must be in the dict!", [position_x, position_y]) '''
        str_len = len(text)
        for y in range(self.rows):
            for x in range(self.cols):
                if str_len == 0:
                    break
                try:
                    cursor_pos = [x * self.FONT_WIDTH + pos[0] + 1, y * self.FONT_HEIGHT + pos[1] + 1]
                    for ch in self.dict[text[-str_len]]:
                        if ch != '\n':
                            self.tupMatrix[tuple(cursor_pos)] = ch
                            cursor_pos[0] += 1
                        else:
                            cursor_pos[1] += 1
                            cursor_pos[0] = x * self.FONT_WIDTH + pos[0] + 1
                    str_len -= 1
                except KeyError:
                    self.draw_line("only upper case!", [1, 1])

    def update(self):
        for i in range(self.height / self.FONT_HEIGHT):
            for j in range(self.width):
                self.tupMatrix[(j, (i + 1) * self.FONT_HEIGHT)] = '-'
        Canvas.update(self)


def getKeyEvent(keyHandler):
    deviceFilePath = '/sys/class/input/'
    os.chdir(deviceFilePath)
    for i in os.listdir(os.getcwd()):
        namePath = deviceFilePath + i + '/device/name'
        if os.path.isfile(namePath) and keyboardDevName in file(namePath).read():
            keyboardDevPath = "/dev/input/" + str(i)

    dev = InputDevice(keyboardDevPath)
    while True:
        select([dev], [], [], Canvas.REFRESH_PERIOD)
        try:
            for event in dev.read():
                if (event.value == 1 or event.value == 0) and event.code != 0:
                    keyHandler(ecodes.KEY[event.code], event.value)
        except Exception:
            pass


def setKeyHandler(keyHandler):
    thread.start_new_thread(getKeyEvent, (keyHandler, ))
