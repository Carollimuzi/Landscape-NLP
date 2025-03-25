import json
import matplotlib.pyplot as plt
from collections import Counter

# # Load the cleaned JSON file
# file_path = '/root/data/cleaned_labeldata211_v2.json'
# with open(file_path, 'r') as file:
#     data = json.load(file)

# # Count occurrences of each label
# label_counter = Counter()
# for item in data:
#     for key in item:
#         for label in item[key]:
#             label_counter[label] += 1

# # Prepare data for plotting
# labels = list(label_counter.keys())
# counts = list(label_counter.values())

# # Plot the distribution
# plt.figure(figsize=(12, 6))
# bars = plt.barh(labels, counts, color='skyblue')
# plt.ylabel('Labels')
# plt.xlabel('Count')
# plt.title('Distribution of Label Categories')
# plt.tight_layout()

# # Add value labels next to each bar
# for bar in bars:
#     plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, str(bar.get_width()), ha='left', va='center')

# # Save the plot to the current path
# plt.savefig('/root/data/label_distribution1.png')


# Load the JSON file
file_path = '/root/data/originaldata.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Count the occurrences of each label
label_counter = Counter()
for item in data:
    for span in item['spans']:
        label_counter[span['type']] += 1

# # Print label counts
# for label, count in label_counter.items():
#     print(f"{label}: {count}")

# Sort labels alphabetically
sorted_labels_counts = sorted(label_counter.items())
labels, counts = zip(*sorted_labels_counts)

# Plot the label distribution
plt.figure(figsize=(12, 6))
bars = plt.barh(labels, counts, color='skyblue')
plt.ylabel('Labels')
plt.xlabel('Count')
plt.title('Label Distribution in Testset')
plt.tight_layout()

# Add value labels on each bar
for bar in bars:
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, str(bar.get_width()), ha='left', va='center')

# Save the plot
plt.savefig('/root/data/originaldata.png')

# Show the plot
plt.show()
