import cv2
import numpy as np

# Load the image using OpenCV
image_path = './imgs/raw/JPEG 2000.jp2'  # Ensure this path is correct and the image is in a readable format
image = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Ensure that the image is being read correctly

if image is None:
    print("Image not loaded, check the file format and path.")
else:
    # Convert the image to grayscale for processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to smooth the image, reducing noise and detail
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    # Detect edges using Canny
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

    # Use morphological operations to close small gaps in contours
    kernel = np.ones((5,5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)
    cv2.imwrite('./imgs/digitized/edges_processed7.jpg', edges)  # Save the processed edges image for review

    # Find contours from the edged image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on aspect ratio and area
    def is_rectangular(contour):
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        return 0.75 < aspect_ratio < 1.25  # Assuming the map is roughly square

    contours = [cnt for cnt in contours if is_rectangular(cnt)]
    largest_contour = max(contours, key=cv2.contourArea) if contours else None

    if largest_contour is not None and len(largest_contour) > 0:
        # Draw the contours on an image for visualization
        contour_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contour_image, [largest_contour], -1, (0, 255, 0), 3)
        cv2.imwrite('./imgs/digitized/largest_contour_filtered7.jpg', contour_image)  # Save the largest contour image for review

        # Create a mask for the largest contour
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

        # Create a bitwise and of gray and mask to isolate the map
        map_isolated = cv2.bitwise_and(gray, mask)
        cv2.imwrite('./imgs/digitized/map_isolated7.jpg', map_isolated)  # Save the isolated map for review

        print("Map area isolated and saved.")
    else:
        print("No suitable contours found, adjust the filtering criteria.")
