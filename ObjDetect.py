import os
from picamzero import Camera
from time import sleep
import cv2


home_dir = os.environ['HOME'] #set the location of the home directory
cam = Camera()
cam.flip_camera(hflip=True, vflip=True) # to rotate camera
cam.still_size = (3280, 2464) # to change the resolution of the image (this is max for this cam, min is 15x15)
# find a user
users = []
users.append(os.getlogin)
#pull the information about what eah object is called
classNames = []


cam.start_preview()
#sleep(5)
#cam.take_photo(f"{home_dir}/Desktop/new_image.jp") #save the image to the desktop
#cam.take_photo(f"{home_dir}/Desktop/max.jp")
#cam.capture_sequence(f"{home_dir}/Desktop/sequence.jpg", num_images=3, interval=2) #capture 3 sequence images with 2 second delay
#cam.record_video(f"{home_dir}/Desktop/new_video.mp4", duration=5)
cam.stop_preview()