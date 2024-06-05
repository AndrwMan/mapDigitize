import cv2
import numpy as np
import os

# Define the input and output directories
input_dir = './imgs/raw/'
output_dir = './imgs/cropped/'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# List all files in the input directory
image_files = [f for f in os.listdir(input_dir) if f.endswith('.jp2')]

for image_file in image_files:
    image_path = os.path.join(input_dir, image_file)
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    if image is None:
        print(f"Image {image_file} not loaded, check the file format and path.")
        continue
    
    # Convert the image to grayscale for processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to smooth the image, reducing noise and detail
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    # Use adaptive thresholding
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)

    # Use morphological operations to close small gaps in contours
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.dilate(thresholded, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)
    edge_output_path = os.path.join(output_dir, f'edges_{os.path.splitext(image_file)[0]}.jpg')
    cv2.imwrite(edge_output_path, edges)

    # Find contours from the thresholded image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on aspect ratio and area
    def is_rectangular(contour):
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        return 0.5 < aspect_ratio < 2  # Adjust aspect ratio according to your map's shape

    contours = [cnt for cnt in contours if is_rectangular(cnt) and cv2.contourArea(cnt) > 1000]  # Adjust area threshold
    largest_contour = max(contours, key=cv2.contourArea) if contours else None

    if largest_contour is not None and len(largest_contour) > 0:
        # Draw the contours on an image for visualization
        contour_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contour_image, [largest_contour], -1, (0, 255, 0), 3)
        contour_output_path = os.path.join(output_dir, f'largest_contour_{os.path.splitext(image_file)[0]}.jpg')
        cv2.imwrite(contour_output_path, contour_image)

        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Crop the isolated map to the bounding box
        cropped_map_color = image[y:y+h, x:x+w]
        cropped_output_path = os.path.join(output_dir, f'cropped_map_{os.path.splitext(image_file)[0]}.jpg')
        cv2.imwrite(cropped_output_path, cropped_map_color)

        print(f"Processed {image_file}: Map area isolated, cropped, and saved in color.")
    else:
        print(f"No suitable contours found in {image_file}, adjust the filtering criteria.")
