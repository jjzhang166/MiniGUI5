import MiniGUI

PAINT_WIDTH = 100
PAINT_HEIGHT = 33

# load image text
f = open("./data/funny.txt", 'r')
image_text = f.read()
f.close()

print "Please maximize your terminal and run in root mode(for use your keyboard device)."
raw_input("Enter any key to continue")

canvas = MiniGUI.Canvas(PAINT_WIDTH, PAINT_HEIGHT)
canvas.draw_line("a string line", [int(canvas.width * 0.4), 1])
canvas.draw_image(image_text, [int(canvas.width * 0.2), 2])
canvas.update()