import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    # Read frame from the webcam
    ret, frame = cap.read()

    # Convert frame to grayscale for circle detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Hough Circle Transform
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=50, param2=30, minRadius=5, maxRadius=20)

    # Check if circles are detected
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        # Create a copy of the frame to draw the circles on
        overlay = frame.copy()

        # Overlay similar circles on the frame
        for i in range(len(circles)):
            (x1, y1, r1) = circles[i]
            for j in range(len(circles)):
                if i == j:
                    continue  # Skip comparing the circle with itself
                (x2, y2, r2) = circles[j]
                distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2)^(.5)
                if distance <= 100:  # Adjust the threshold as needed
                    cv2.circle(overlay, (x2, y2), r2, (0, 255, 0), 4)  # Green circle with thickness 4

        # Add the overlay with similar circles to the original frame
        frame = cv2.addWeighted(frame, 1, overlay, 0.5, 0)

    # Display the frame in the GUI window
    cv2.imshow("Concentric Circle Detection", frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
