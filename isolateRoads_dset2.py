import cv2
import numpy as np
import os

# Define the input and output directories
input_dir = './imgs/cropped/'
output_dir = './imgs/isolated/'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# List all image files in the input directory
image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp', '.jp2'))]

for image_file in image_files:
    image_path = os.path.join(input_dir, image_file)
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Ensure that the image is being read correctly

    if image is None:
        print(f"Image {image_file} not loaded, check the file format and path.")
        continue
    
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
    output_path = os.path.join(output_dir, f'red_elements_{os.path.splitext(image_file)[0]}.jpg')
    cv2.imwrite(output_path, red_elements)  # Save the isolated red elements image for review

    print(f"Processed {image_file}: Red elements isolated and saved to {output_path}.")