import numpy as np
from numpy import pi
import cv2
import random
from Animator import Animator
import seaborn as sns

an = Animator()

class MySketch:

    # initialize an empty square list.
    squares = []
    # define the size of the squares.
    square_size = 25
    # define the gap between squares.
    square_gap = 5
    # define the width and height of the drawing window (consistent with Animator.py)
    width = 640
    height = 480
    # initialize frame counter
    frame = 0
    # initialize the mouse position at (1, 1)
    mouse_x = 1
    mouse_y = 1

    # Define a color palette,as Ref:https://seaborn.pydata.org/tutorial/color_palettes.html
    rocket_palette = sns.color_palette("rocket")

    def __init__(self):
        # call the setup method for initial settings and start the main loop to process subsequent mouse events
        self.setup()
        self.start_loop()

    def setup(self):
        print("setup")
        # calculate the rows and columns
        cols = self.width // (self.square_size + self.square_gap)
        rows = self.height // (self.square_size + self.square_gap)
        # loop through rows and columns
        # initializing the position, 'pai' parameter and the 'False' boolean
        for i in range(rows):
            for j in range(cols):
                x = self.square_gap + j * (self.square_size + self.square_gap)
                y = self.square_gap + i * (self.square_size + self.square_gap)
                col = random.randint(0,10)
                self.squares.append([(x, y), col, False])

    def draw(self):
        # define a background
        an.background(0)
        # loop through the square list
        for square in self.squares:
            # extract the parameters' values
            x, y = square[0]
            # increment 'pai' value by 0.05 in each loop to change color over time
            square[1] += 0.1
            # calculate the color based on the palette
            color_index = int((square[1] / 10) * len(self.rocket_palette)) % len(self.rocket_palette)
            color = tuple(int(color * 255) for color in self.rocket_palette[color_index])
            # use a boolean value to change between solid and empty
            if not square[2]:
                fill = 1
            else:
                fill = -1
            # draw the square
            cv2.rectangle(an.canvas, (x, y), (x + self.square_size, y + self.square_size), color, fill)

    def mouse_moved(self, event, mouse_x, mouse_y, flags, param):
        # 1 indicates the mouse was clicked
        if event == 1:
            # loop squares list
            for square in self.squares:
                # get the top-left position of square
                click_x, click_y = square[0]
                # check if the mouse position is within the square's boundaries
                if click_x <= mouse_x <= click_x + self.square_size and click_y <= mouse_y <= click_y + self.square_size:
                    # if the mouse was clicked inside the small square, change the boolean value (from empty to solid)
                    square[2] = True

    def start_loop(self):
        # initialize a variable to control the loop
        done = False
        # create a window named 'drawing'
        cv2.namedWindow('drawing')
        # set the mouse callback function
        cv2.setMouseCallback('drawing', self.mouse_moved)

        while not done:
            # draw the square
            self.draw()
            # display the current canvas in the window
            cv2.imshow("drawing", an.canvas)

            # check every 1 millisecond for a key press event, end the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # set done to True to end the loop
                done = True
                break

            # increase frame count
            self.frame += 1

        # close all windows created by OpenCV
        cv2.destroyAllWindows()

MySketch()
