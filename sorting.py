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
#_____________________________________________________________________________________________________________


# calculates the breakpoints based on the distribution of values of soretd_sust_scores. 
# It iterates over each range, calculates the percentage of total values in that range, computes the cumulative percentage, and then calculates the breakpoint. 
ranges_counts = [
    (0, 17129),
    (1, 22707),
    (2, 25117),
    (3, 26226),
    (4, 27178)
]

# Calculate the breakpoints
breakpoints = []
total_values = ranges_counts[-1][1]  # Total count of values

# Iterate over each range and calculate the breakpoints
for i in range(len(ranges_counts) - 1):
    range_start, count = ranges_counts[i]
    next_range_start, _ = ranges_counts[i + 1] if i < len(ranges_counts) - 1 else (None, None)
    percentage_of_total = count / total_values  # Percentage of total values in this range
    cumulative_percentage = sum(b[1] / total_values for b in breakpoints)  # Cumulative percentage
    breakpoint = cumulative_percentage + percentage_of_total
    breakpoints.append((range_start, breakpoint))

# Add the last breakpoint for the final range
breakpoints.append((ranges_counts[-1][0], 1.0))

# Print the breakpoints
for i, (range_start, breakpoint) in enumerate(breakpoints, start=1):
    next_range_start = ranges_counts[i][0] if i < len(ranges_counts) else None
    print(f"Breakpoint {i}: {breakpoint:.4f} (Range {range_start} - {next_range_start - 1 if next_range_start is not None else 'end'})")
