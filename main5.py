# # import cv2
# # import os
# # import numpy as np
# # from ultralytics import YOLO

# # # Load YOLOv8 model
# # model = YOLO("yolov8n.pt")

# # # Paths
# # video_path = r'C:\Users\Shrut\traffic_density_project\video\traffic_video.mp4.mp4'
# # output_folder = r'C:\Users\Shrut\traffic_density_project\output5'
# # frames_folder = os.path.join(output_folder, "frames")
# # coordinates_file = os.path.join(output_folder, "coordinates.txt")

# # # Create output directories if not exist
# # os.makedirs(frames_folder, exist_ok=True)

# # # Open video
# # cap = cv2.VideoCapture(video_path)

# # if not cap.isOpened():
# #     print("❌ Error: Unable to open video file.")
# #     exit()

# # # Get video properties
# # fps = int(cap.get(cv2.CAP_PROP_FPS))
# # frame_count = 0

# # # Open file to save coordinates
# # with open(coordinates_file, "w") as coord_file:
# #     coord_file.write("Frame, X1, Y1, X2, Y2, Class, Confidence\n")

# #     while cap.isOpened():
# #         ret, frame = cap.read()
# #         if not ret:
# #             print(f"✅ Video processing completed. Total frames: {frame_count}")
# #             break

# #         frame_count += 1

# #         # Process every frame
# #         frame_name = f"frame_{frame_count}.jpg"
# #         frame_path = os.path.join(frames_folder, frame_name)

# #         # Run YOLO model
# #         results = model(frame)

# #         # Iterate through detected objects
# #         for result in results:
# #             for box in result.boxes:
# #                 x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
# #                 cls = int(box.cls[0])  # Class ID
# #                 conf = float(box.conf[0])  # Confidence score

# #                 # Draw bounding box on frame
# #                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

# #                 # Write coordinates to file
# #                 coord_file.write(f"{frame_count}, {x1}, {y1}, {x2}, {y2}, {cls}, {conf:.2f}\n")

# #         # Save the frame with annotations
# #         success = cv2.imwrite(frame_path, frame)
# #         if success:
# #             print(f"✅ Frame saved: {frame_path}")
# #         else:
# #             print(f"❌ Error saving frame: {frame_path}")

# # # Release video capture
# # cap.release()
# # cv2.destroyAllWindows()

# # print("🚀 All frames processed successfully!")
# # import cv2
# # import numpy as np
# # import os
# # import pandas as pd
# # from ultralytics import YOLO
# # from scipy.spatial import distance

# # # Load YOLO model
# # model = YOLO("yolov8n.pt")  # Using YOLOv8 Nano for speed

# # # Define paths
# # video_path = r"C:\Users\Shrut\traffic_density_project\video\traffic_video.mp4.mp4"
# # output_folder = r"C:\Users\Shrut\traffic_density_project\output5\frames"
# # coord_file = r"C:\Users\Shrut\traffic_density_project\output5\coordinates.csv"

# # # Create output folder if not exists
# # os.makedirs(output_folder, exist_ok=True)

# # # Open video
# # cap = cv2.VideoCapture(video_path)
# # if not cap.isOpened():
# #     print("❌ Error: Unable to open video file.")
# #     exit()

# # frame_count = 0
# # csv_data = []

# # # Vehicle class IDs for YOLOv8
# # VEHICLE_CLASSES = {2, 3, 5, 7}  # Car, Motorcycle, Bus, Truck (COCO class IDs)

# # def merge_boxes(boxes, threshold=50):
# #     """
# #     Merge bounding boxes that are close to each other within 'threshold' pixels.
# #     """
# #     merged_boxes = []
# #     used = set()

# #     for i in range(len(boxes)):
# #         if i in used:
# #             continue
# #         x1, y1, x2, y2 = boxes[i]

# #         for j in range(i + 1, len(boxes)):
# #             if j in used:
# #                 continue
# #             x1_b, y1_b, x2_b, y2_b = boxes[j]

# #             # Calculate center distance
# #             center1 = ((x1 + x2) // 2, (y1 + y2) // 2)
# #             center2 = ((x1_b + x2_b) // 2, (y1_b + y2_b) // 2)

# #             if distance.euclidean(center1, center2) < threshold:
# #                 # Merge bounding boxes
# #                 x1, y1 = min(x1, x1_b), min(y1, y1_b)
# #                 x2, y2 = max(x2, x2_b), max(y2, y2_b)
# #                 used.add(j)

# #         merged_boxes.append((x1, y1, x2, y2))

