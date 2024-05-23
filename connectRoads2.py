import cv2
import numpy as np

# Load the red elements image using OpenCV
red_elements_image_path = './imgs/digitized/red_elements.jpg'  # Ensure this path is correct and the image is in a readable format
image = cv2.imread(red_elements_image_path, cv2.IMREAD_COLOR)  # Ensure that the image is being read correctly

if image is None:
    print("Image not loaded, check the file format and path.")
else:
    # Convert the image to grayscale for processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply morphological operations to connect the dotted lines
    kernel = np.ones((5, 5), np.uint8)
    closed_red_elements = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=5)

    # Convert the closed red elements back to BGR format
    closed_red_elements_bgr = cv2.cvtColor(closed_red_elements, cv2.COLOR_GRAY2BGR)

    # Create a mask from the closed red elements
    red_mask_closed = cv2.inRange(closed_red_elements_bgr, (1, 1, 1), (255, 255, 255))

    # Combine the closed red elements with the original image using the mask
    final_red_elements = cv2.bitwise_and(image, image, mask=red_mask_closed)

    cv2.imwrite('./imgs/digitized/connected_red_elements2.jpg', final_red_elements)  # Save the connected red elements image for review

    print("Red dotted lines connected and saved.")
