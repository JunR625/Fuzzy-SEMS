import numpy as np
from skfuzzy import control as ctrl
from skfuzzy import membership as mf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Input variables
temperature = ctrl.Antecedent(np.arange(20, 40, 1), 'temperature')
time_of_day = ctrl.Antecedent(np.arange(0, 24, 1), 'time of day')
outdoor_light_intensity = ctrl.Antecedent(np.arange(0, 100, 0.5), 'outdoor light intensity')
room_size = ctrl.Antecedent(np.arange(0, 500, 10), 'room size')

# Output variables
cooling_capacity = ctrl.Consequent(np.arange(0, 10.0, 0.1), 'cooling capacity')
indoor_light_intensity = ctrl.Consequent(np.arange(0, 1000, 10), 'indoor light intensity')

# Temperature membership functions (in degrees Celcius)
temperature['cool'] = mf.trimf(temperature.universe, [20, 20, 25])
temperature['comfortable'] = mf.trimf(temperature.universe, [20, 25, 30])
temperature['warm'] = mf.trimf(temperature.universe, [25, 30, 35])
temperature['hot'] = mf.trapmf(temperature.universe, [30, 35, 40, 40])
# temperature.view()

# Time of day membership functions (24-hour format)
time_of_day['daytime'] = mf.trapmf(time_of_day.universe, [7, 10, 17, 19])
nighttime_mf1 = mf.trapmf(time_of_day.universe, [0, 0, 6, 10])
nighttime_mf2 = mf.trapmf(time_of_day.universe, [18, 20, 24, 24])
time_of_day['nighttime'] = np.maximum(nighttime_mf1, nighttime_mf2)
# time_of_day.view()

# Light level membership functions (in klux)
outdoor_light_intensity['low'] = mf.trimf(outdoor_light_intensity.universe, [0, 0, 35])
outdoor_light_intensity['medium'] = mf.trimf(outdoor_light_intensity.universe, [25, 50, 75])
outdoor_light_intensity['high'] = mf.trimf(outdoor_light_intensity.universe, [70, 100, 100])
# outdoor_light_intensity.view()

# Room size membership functions (in square meters)
room_size['small'] = mf.trimf(room_size.universe, [0, 0, 100])
room_size['medium'] = mf.trimf(room_size.universe, [50, 200, 300])
room_size['large'] = mf.trimf(room_size.universe, [300, 400, 500])
room_size['very large'] = mf.trimf(room_size.universe, [400, 500, 500])
# room_size.view()

# Cooling capacity membership functions (in kW)
cooling_capacity['off'] = mf.trimf(cooling_capacity.universe, [0, 0, 0])
cooling_capacity['low'] = mf.trapmf(cooling_capacity.universe, [0, 0.1, 2, 3.5])
cooling_capacity['medium'] = mf.trimf(cooling_capacity.universe, [3, 5, 7])
cooling_capacity['high'] = mf.trimf(cooling_capacity.universe, [6.5, 8, 9.5])
cooling_capacity['maximum'] = mf.trimf(cooling_capacity.universe, [9, 10, 10])
# cooling_capacity.view()

# Light intensity membership functions (in lux)
indoor_light_intensity['off'] = mf.trimf(indoor_light_intensity.universe, [0, 0, 0]) 
indoor_light_intensity['low'] = mf.trapmf(indoor_light_intensity.universe, [0, 1, 200, 400])
indoor_light_intensity['medium'] = mf.trimf(indoor_light_intensity.universe, [300, 500, 700])
indoor_light_intensity['high'] = mf.trapmf(indoor_light_intensity.universe, [600, 800, 1000, 1000])
# indoor_light_intensity.view()

# Rule for night - AC always off and lights off regardless of other conditions
rule1 = ctrl.Rule(time_of_day['nighttime'],
                  (cooling_capacity['off'], indoor_light_intensity['off']))

# All other rule combinations
rule2 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['small'],
                  (cooling_capacity['low'], indoor_light_intensity['medium']))
rule3 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['small'],
                  (cooling_capacity['low'], indoor_light_intensity['low']))
rule4 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['small'],
                  (cooling_capacity['low'], indoor_light_intensity['off']))
rule5 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['medium'],
                  (cooling_capacity['low'], indoor_light_intensity['high']))
rule6 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['medium'],
                  (cooling_capacity['low'], indoor_light_intensity['medium']))
rule7 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['medium'],
                  (cooling_capacity['low'], indoor_light_intensity['low']))
rule8 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['large'],
                  (cooling_capacity['medium'], indoor_light_intensity['high']))
rule9 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['large'],
                  (cooling_capacity['medium'], indoor_light_intensity['high']))
rule10 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['large'],
                   (cooling_capacity['medium'], indoor_light_intensity['medium']))
rule11 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['very large'],
                   (cooling_capacity['medium'], indoor_light_intensity['high']))
rule12 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['very large'],
                   (cooling_capacity['medium'], indoor_light_intensity['high']))
