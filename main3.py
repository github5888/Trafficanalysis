# import cv2
# import numpy as np
# from ultralytics import YOLO

# # Load YOLO model
# model = YOLO("yolov8n.pt")

# # Load the image
# image_path = r'C:\Users\Shrut\traffic_density_project\images\traffic_density1.jpg'
# image = cv2.imread(image_path)

# # Detect objects
# results = model(image)

# # Initialize bounding box coordinates
# x_min, y_min = float('inf'), float('inf')  # Top-left corner
# x_max, y_max = 0, 0  # Bottom-right corner

# # Iterate through detected objects
# for result in results[0].boxes:
#     x1, y1, x2, y2 = map(int, result[:4])  # Extract bounding box coordinates
#     x_min, y_min = min(x_min, x1), min(y_min, y1)
#     x_max, y_max = max(x_max, x2), max(y_max, y2)

# # Draw the combined bounding box
# cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 3)

# # Display bounding box coordinates
# print(f"Bounding Box Coordinates:")
# print(f"Top: {y_min}")
# print(f"Bottom: {y_max}")
# print(f"Left: {x_min}")
# print(f"Right: {x_max}")

# # Save the output image
# output_path = r'C:\Users\Shrut\traffic_density_project\output'
# cv2.imwrite(output_path, image)

# cv2.imshow("Combined Bounding Box", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# import cv2
# import numpy as np
# from ultralytics import YOLO

# # Load YOLO model
# model = YOLO("yolov8n.pt")

# # Load the image
# image_path = r'C:\Users\Shrut\traffic_density_project\images\traffic_density1.jpg'
# image = cv2.imread(image_path)

# # Detect objects
# results = model(image)

# # Initialize bounding box coordinates
# all_boxes = []
# x_min, y_min = float('inf'), float('inf')  # Top-left corner
# x_max, y_max = 0, 0                        # Bottom-right corner

# # Iterate through detected objects
# for result in results[0].boxes:
#     x1, y1, x2, y2 = map(int, result.xyxy[0])  # Extract bounding box coordinates
#     all_boxes.append([x1, y1, x2, y2])
    
#     # Update overall bounding box coordinates
#     x_min, y_min = min(x_min, x1), min(y_min, y1)
#     x_max, y_max = max(x_max, x2), max(y_max, y2)

# # Draw the combined bounding box
# if all_boxes:
#     cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 3)

#     # Display bounding box coordinates
#     print(f"Bounding Box Coordinates:")
#     print(f"Top: {y_min}")
#     print(f"Bottom: {y_max}")
#     print(f"Left: {x_min}")
#     print(f"Right: {x_max}")

#     # Display the vehicle count
#     cv2.putText(image, f'Count: {len(all_boxes)}', (x_min, y_min - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# # Save the output image
# output_path = r'C:\Users\Shrut\traffic_density_project\output\merged_bounding_box.jpg'
# cv2.imwrite(output_path, image)

# # Display result
# cv2.imshow("Merged Bounding Box", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import os
import pandas as pd
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

# Paths for images and output
image_folder = r'C:\Users\Shrut\traffic_density_project\images'
output_folder = r'C:\Users\Shrut\traffic_density_project\output'
csv_path = os.path.join(output_folder, 'bounding_box_coordinates.csv')

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Data storage for bounding box coordinates
data = []

# Iterate through all images in the folder
for image_name in os.listdir(image_folder):
    if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_folder, image_name)
        image = cv2.imread(image_path)

        # Detect objects
        results = model(image)

        # Initialize bounding box coordinates
        all_boxes = []
        x_min, y_min = float('inf'), float('inf')
        x_max, y_max = 0, 0

        # Iterate through detected objects
        for result in results[0].boxes:
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            all_boxes.append([x1, y1, x2, y2])

            # Update overall bounding box coordinates
            x_min, y_min = min(x_min, x1), min(y_min, y1)
            x_max, y_max = max(x_max, x2), max(y_max, y2)

        # Draw merged bounding box on the image
        if all_boxes:
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 3)
            cv2.putText(image, f'Count: {len(all_boxes)}', (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Save the annotated image
        output_image_path = os.path.join(output_folder, image_name)
        cv2.imwrite(output_image_path, image)

        # Save bounding box coordinates for the image
        data.append({
            'Image Name': image_name,
            'Top': y_min,
            'Bottom': y_max,
            'Left': x_min,
            'Right': x_max,
            'Vehicle Count': len(all_boxes)
        })

# Save coordinates in CSV format
df = pd.DataFrame(data)
df.to_csv(csv_path, index=False)

print(f"Annotated images saved in: {output_folder}")
print(f"Bounding box coordinates saved in: {csv_path}")
