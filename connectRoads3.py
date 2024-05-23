import cv2
import numpy as np

# Load the red elements image using OpenCV
red_elements_image_path = './imgs/digitized/red_elements.jpg'  # Ensure this path is correct and the image is in a readable format
image = cv2.imread(red_elements_image_path, cv2.IMREAD_COLOR)  # Ensure that the image is being read correctly

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
    
    # Save the red mask
    cv2.imwrite('./imgs/digitized/intermediate_red_mask4.jpg', red_mask)

    # Extract the red elements using the mask
    red_elements = cv2.bitwise_and(image, image, mask=red_mask)
    
    # Save the extracted red elements
    cv2.imwrite('./imgs/digitized/intermediate_red_elements4.jpg', red_elements)

    # Convert the red elements to grayscale
    red_elements_gray = cv2.cvtColor(red_elements, cv2.COLOR_BGR2GRAY)
    
    # Save the grayscale red elements
    cv2.imwrite('./imgs/digitized/intermediate_red_elements_gray4.jpg', red_elements_gray)

    # Apply morphological operations to connect the dotted lines
    kernel = np.ones((5, 5), np.uint8)
    closed_red_elements = cv2.morphologyEx(red_elements_gray, cv2.MORPH_CLOSE, kernel, iterations=5)
    
    # Save the closed red elements
    cv2.imwrite('./imgs/digitized/intermediate_closed_red_elements4.jpg', closed_red_elements)

    # Create a mask from the closed red elements
    _, red_mask_closed = cv2.threshold(closed_red_elements, 1, 255, cv2.THRESH_BINARY)
    
    # Save the mask from closed red elements
    cv2.imwrite('./imgs/digitized/intermediate_red_mask_closed4.jpg', red_mask_closed)

    # Convert the closed red elements back to BGR format
    closed_red_elements_bgr = cv2.bitwise_and(image, image, mask=red_mask_closed)
    
    # Save the closed red elements in BGR format
    cv2.imwrite('./imgs/digitized/intermediate_closed_red_elements_bgr4.jpg', closed_red_elements_bgr)

    # Combine the closed red elements with the original red elements
    final_red_elements = cv2.addWeighted(red_elements, 0.5, closed_red_elements_bgr, 0.5, 0)
    
    # Save the final result
    cv2.imwrite('./imgs/digitized/connected_red_elements4.jpg', final_red_elements)

    print("Red dotted lines connected and saved.")