rule13 = ctrl.Rule(temperature['cool'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['very large'],
                   (cooling_capacity['medium'], indoor_light_intensity['medium']))
rule14 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['small'],
                  (cooling_capacity['low'], indoor_light_intensity['medium']))
rule15 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['small'],
                  (cooling_capacity['low'], indoor_light_intensity['low']))
rule16 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['small'],
                  (cooling_capacity['low'], indoor_light_intensity['off']))
rule17 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['medium'],
                  (cooling_capacity['low'], indoor_light_intensity['high']))
rule18 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['medium'],
                  (cooling_capacity['low'], indoor_light_intensity['medium']))
rule19 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['medium'],
                  (cooling_capacity['low'], indoor_light_intensity['low']))
rule20 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['large'],
                  (cooling_capacity['medium'], indoor_light_intensity['high']))
rule21 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['large'],
                  (cooling_capacity['medium'], indoor_light_intensity['high']))
rule22 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['large'],
                   (cooling_capacity['medium'], indoor_light_intensity['medium']))
rule23 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['very large'],
                   (cooling_capacity['high'], indoor_light_intensity['high']))
rule24 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['very large'],
                   (cooling_capacity['high'], indoor_light_intensity['high']))
rule25 = ctrl.Rule(temperature['comfortable'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['very large'],
                   (cooling_capacity['high'], indoor_light_intensity['medium']))
rule26 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['small'],
                   (cooling_capacity['low'], indoor_light_intensity['medium']))
rule27 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['small'],
                   (cooling_capacity['low'], indoor_light_intensity['low']))
rule28 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['small'],
                   (cooling_capacity['low'], indoor_light_intensity['off']))
rule29 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['medium'],
                   (cooling_capacity['medium'], indoor_light_intensity['high']))
rule30 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['medium'],
                   (cooling_capacity['medium'], indoor_light_intensity['medium']))
rule31 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['medium'],
                   (cooling_capacity['medium'], indoor_light_intensity['low']))
rule32 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['large'],
                   (cooling_capacity['high'], indoor_light_intensity['high']))
rule33 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['large'],
                   (cooling_capacity['high'], indoor_light_intensity['high']))
rule34 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['large'],
                   (cooling_capacity['high'], indoor_light_intensity['medium']))
rule35 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['very large'],
                   (cooling_capacity['maximum'], indoor_light_intensity['high']))
rule36 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['very large'],
                   (cooling_capacity['maximum'], indoor_light_intensity['high']))
rule37 = ctrl.Rule(temperature['warm'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['very large'],
                   (cooling_capacity['maximum'], indoor_light_intensity['medium']))
rule38 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['small'],
                   (cooling_capacity['medium'], indoor_light_intensity['medium']))
rule39 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['small'],
                   (cooling_capacity['medium'], indoor_light_intensity['low']))
rule40 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['small'],
                   (cooling_capacity['medium'], indoor_light_intensity['off']))
rule41 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['medium'],
                   (cooling_capacity['high'], indoor_light_intensity['high']))
rule42 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['medium'],
                   (cooling_capacity['high'], indoor_light_intensity['medium']))
rule43 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['medium'],
                   (cooling_capacity['high'], indoor_light_intensity['low']))
rule44 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['large'],
                   (cooling_capacity['maximum'], indoor_light_intensity['high']))
rule45 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['large'],
                   (cooling_capacity['maximum'], indoor_light_intensity['high']))
rule46 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['large'],
                   (cooling_capacity['maximum'], indoor_light_intensity['medium']))
rule47 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['low'] & room_size['very large'],
                   (cooling_capacity['maximum'], indoor_light_intensity['high']))
rule48 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['medium'] & room_size['very large'],
                   (cooling_capacity['maximum'], indoor_light_intensity['high']))
rule49 = ctrl.Rule(temperature['hot'] & time_of_day['daytime'] & outdoor_light_intensity['high'] & room_size['very large'],
                   (cooling_capacity['maximum'], indoor_light_intensity['medium']))

rules = []
for i in range(1, 50):
    rule = globals().get(f'rule{i}')  
    if rule is not None:
        rules.append(rule)
        
sems_ctrl = ctrl.ControlSystem(rules=rules)
sems = ctrl.ControlSystemSimulation(control_system=sems_ctrl)

def get_input():
    while True:
        try:
            temp = float(input("Temperature (20-40°C): "))
            time = float(input("Time of day (0-24 hours): "))
            light = float(input("Outdoor light intensity (0-100 klux): "))
            size = float(input("Room size (0-500 square meters): "))
            
            if (20 <= temp <= 40 and 0 <= time <= 24 and 
                0 <= light <= 100 and 0 <= size <= 500):
                return temp, time, light, size
            else:
                print("Please enter values within the specified limits!\n")
        except ValueError:
            print("Please enter valid numeric values!\n")
            
