import MiniGUI

WRITE_ROWS = 2
WRITE_COLS = 10

canvas = MiniGUI.Tablet(WRITE_ROWS, WRITE_COLS)
canvas.draw_text(raw_input("Enter any number of upper case: "))
canvas.update()