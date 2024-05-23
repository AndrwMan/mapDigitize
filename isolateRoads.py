import cv2
import numpy as np

# Load the cropped color image using OpenCV
cropped_image_path = './imgs/digitized/cropped_map_color.jpg'  # Ensure this path is correct and the image is in a readable format
image = cv2.imread(cropped_image_path, cv2.IMREAD_COLOR)  # Ensure that the image is being read correctly

if image is None:
    print("Image not loaded, check the file format and path.")
else:
    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for the red color in HSV
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Use the mask to extract the red elements
    red_elements = cv2.bitwise_and(image, image, mask=red_mask)
    cv2.imwrite('./imgs/digitized/red_elements.jpg', red_elements)  # Save the isolated red elements image for review

    print("Red elements isolated and saved.")
