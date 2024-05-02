import cv2
import numpy as np

# Load the image using OpenCV
image_path = './imgs/raw/indonesia1.1.jpg'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur and find edges
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 75, 150)

# Find contours and get the largest one
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_contour = max(contours, key=cv2.contourArea)

# Create a mask for the largest contour
mask = np.zeros_like(gray)
cv2.drawContours(mask, [largest_contour], -1, (255, 255, 255), thickness=cv2.FILLED)

# Bitwise AND with the original image to get the map area
map_area = cv2.bitwise_and(image, image, mask=mask)

# Convert the map area to HSV
hsv = cv2.cvtColor(map_area, cv2.COLOR_BGR2HSV)

# Define lower and upper bounds for red color in HSV based on RGB values
lower_red = np.array([0, 100, 100])  # Lower bound for red color in HSV
upper_red = np.array([20, 255, 255])  # Upper bound for red color in HSV

# Threshold the HSV image to get only red colors
mask_red = cv2.inRange(hsv, lower_red, upper_red)

# Bitwise-AND mask and original image
red_pixels = cv2.bitwise_and(map_area, map_area, mask=mask_red)

# Save the isolated red pixels
cv2.imwrite('./imgs/digitized/indonesia_red_pixels.jpg', red_pixels)
