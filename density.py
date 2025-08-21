import cv2
from ultralytics import YOLO
import os

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Paths to input images and output folder
image_paths = ['images/traffic_density1.jpg', 'images/traffic_density2.jpg']
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

for image_path in image_paths:
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading {image_path}")
        continue

    # Perform detection
    results = model(image)

    # Count total vehicles (full image)
    vehicle_count = 0
    for result in results[0].boxes:
        x_min, y_min, x_max, y_max = map(int, result.xyxy[0])
        class_id = int(result.cls[0])

        # Filter for vehicles (car, truck, bus, motorcycle)
        if class_id in [2, 3, 5, 7]:
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            vehicle_count += 1

    # Calculate density based on total image area
    total_area = image.shape[0] * image.shape[1]
    density = (vehicle_count / total_area) * 100

    # Display vehicle count and density
    cv2.putText(image, f'Count: {vehicle_count}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
    cv2.putText(image, f'Density: {density:.4f}%', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    # Save result
    output_path = os.path.join(output_folder, f'detected_{os.path.basename(image_path)}')
    cv2.imwrite(output_path, image)

    print(f"Processed image saved at: {output_path}")
    print(f"Total Vehicles Detected in {image_path}: {vehicle_count}")
    print(f"Traffic Density in {image_path}: {density:.4f}%")