def compute_results(temp, time, light, size, smse):
    # Set inputs and compute
    sems.input['temperature'] = temp
    sems.input['time of day'] = time
    sems.input['outdoor light intensity'] = light
    sems.input['room size'] = size
    sems.compute()
    
    print("\nResults:")
    print(f"Cooling Capacity: {smse.output['cooling capacity']:.2f} kW")
    print(f"Indoor Light Intensity: {smse.output['indoor light intensity']:.2f} lux")
    
def plot_membership_functions(cooling_capacity, indoor_light_intensity, sems):
    plt.close('all')
    print("\nShowing membership function plots...")
    cooling_capacity.view(sim=sems)
    indoor_light_intensity.view(sim=sems)
    plt.show()

def create_3d_plot(temp, time, light, size):
    # Get user choices for x and y variables
    input_vars = {
        'temperature': {'var': temperature, 'value': temp, 'min': 20, 'max': 40},
        'time of day': {'var': time_of_day, 'value': time, 'min': 0, 'max': 24},
        'outdoor light intensity': {'var': outdoor_light_intensity, 'value': light, 'min': 0, 'max': 100},
        'room size': {'var': room_size, 'value': size, 'min': 0, 'max': 500}
    }
    
    print("\nSelect variables for 3D plot:")
    print("Choose first input variable (x-axis):")
    for i, var in enumerate(input_vars.keys(), 1):
        print(f"{i}. {var}")
    x_choice = int(input("Enter choice (1-4): "))
    x_var = list(input_vars.keys())[x_choice-1]
    
    remaining_vars = [var for var in input_vars.keys() if var != x_var]
    print("\nChoose second input variable (y-axis):")
    for i, var in enumerate(remaining_vars, 1):
        print(f"{i}. {var}")
    y_choice = int(input("Enter choice (1-3): "))
    y_var = remaining_vars[y_choice-1]

    # Ask which output to plot before calculating
    print("\nWhich output to plot?")
    print("1. Cooling Capacity")
    print("2. Indoor Light Intensity")
    print("3. Both")
    output_choice = int(input("Enter choice (1-3): "))
    
    # Create meshgrid
    x, y = np.meshgrid(np.linspace(input_vars[x_var]['min'], input_vars[x_var]['max'], 100),
                       np.linspace(input_vars[y_var]['min'], input_vars[y_var]['max'], 100))
    
    # Only create arrays for the chosen output(s)
    if output_choice in [1, 3]:
        z_cooling = np.zeros_like(x, dtype=float)
    if output_choice in [2, 3]:
        z_light = np.zeros_like(x, dtype=float)
    
    # Get fixed values from previously entered inputs
    fixed_values = {var: info['value'] for var, info in input_vars.items() if var not in [x_var, y_var]}
    
    print("\nCalculating and plotting 3D graph...")
    for i, r in enumerate(x):
        for j, c in enumerate(r):
            sems.input[x_var] = x[i,j]
            sems.input[y_var] = y[i,j]
            for var, value in fixed_values.items():
                sems.input[var] = value
            try:
                sems.compute()
                if output_choice in [1, 3]:
                    z_cooling[i,j] = sems.output['cooling capacity']
                if output_choice in [2, 3]:
                    z_light[i,j] = sems.output['indoor light intensity']
            except:
                if output_choice in [1, 3]:
                    z_cooling[i,j] = float('inf')
                if output_choice in [2, 3]:
                    z_light[i,j] = float('inf')
    
    if output_choice in [1, 3]:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(x, y, z_cooling, rstride=1, cstride=1, 
                             cmap='viridis', linewidth=0.4, antialiased=True)
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        ax.set_zlabel('Cooling Capacity (kW)')
        ax.set_title(f'Cooling Capacity vs {x_var} and {y_var}')
        plt.colorbar(surf)
        plt.show()
    
    if output_choice in [2, 3]:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(x, y, z_light, rstride=1, cstride=1, 
                             cmap='viridis', linewidth=0.4, antialiased=True)
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        ax.set_zlabel('Indoor Light Intensity (lux)')
        ax.set_title(f'Indoor Light Intensity vs {x_var} and {y_var}')
        plt.colorbar(surf)
        plt.show()

if __name__ == "__main__":
    print("="*75)
    print("\n                 Smart Energy Management System                 ")
    print("\n" + "="*75 + "\n")
    
    while True:
        # Get inputs and compute results
        temp, time, light, size = get_input()
        compute_results(temp, time, light, size, sems)
        
        # Show membership functions
        plot_membership_functions(cooling_capacity, indoor_light_intensity, sems)
        
        # Ask about 3D plot
        plot_3d = input("\nWould you like to see a 3D surface plot? (yes/no): ").lower()
        if plot_3d == 'yes':
            create_3d_plot(temp, time, light, size)
        
        # Ask to try again
        check_again = input("\nWould you like to try again? (yes/no): ").lower()
        if check_again != 'yes':
            print("\nThank you for using the Smart Energy Management System!")
            break
