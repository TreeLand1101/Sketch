def calculate_elephant_mice_sums(file_path, threshold):
    elephant_sum = 0
    mice_sum = 0
    total_sum = 0

    elephant_count = 0 
    mice_count = 0 

    with open(file_path, 'r') as file:
        for line in file:
            count = int(line.strip())
            total_sum += count

            if count >= threshold:
                elephant_sum += count
                elephant_count += 1
            else:
                mice_sum += count
                mice_count += 1

    elephant_ratio = elephant_sum / total_sum if total_sum > 0 else 0
    mice_ratio = mice_sum / total_sum if total_sum > 0 else 0

    return elephant_sum, mice_sum, elephant_ratio, mice_ratio, elephant_count, mice_count

file_path = 'memory_500000_threshold_0.000100_all.txt'
threshold = 3216 

elephant_sum, mice_sum, elephant_ratio, mice_ratio, elephant_count, mice_count = calculate_elephant_mice_sums(file_path, threshold)
print(f"Elephant sum: {elephant_sum}")
print(f"Mice sum: {mice_sum}")
print(f"Elephant ratio: {elephant_ratio:.2%}")
print(f"Mice ratio: {mice_ratio:.2%}")
print(f"Elephant flow count: {elephant_count}")
print(f"Mice flow count: {mice_count}")
