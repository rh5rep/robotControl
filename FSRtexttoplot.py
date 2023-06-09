import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path_to_save = 'C:/Users/hannar1/OneDrive - Wentworth Institute of Technology/Capstone/2023/Software/Load Sensor Data Collection/Flexiforcetest1/'
test_name = 'flexiforcetest_incrementingweights1'
# filename = "C:/Users/hannar1/OneDrive - Wentworth Institute of Technology/Capstone/2023/Software/Load Sensor Data Collection/loadcelltest_50.log"
filename = f"{path_to_save}{test_name}.log"

averages = []
found_readings = False
count = 0
count2 = 0
above_25 = 0
average_weight = 0;
above_25_array = []
min_length = 0
weight = []
time = []

with open(filename, "r") as file:
    lines = file.readlines()
    for line in lines:
        try:
            values = line.split(" | ")
            force = values[0].split(": ")[1]
            weight.append(force)
            times = values[1].split(": ")[1]
            time.append(times)
            cap = values[2].split(": ")[1]
        except (ValueError, IndexError) as e:
            # handle the error
            print(f"Error processing line: {line.strip()} ({str(e)})")
            continue

plt.plot(time, weight)
# plt.title(f'Load Sensor Readings  | Average Weight: {average_weight:.2f} | Total Samples of ~50g: {count} | STD: {np.std(above_25_array):.2f}')
plt.xlabel('Time (seconds)')
plt.ylabel(f'Weight (lbs)')
plt.show()

weight = np.array(weight)
weight.astype(float)
time = np.array(time)
time.astype(float)

# weight.resize(min_length)

# # Create a pandas dataframe with the variables
data = {'Weight (g)': weight, 'Time (s)': time}
df = pd.DataFrame(data)
#
# # Save the dataframe to an Excel file
writer = pd.ExcelWriter(f'{path_to_save}{test_name}.xlsx')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.close()
