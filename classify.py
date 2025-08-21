import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv(r"C:\Users\Shrut\traffic_density_project\filtered_boxes.csv")

# Count the number of bounding boxes (vehicles) per frame
vehicle_counts = df.groupby("Frame").size().reset_index(name="VehicleCount")

# Define traffic levels
def classify_traffic(count):
    if count <= 5:
        return "Low"
    elif count <= 12:
        return "Medium"
    else:
        return "High"

# Apply the classification
vehicle_counts["TrafficLevel"] = vehicle_counts["VehicleCount"].apply(classify_traffic)

# Show a sample of the result
print("Sample of vehicle counts per frame:")
print(vehicle_counts.head())

# Show traffic level distribution
traffic_summary = vehicle_counts["TrafficLevel"].value_counts(normalize=True) * 100
print("\nTraffic level summary (% of frames):")
print(traffic_summary.round(2))

# Optional: plot the summary
traffic_summary.plot(kind="bar", color=["green", "orange", "red"])
plt.title("Traffic Density Classification")
plt.ylabel("Percentage of Frames")
plt.xlabel("Traffic Level")
plt.tight_layout()
plt.show()

# Optional: save results to CSV
output_path = r"C:\Users\Shrut\traffic_density_project\frame_traffic_classification.csv"
vehicle_counts.to_csv(output_path, index=False)
print(f"\nTraffic classification saved to: {output_path}")
