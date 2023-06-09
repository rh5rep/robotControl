import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path_to_save = 'C:/Users/hannar1/OneDrive - Wentworth Institute of Technology/Capstone/2023/Software/Load Sensor Data Collection/'
test_name = '30_min_drift_test_no_tare'
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

with open(filename, "r") as file:
    lines = file.readlines()
    for line in lines:
        # print('tru')

        if "Readings:" in line:
            found_readings = True
            continue
        if found_readings and "average:" in line:
            if "average:" in line:
                value = float(line.split("average:")[1])
                count2 +=1
                if value > -5:
                    count +=1
                    above_25 += value
                    average_weight =above_25/count
                    above_25_array.append(value)
                    # average_weight = value/count
                # print(average_weight)
                # print()
                averages.append(value)
    min_length = count2
    print(f'our average mass over {count} readings is: {average_weight}\n')
    print(f'std test {np.std(above_25_array)}')

plt.plot(averages)
plt.title(f'Load Sensor Readings  | Average Mass: {average_weight:.2f} | Total Samples of ~50g: {count} | STD: {np.std(above_25_array):.2f}')
plt.xlabel('Time (seconds)')
plt.ylabel(f'Mass (g)')
plt.show()

above_25_array = np.array(above_25_array)
above_25_array.resize(min_length)

# Create a pandas dataframe with the variables
data = {'averages': averages, 'above_25_array': above_25_array}
df = pd.DataFrame(data)

# Save the dataframe to an Excel file
writer = pd.ExcelWriter(f'{path_to_save}{test_name}.xlsx')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.close()
