import cv2
import numpy as np
import os
import csv
import matplotlib.pyplot as plt

# Simulated function to detect vehicles
def detect_vehicles(image_path):
    np.random.seed(abs(hash(image_path)) % (10 ** 8))  # unique seed per image
    return np.random.randint(10, 100)  # random vehicle count between 10-100

def calculate_density(vehicle_count, frame_area, lane_count):
    vehicles_per_lane = vehicle_count / lane_count
    density = vehicles_per_lane / (frame_area / lane_count)
    return density

def classify_density(density):
    if density > 0.0002:
        return "High Traffic - Extend Green Light"
    elif density > 0.0001:
        return "Medium Traffic - Normal Cycle"
    else:
        return "Low Traffic - Short Green Light"

def sync_traffic_lights(pattern):
    if pattern == "High Traffic - Extend Green Light":
        return "Green Light Time: 90 seconds"
    elif pattern == "Medium Traffic - Normal Cycle":
        return "Green Light Time: 60 seconds"
    else:
        return "Green Light Time: 30 seconds"

# Main function to process folder
# Returns report_data and saves CSV/graph
# No popups, no plt.show()
def analyze_traffic_from_folder(folder_path, lane_count=3, report_csv="traffic_report.csv", graph_png="traffic_flow_graph.png"):
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} not found!")
        return []

    images = [img for img in os.listdir(folder_path) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        print("No images found in the folder.")
        return []

    report_data = []

    for image_name in sorted(images):
        image_path = os.path.join(folder_path, image_name)

        img = cv2.imread(image_path)
        if img is None:
            print(f"Error loading image: {image_name}")
            continue

        frame_area = img.shape[0] * img.shape[1]

        # Step 1: Detect vehicles
        vehicle_count = detect_vehicles(image_path)
        print(f"\nImage: {image_name}")
        print(f"Detected vehicles: {vehicle_count}")

        # Step 2: Calculate density
        density = calculate_density(vehicle_count, frame_area, lane_count)
        print(f"Calculated density: {density:.6f}")

        # Step 3: Classify traffic pattern
        pattern = classify_density(density)
        print(f"Traffic Pattern: {pattern}")

        # Step 4: Suggest light sync
        light_instruction = sync_traffic_lights(pattern)
        print(f"Suggested Traffic Light Timing: {light_instruction}")

        # Collecting data for report
        report_data.append({
            "Image": image_name,
            "Vehicle_Count": vehicle_count,
            "Density": density,
            "Traffic_Pattern": pattern,
            "Light_Instruction": light_instruction
        })

    # Save report to CSV
    save_report_as_csv(report_data, filename=report_csv)

    # Create traffic flow graph
    plot_traffic_flow(report_data, graph_png)

    return report_data

def save_report_as_csv(report_data, filename="traffic_report.csv"):
    if not report_data:
        return
    keys = report_data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(report_data)
    print(f"\n705 Traffic analysis report saved as {filename}")

def plot_traffic_flow(report_data, graph_png="traffic_flow_graph.png"):
    images = [entry["Image"] for entry in report_data]
    densities = [entry["Density"] for entry in report_data]

    plt.figure(figsize=(12, 6))
    plt.plot(images, densities, marker='o', linestyle='-', color='green')
    plt.title('Traffic Density Flow Throughout the Day')
    plt.xlabel('Image Frame')
    plt.ylabel('Traffic Density')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(graph_png)
    plt.close()
    print(f"\n705 Traffic density graph saved as {graph_png}")

# If run as script, do nothing (integration will be via import)
if __name__ == "__main__":
    output_folder = "output"  # Folder where your annotated images are
    analyze_traffic_from_folder(output_folder)
