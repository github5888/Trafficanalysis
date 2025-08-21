import matplotlib.pyplot as plt
import csv
import os
import re

def generate_density_vs_green_graph(csv_path='traffic_report.csv', output_png='density_vs_green_time.png'):
    densities = []
    timings = []

    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return False

    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Use the correct column name 'Density' (capital D)
                density = float(row['Density'])
                # Extract seconds from 'Light_Instruction' (e.g., 'Green Light Time: 30 seconds')
                match = re.search(r'(\d+)\s*seconds', row['Light_Instruction'])
                if match:
                    green_time = int(match.group(1))
                    densities.append(density)
                    timings.append(green_time)
                else:
                    print(f"Could not extract green time from: {row['Light_Instruction']}")
            except (ValueError, KeyError) as e:
                print(f"Skipping row due to error: {e} | Row: {row}")

    if not densities or not timings:
        print("No valid data found in CSV.")
        return False

    plt.figure(figsize=(8, 5))
    plt.plot(densities, timings, marker='o')
    plt.xlabel("Traffic Density")
    plt.ylabel("Green Light Time (s)")
    plt.title("Density vs Green Signal Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_png)
    plt.close()
    print(f"Graph saved as {output_png}")
    return True

# If run as script, do nothing (integration will be via import)
if __name__ == "__main__":
    generate_density_vs_green_graph()
