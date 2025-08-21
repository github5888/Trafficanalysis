import os
import cv2
from ultralytics import YOLO
import csv

def run_detection(input_folder='images', output_folder='output'):
    """
    Runs YOLO detection on all images in input_folder, saves annotated images to output_folder.
    Also saves vehicle counts per image to vehicle_counts.csv in output_folder.
    """
    model = YOLO('yolov8n.pt')  # Use YOLOv8 Nano for speed
    vehicle_labels = {'car', 'truck', 'bus', 'motorbike'}

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not images:
        print(f'No images found in {input_folder}')
        return 0

    vehicle_counts = []

    for image_name in images:
        image_path = os.path.join(input_folder, image_name)
        frame = cv2.imread(image_path)
        if frame is None:
            print(f'Skipping {image_name} (could not load)')
            continue
        results = model(frame)[0]
        count = 0
        for result in results.boxes:
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            conf = float(result.conf[0])
            cls = int(result.cls[0])
            label = model.names[cls]
            if label in vehicle_labels and conf > 0.3:
                count += 1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        out_path = os.path.join(output_folder, image_name)
        cv2.imwrite(out_path, frame)
        vehicle_counts.append({'frame': image_name, 'count': count})
        print(f'Processed and saved: {out_path} (vehicles: {count})')

    # Save vehicle counts to CSV
    csv_path = os.path.join(output_folder, 'vehicle_counts.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['frame', 'count'])
        writer.writeheader()
        writer.writerows(vehicle_counts)
    print(f'✅ Detection complete. Annotated images saved in {output_folder}. Vehicle counts saved in {csv_path}')
    return len(images)

# If run as script, do detection
if __name__ == '__main__':
    run_detection() 