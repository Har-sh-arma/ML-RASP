#!/usr/bin/env python3

import cv2

def applyTransform(img, message):
#    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.putText(img, message, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
    img = cv2.resize(img, (780, 540),interpolation = cv2.INTER_LINEAR)
    cv2.imshow("Video", img)
    cv2.waitKey(1)
