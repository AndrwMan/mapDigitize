import cv2
import numpy as np
from PIL import Image

# Load the image using OpenCV
image_path = './imgs/raw/indonesia1.1.jpg'  # Change to the path of your image
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blurred, 75, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Assuming the largest contour is the map
largest_contour = max(contours, key=cv2.contourArea)
x, y, w, h = cv2.boundingRect(largest_contour)

# Crop the image using the coordinates of the largest contour
cropped_image = image[y:y+h, x:x+w]

# Convert the cropped image to a PIL image and save or display it
final_image = Image.fromarray(cropped_image)
final_image.save('./imgs/digitized/indonesia_processed1.jpg')  # Save the cropped image
final_image.show()  # Display the cropped image
