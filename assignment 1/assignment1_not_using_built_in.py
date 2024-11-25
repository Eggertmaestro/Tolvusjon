import cv2
import time

cap = cv2.VideoCapture(1)

prev_frame_time = 0
fps = 0

while True:
    ret, frame = cap.read()

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape


    max_brightness_value = 0
    max_brightness_location = (0, 0)

    max_red_value = 0
    max_red_location = (0, 0)


    # Loop through each pixel in the grayscale image
    for y in range(height):
        for x in range(width):
            # Get the brightness pixel value
            brightness_value = gray[y, x]
            # If this pixel is brighter than the current max, update max_brightness_value and max_brightness_location
            if brightness_value > max_brightness_value:
                max_brightness_value = brightness_value
                max_brightness_location = (x, y)

            # Get the red, green, blue channel values
            b_channel, g_channel, r_channel = frame[y, x]
            
            # Check for the reddest pixel
            if r_channel > 100 and g_channel < 80 and b_channel < 80:
                if r_channel > max_red_value:
                    max_red_value = r_channel
                    max_red_location = (x, y)

    cv2.circle(frame, max_brightness_location, 10, (0, 255, 0), 2)  # Green circle for brightest spot
    cv2.circle(frame, max_red_location, 10, (0, 0, 255), 2)  # Red circle for reddest spot

   # Calculating the fps
    font = cv2.FONT_HERSHEY_SIMPLEX 
    new_frame_time = time.time() 
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 

    # Converting the fps into integer 
    fps = int(fps) 
    fps = str(fps) 

    # Put the FPS text on the frame
    cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

    # Display the result
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()