# #     return merged_boxes

# # while cap.isOpened():
# #     ret, frame = cap.read()
# #     if not ret:
# #         break  # Stop when video ends

# #     # Detect objects
# #     results = model(frame)

# #     # Extract vehicle bounding boxes
# #     boxes = []
# #     for result in results:
# #         for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
# #             if int(cls) in VEHICLE_CLASSES:  # Only keep vehicles
# #                 x1, y1, x2, y2 = map(int, box[:4])
# #                 boxes.append((x1, y1, x2, y2))

# #     # Merge nearby bounding boxes
# #     merged_boxes = merge_boxes(boxes, threshold=50)

# #     # Draw merged bounding boxes
# #     for (x1, y1, x2, y2) in merged_boxes:
# #         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)

# #     # Save frame with annotations
# #     frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
# #     cv2.imwrite(frame_filename, frame)

# #     # Save bounding box coordinates in CSV format
# #     for (x1, y1, x2, y2) in merged_boxes:
# #         csv_data.append([frame_count, x1, y1, x2, y2])

# #     frame_count += 1

# # # Save CSV file
# # df = pd.DataFrame(csv_data, columns=["Frame", "X1", "Y1", "X2", "Y2"])
# # df.to_csv(coord_file, index=False)

# # # Cleanup
# # cap.release()
# # cv2.destroyAllWindows()

# # print(f"✅ Processing complete! Annotated frames saved in '{output_folder}' and coordinates in '{coord_file}'.")
# import cv2
# import numpy as np
# import os
# import pandas as pd
# from ultralytics import YOLO
# from scipy.spatial import distance
# from itertools import combinations

# # Load YOLO model
# model = YOLO("yolov8n.pt")  # YOLOv8 Nano for fast detection

# # Paths
# video_path = r"C:\Users\Shrut\traffic_density_project\video\traffic_video.mp4.mp4"
# output_folder = r"C:\Users\Shrut\traffic_density_project\output\frames2"
# coord_file = r"C:\Users\Shrut\traffic_density_project\output\coordinates2.csv"

# # Create output folder
# os.makedirs(output_folder, exist_ok=True)

# # Open video
# cap = cv2.VideoCapture(video_path)
# if not cap.isOpened():
#     print("❌ Error: Unable to open video file.")
#     exit()

# frame_count = 0
# csv_data = []

# # Vehicle class IDs for YOLOv8 (Car, Motorcycle, Bus, Truck)
# VEHICLE_CLASSES = {2, 3, 5, 7}

# def iou(box1, box2):
#     """Calculate Intersection over Union (IoU) between two bounding boxes."""
#     x1, y1, x2, y2 = box1
#     x1_b, y1_b, x2_b, y2_b = box2

#     # Compute the intersection
#     inter_x1 = max(x1, x1_b)
#     inter_y1 = max(y1, y1_b)
#     inter_x2 = min(x2, x2_b)
#     inter_y2 = min(y2, y2_b)

#     inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

#     # Compute the union
#     box1_area = (x2 - x1) * (y2 - y1)
#     box2_area = (x2_b - x1_b) * (y2_b - y1_b)
#     union_area = box1_area + box2_area - inter_area

#     return inter_area / union_area if union_area > 0 else 0

# def merge_boxes(boxes, iou_threshold=0.3, dist_threshold=80):
#     """
#     Merge bounding boxes that have IoU > threshold or are close in distance.
#     """
#     merged_boxes = []
#     used = set()

#     for i, j in combinations(range(len(boxes)), 2):
#         if i in used or j in used:
#             continue

#         if iou(boxes[i], boxes[j]) > iou_threshold or distance.euclidean(
#             ((boxes[i][0] + boxes[i][2]) // 2, (boxes[i][1] + boxes[i][3]) // 2),
#             ((boxes[j][0] + boxes[j][2]) // 2, (boxes[j][1] + boxes[j][3]) // 2)
#         ) < dist_threshold:
#             # Merge bounding boxes
#             x1 = min(boxes[i][0], boxes[j][0])
#             y1 = min(boxes[i][1], boxes[j][1])
#             x2 = max(boxes[i][2], boxes[j][2])
#             y2 = max(boxes[i][3], boxes[j][3])

#             merged_boxes.append((x1, y1, x2, y2))
#             used.add(i)
#             used.add(j)

#     # Add unmerged boxes
#     for i, box in enumerate(boxes):
#         if i not in used:
#             merged_boxes.append(box)

