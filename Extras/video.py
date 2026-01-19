# Script for creating gif of near threshold stimulus presentation for use on our presentation slide!

import cv2
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'mp4v');
out = cv2.VideoWriter('vid.mp4', fourcc, 60, (1500, 1500));

for i in range(180): # Seems like roughly a solid amount of time between to look good on the slide
    frame = np.zeros((1500, 1500, 3), dtype=np.uint8);
    frame[:] = (255, 255, 255);
    
    if (i == 90):
        frame = cv2.imread("x_001.jpg", cv2.IMREAD_COLOR);
    
    out.write(frame);
    
    
out.release();