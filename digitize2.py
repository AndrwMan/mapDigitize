import cv2
import numpy as np
from PIL import Image

# Load the image using OpenCV
image_path = './imgs/raw/indonesia1.1.jpg'  # Change to the path of your image
image = cv2.imread(image_path)
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

# Convert the map area to grayscale and threshold to get a binary mask
map_area_gray = cv2.cvtColor(map_area, cv2.COLOR_BGR2GRAY)
_, binary_map = cv2.threshold(map_area_gray, 1, 255, cv2.THRESH_BINARY)

# Invert the binary mask
binary_map = cv2.bitwise_not(binary_map)

# Find contours in the inverted mask
contours, _ = cv2.findContours(binary_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get the bounding box of the map area
x, y, w, h = cv2.boundingRect(contours[0])

# Crop the image to the map area
cropped_map = image[y:y+h, x:x+w]
cv2.imwrite('./imgs/digitized/indonesia_processed2.jpg', cropped_map)

# Convert the cropped image to RGB and isolate red lines
cropped_map_rgb = cv2.cvtColor(cropped_map, cv2.COLOR_BGR2RGB)
lower_red = np.array([202, 55, 78])  # Lower bound of red color
upper_red = np.array([262, 175, 134])  # Upper bound of red color
mask = cv2.inRange(cropped_map_rgb, lower_red, upper_red)

# Clean up the mask
kernel = np.ones((3,3), np.uint8)
mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
mask_cleaned = cv2.dilate(mask_cleaned, kernel, iterations=1)

# Apply the mask to isolate the red lines
red_lines = cv2.bitwise_and(cropped_map, cropped_map, mask=mask_cleaned)

# Convert to PIL image for saving or displaying
final_image = Image.fromarray(cv2.cvtColor(red_lines, cv2.COLOR_BGR2RGB))
final_image.save('./imgs/digitized/indonesia_isolated1.jpg')  # Save the image
final_image.show()  # Display the image
