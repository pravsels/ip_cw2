#!/usr/bin/env python
import argparse
import numpy as np
import cv2 as cv
from os import path


class Mask():

    def __init__(self, image_path):

        self.image_path = image_path

        self.image = cv.imread(image_path)
        self.image_dup = self.image.copy()

        self.mask = np.zeros(self.image.shape)
        self.mask_dup = self.mask.copy()

        self.brush_size = 3
        self.draw_mode = False

        self.window_name = "Select mask boundaries. s: save, r: redo, q: quit"


    def event_handler_cb(self, event, x, y, flags, params):

        if event == cv.EVENT_LBUTTONDOWN:
            self.draw_mode = True

        elif event == cv.EVENT_MOUSEMOVE:
            if self.draw_mode:
                cv.rectangle(self.image, (x-self.brush_size, y-self.brush_size),
                                         (x+self.brush_size, y+self.brush_size), (255, 0, 0), -1)

                cv.rectangle(self.mask, (x-self.brush_size, y-self.brush_size),
                                        (x+self.brush_size, y+self.brush_size), (255, 255, 255), -1)

                cv.imshow(self.window_name, self.image)

        elif event == cv.EVENT_LBUTTONUP:
            self.draw_mode = False


    def select_mask(self):
        cv.namedWindow(self.window_name, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.window_name, (1280, 720))
        cv.setMouseCallback(self.window_name, self.event_handler_cb)

        while True:

            cv.imshow(self.window_name, self.image)
            key = cv.waitKey(1)

            if key == ord("r") or key == ord("R"):
                self.image = self.image_dup.copy()
                self.mask = self.mask_dup.copy()

            elif key == ord("s") or key == ord("S"):
                break

            elif key == ord("q") or key == ord("Q"):
                cv.destroyAllWindows()
                exit()


        self.mask = self.mask
        cv.imshow("press any key to save mask.", self.mask)
        cv.waitKey(0)

        mask_path = path.join(path.dirname(self.image_path), 'mask.png')
        cv.imwrite(mask_path, self.mask)

        cv.destroyAllWindows()



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", required=True, help="path to image")

    args = parser.parse_args()

    assert args.image, "Arguement --image or -i is required for selecting mask boundaries."

    mask = Mask(args.image)

    mask.select_mask()
