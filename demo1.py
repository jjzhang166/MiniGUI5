import MiniGUI

PAINT_WIDTH = 100
PAINT_HEIGHT = 33

image_text = MiniGUI.loadImageText("./data/funny.txt")

canvas = MiniGUI.Canvas(PAINT_WIDTH, PAINT_HEIGHT)
canvas.draw_line("a string line", [int(canvas.width * 0.4), 1])
canvas.draw_image(image_text, [int(canvas.width * 0.2), 2])
canvas.update()