import cv2
import numpy as np
import time 

def fit_line_with_ransac(points, threshold=1):
    best_inliers_count = 0
    best_line = None

    for _ in range(100):  # Iterate for RANSAC iterations
        if len(points) < 2:
            continue
        sample_indices = np.random.choice(len(points), 2, replace=False)
        sample_pts = points[sample_indices]

        x1, y1 = sample_pts[0]
        x2, y2 = sample_pts[1]

        if x2 - x1 == 0:  # Skip vertical lines
            continue
        
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        inliers = []
        for pt in points:
            x, y = pt
            distance = abs(slope * x - y + intercept) / np.sqrt(slope ** 2 + 1)
            if distance < threshold:
                inliers.append(pt)

        if len(inliers) > best_inliers_count:
            best_inliers_count = len(inliers)
            best_line = (slope, intercept)

    return best_line

cap = cv2.VideoCapture(1)

prev_frame_time = 0
new_frame_time = 0

# minimizing the frame width and height for improved performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    points = np.column_stack(np.where(edges > 0))
    line = fit_line_with_ransac(points)
    
    if line is not None:
        slope, intercept = line
        y1 = int(intercept + slope * 0)  # y value at x = 0
        y2 = int(intercept + slope * (edges.shape[1] - 1))  # y value at max width
        cv2.line(edges, (0, y1), (edges.shape[1] - 1, y2), (255, 0, 0), 2)  # Draw the line in blue

    # Calculating the fps
    font = cv2.FONT_HERSHEY_SIMPLEX 
    new_frame_time = time.time() 
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 

    # Converting the fps into integer 
    fps = int(fps) 
    fps = str(fps) 

    # Putting the FPS count on the frame 
    cv2.putText(edges, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow('Edges with Line', edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()