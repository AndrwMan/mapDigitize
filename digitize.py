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

# Convert the map area to grayscale
map_gray = cv2.cvtColor(map_area, cv2.COLOR_BGR2GRAY)

# Find contours of non-black pixels
contours, _ = cv2.findContours(map_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get the bounding box of the non-black pixels
x, y, w, h = cv2.boundingRect(contours[0])

# Crop the map area to the bounding box
map_cropped = map_area[y:y+h, x:x+w]

# Save the cropped map
cv2.imwrite('./imgs/digitized/indonesia_map_cropped2.jpg', map_cropped)

