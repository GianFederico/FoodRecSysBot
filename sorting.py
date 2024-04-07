# # Sorts values in file
# file_path = "sust_scores.txt"

# with open(file_path, 'r') as file:
#     lines = file.readlines()
#     numbers = []
#     for line in lines:
#         numbers.extend([float(num.strip()) for num in line.split(',') if num.strip()])

# sorted_numbers = sorted(numbers)

# sorted_file_path = "sorted_" + file_path

# with open(sorted_file_path, 'w') as file:
#     for number in sorted_numbers:
#         file.write(str(number) + '\n')
# ##_____________________________________________________________________________________________________________


import numpy as np

with open('sorted_DSS.txt', 'r') as file:
    # Read the contents of the file
    data = file.read()

data = [float(number) for number in data.split('\n')]

# Convert the list into a NumPy array
data_array = np.array(data)

# Calculate quartiles (20th, 40th, 60th, 80th, 100th  percentiles)
quartiles = np.percentile(data, [20, 40, 60, 80, 100])

# Calculate thresholds
thresholds = [quartiles[0], quartiles[1], quartiles[2], quartiles[3], quartiles[4]]

print("Thresholds:", thresholds)