#     return merged_boxes

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break  # Stop when video ends

#     # Detect objects
#     results = model(frame)

#     # Extract vehicle bounding boxes
#     boxes = []
#     for result in results:
#         for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
#             if int(cls) in VEHICLE_CLASSES:  # Only keep vehicles
#                 x1, y1, x2, y2 = map(int, box[:4])
#                 boxes.append((x1, y1, x2, y2))

#     # Merge nearby bounding boxes
#     merged_boxes = merge_boxes(boxes, iou_threshold=0.3, dist_threshold=80)

#     # Draw merged bounding boxes
#     for (x1, y1, x2, y2) in merged_boxes:
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)

#     # Save frame with annotations
#     frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
#     cv2.imwrite(frame_filename, frame)

#     # Save bounding box coordinates in CSV format
#     for (x1, y1, x2, y2) in merged_boxes:
#         csv_data.append([frame_count, x1, y1, x2, y2])

#     frame_count += 1

# # Save CSV file
# df = pd.DataFrame(csv_data, columns=["Frame", "X1", "Y1", "X2", "Y2"])
# df.to_csv(coord_file, index=False)

# # Cleanup
# cap.release()
# cv2.destroyAllWindows()

# print(f"✅ Processing complete! Annotated frames saved in '{output_folder}' and coordinates in '{coord_file}'.")
import cv2
import numpy as np
from ultralytics import YOLO
import pandas as pd

# Load YOLO model
model = YOLO("yolov8n.pt")

# Load video
video_path = r"C:\Users\Shrut\traffic_density_project\video\traffic_video.mp4.mp4"
cap = cv2.VideoCapture(video_path)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Output video writer
out = cv2.VideoWriter("output_polygon_filtered.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

frame_count = 0
csv_data = []

# Define polygon points for right side of the road (adjust as needed)
polygon_pts = np.array([[650, 0], [1280, 0], [1280, 720], [650, 720]], dtype=np.int32)

def is_box_inside_polygon(box, polygon):
    """Check if the center of the bounding box is inside the polygon."""
    x1, y1, x2, y2 = box
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    return cv2.pointPolygonTest(polygon, (center_x, center_y), False) >= 0

def merge_overlapping_boxes(boxes, threshold=0.5):
    merged_boxes = []
    used = [False] * len(boxes)

    for i in range(len(boxes)):
        if used[i]:
            continue
        x1, y1, x2, y2 = boxes[i]
        for j in range(i + 1, len(boxes)):
            if used[j]:
                continue
            x1_, y1_, x2_, y2_ = boxes[j]

            # Calculate IoU
            xx1 = max(x1, x1_)
            yy1 = max(y1, y1_)
            xx2 = min(x2, x2_)
            yy2 = min(y2, y2_)
            inter_area = max(0, xx2 - xx1) * max(0, yy2 - yy1)
            area_i = (x2 - x1) * (y2 - y1)
            area_j = (x2_ - x1_) * (y2_ - y1_)
            iou = inter_area / float(area_i + area_j - inter_area)

            if iou > threshold:
                # Merge
                x1 = min(x1, x1_)
                y1 = min(y1, y1_)
                x2 = max(x2, x2_)
                y2 = max(y2, y2_)
                used[j] = True

        merged_boxes.append([x1, y1, x2, y2])
        used[i] = True

    return merged_boxes

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Run object detection
    results = model(frame)[0]

    boxes = []
    for result in results.boxes:
        x1, y1, x2, y2 = result.xyxy[0]
        conf = result.conf[0]
        cls = result.cls[0]
        label = model.names[int(cls)]

        if label in ["car", "truck", "bus", "motorbike"] and conf > 0.3:
            boxes.append([int(x1), int(y1), int(x2), int(y2)])

    # Merge overlapping boxes
    merged_boxes = merge_overlapping_boxes(boxes)

    # Filter boxes inside polygon
    filtered_boxes = [box for box in merged_boxes if is_box_inside_polygon(box, polygon_pts)]

    # Draw polygon
    cv2.polylines(frame, [polygon_pts], isClosed=True, color=(0, 255, 255), thickness=3)

    # Draw filtered boxes
    for (x1, y1, x2, y2) in filtered_boxes:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
        csv_data.append([frame_count, x1, y1, x2, y2])

    out.write(frame)
    cv2.imshow("Filtered Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# Save CSV
df = pd.DataFrame(csv_data, columns=["Frame", "x1", "y1", "x2", "y2"])
df.to_csv("filtered_boxes.csv", index=False)
