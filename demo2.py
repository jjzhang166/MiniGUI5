import MiniGUI

WRITE_ROWS = 2
WRITE_COLS = 10

print "Please maximize your terminal and run in root mode(for use your keyboard device)."
raw_input("Enter any key to continue")

canvas = MiniGUI.Tablet(WRITE_ROWS, WRITE_COLS)
canvas.draw_text(raw_input("Enter any number of upper case: "))
canvas.update()