import cv2
import numpy as np

def detect_smpm_connector(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform circle detection using HoughCircles
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=30, minRadius=10, maxRadius=100)

    if circles is not None:
        # Convert the circle parameters to integers
        circles = np.round(circles[0, :]).astype(int)

        for (x, y, r) in circles:
            # Draw the outer aluminum circle
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)

            # Draw the inner amber circle
            amber_radius = int(r * 0.8)  # Adjust the scaling factor as needed
            cv2.circle(image, (x, y), amber_radius, (0, 0, 255), 2)

            # Draw the central pin
            pin_radius = int(r * 0.2)  # Adjust the scaling factor as needed
            cv2.circle(image, (x, y), pin_radius, (255, 0, 0), 2)

        return True, image
    else:
        return False, image

# Load the image
image = cv2.imread('C:\\Users\\hannar1\\OneDrive\\Wentworth Institute of Technology\\Capstone\\2023\\Media\\oneJib.JPG')  # Replace 'your_image.jpg' with the path to your image

# Detect SMPM connector
success, result_image = detect_smpm_connector(image)

# Display the result
cv2.imshow('SMPM Connector Detection', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
