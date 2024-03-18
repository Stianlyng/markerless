import cv2
import numpy as np

def detect_and_fill_markers(image_path):
    # Load the image
    image = cv2.imread(image_path)
    inpaint_mask = np.zeros(image.shape[:2], np.uint8)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to find white markers. Adjust the thresholds as needed.
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a mask for inpainting
    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        
        # Fill the circle in the mask
        #cv2.circle(inpaint_mask, center, radius, (255, 255, 255), -1)
        cv2.circle(inpaint_mask, center, radius+3, (255, 255, 255), -1)
    
    # Inpaint the original image using the mask
    inpainted_image = cv2.inpaint(image, inpaint_mask, inpaintRadius=30, flags=cv2.INPAINT_TELEA)
    
    new_img_path = image_path.replace('.ppm','')
    cv2.imwrite('output.png', inpainted_image)
    # Show the output image
    cv2.imshow('Inpainted Image', inpainted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Replace 'path_to_your_image.jpg' with the path to the image you want to process
detect_and_fill_markers('man.ppm')
