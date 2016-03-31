import math
import MiniGUI

PAINT_WIDTH = 100
PAINT_HEIGHT = 33
ROTATE_SPEED = 0.2
MOVING_SPEED = [1, 0]

def keyHandler(key, value):
    global MOVING_SPEED
    if value == 1:
        if key == 'KEY_D':
            MOVING_SPEED[0] += 1
        elif key == 'KEY_A':
            MOVING_SPEED[0] -= 1
        elif key == 'KEY_S':
            MOVING_SPEED[1] += 1
        elif key == 'KEY_W':
            MOVING_SPEED[1] -= 1

# load image_text
image_text = {}
image_text['bus'] = MiniGUI.loadImageText("./data/bus.txt")
image_text['wheel'] = MiniGUI.loadImageText("./data/wheel.txt")

canvas = MiniGUI.Canvas(PAINT_WIDTH, PAINT_HEIGHT)
MiniGUI.setKeyHandler(keyHandler)

det_angle = 0
det_pos = [0, 0]
while True:
    det_angle += math.pi * ROTATE_SPEED
    det_angle %= math.pi * 2
    det_pos[0] += MOVING_SPEED[0]
    det_pos[1] += MOVING_SPEED[1]
    det_pos[0] %= PAINT_WIDTH
    det_pos[1] %= PAINT_HEIGHT
    canvas.draw_image(image_text["wheel"], [5 + int(det_pos[0]), 5 + int(det_pos[1])], det_angle)
    canvas.draw_image(image_text["wheel"], [35 + int(det_pos[0]), 5 + int(det_pos[1])], det_angle)
    canvas.draw_image(image_text["bus"], [1 + int(det_pos[0]), 1 + int(det_pos[1])])
    canvas.draw_image("#########", [30, 25], det_angle)
    canvas.draw_image("#########", [60, 25], det_angle)
    canvas.update()