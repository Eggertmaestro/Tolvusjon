import numpy as np 
import cv2 
import time 

cap = cv2.VideoCapture(1)

prev_frame_time = 0
new_frame_time = 0

while(True):
    ret, frame = cap.read()
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    
    # Finding the brightest spot
    min_val_bright, max_val_bright, min_loc_bright, max_loc_bright = cv2.minMaxLoc(gray)

    # Split the frame into BGR channels for redness detection
    b_channel, g_channel, r_channel = cv2.split(frame)
    
    # Create a mask for detecting the reddest spot
    mask = (r_channel > 100) & (g_channel < 80) & (b_channel < 80)

    # Find the reddest spot based on the red channel
    min_val_red, max_val_red, min_loc_red, max_loc_red = cv2.minMaxLoc(r_channel, mask.astype(np.uint8))

    cv2.circle(frame, max_loc_bright, 10, (255, 255, 0), 2)  # Brightest spot in cyan
    cv2.circle(frame, max_loc_red, 10, (0, 0, 255), 2)      # Reddest spot in red
   
   # Calculating the fps
    font = cv2.FONT_HERSHEY_SIMPLEX 
    new_frame_time = time.time() 
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 

    # Converting the fps into integer 
    fps = int(fps) 
    fps = str(fps) 

    # Putting the FPS count on the frame 
    cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

    # Display the result
    cv2.imshow('frame', frame)

    # print(fps)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
