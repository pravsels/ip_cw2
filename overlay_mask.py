#!/usr/bin/env python
import argparse
import numpy as np
import cv2 as cv
from os import path


class MaskOverlay():

    def __init__(self, image_path, mask_path):

        self.image_path = image_path
        self.mask_path = mask_path

        self.image = cv.imread(image_path)
        self.image_dup = self.image.copy()

        mask = cv.imread(mask_path)
        self.mask = np.zeros(self.image.shape)
        self.mask[np.where(mask != 0)] = 255
        self.mask_dup = self.mask.copy()

        self.move_mode = False

        self.x0 = 0
        self.y0 = 0
        self.x = 0
        self.y = 0

        self.first_touch = True

        self.window_name = "Move mask. s: save, r: redo, q: quit"


    def blend(self, image, mask):

        result = image.copy()

        alpha = 0.2
        result[mask != 0] = result[mask != 0]*alpha + 255*(1-alpha)

        return result.astype(np.uint8)


    def event_handler_cb(self, event, x, y, flags, params):

        if event == cv.EVENT_LBUTTONDOWN:
            self.move_mode = True

            if self.first_touch:
                self.x0, self.y0 = x, y
                self.first_touch = False

            self.x, self.y = x, y

        elif event == cv.EVENT_MOUSEMOVE:
            if self.move_mode:
                M = np.float32([
                                [1, 0, x - self.x],
                                [0, 1, y - self.y]
                            ])
                self.mask = cv.warpAffine(self.mask, M, (self.mask.shape[1], self.mask.shape[0]))

                cv.imshow(self.window_name, self.blend(self.image, self.mask))

                self.x, self.y = x, y

        elif event == cv.EVENT_LBUTTONUP:
            self.move_mode = False


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
        # cv.imshow("press any key to save mask.", self.mask)
        # cv.waitKey(0)

        mask_overlayed_path = path.join(path.dirname(self.image_path), 'mask_overlayed.png')
        cv.imwrite(mask_overlayed_path, self.mask)

        cv.destroyAllWindows()



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", required=True, help="path to image")
    parser.add_argument("-m", "--mask", required=True, help="path to mask")

    args = parser.parse_args()

    assert args.image, "Arguement --image or -i is required for overlaying mask."
    assert args.mask, "Arguement --mask or -m is required for overlaying mask."

    mask = MaskOverlay(args.image, args.mask)

    mask.select_mask()
