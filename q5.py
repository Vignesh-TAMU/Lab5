import numpy as np
import matplotlib.pyplot as plt

# Given data
dnl = np.array([0, -0.5, 0, 0.5, -1, 0.5, 0.5, 0])  # DNL for codes 0 to 7
offset_error = 0.5  # LSB
full_scale_error = 0.5  # LSB
num_codes = 8  # 3-bit ADC: codes 0 to 7
codes = np.arange(num_codes)  # Codes 0 to 7

# Step 1: Compute actual transition levels
transition_levels = np.zeros(num_codes + 1)  # T(1) to T(9)
transition_levels[0] = 0  # Start at 0 LSB
# First transition includes offset
transition_levels[1] = 1 + offset_error  # T(2) = 1 + 0.5 = 1.5 LSB
# Compute remaining transitions using DNL
for k in range(1, num_codes):
    step_size = 1 + dnl[k-1]  # Step size = 1 + DNL(k-1)
    transition_levels[k+1] = transition_levels[k] + step_size

# Step 2: Compute INL
# Ideal transition levels (adjusted for offset)
ideal_transitions = np.arange(num_codes + 1) + offset_error  # [0, 1.5, 2.5, ..., 8.5]
# INL = actual transition level - ideal transition level
inl = transition_levels - ideal_transitions

# Print results
print("Part (a): INL (LSB)")
print(inl[:-1])  # INL for codes 0 to 7 (exclude T(9))

# Step 3: Plotting
plt.figure(figsize=(15, 5))

# Plot 1: DNL vs. Code
plt.subplot(1, 3, 1)
plt.plot(codes, dnl, 'r-o', markersize=5, linewidth=1.5, label='DNL')
plt.xlabel('Code')
plt.ylabel('DNL (LSB)')
plt.title('DNL Curve')
plt.grid(True)
plt.axhline(0, color='black', linestyle='--', alpha=0.3)
plt.ylim(-1.2, 0.8)  # Adjust y-axis for visibility
plt.xticks(codes)

# Plot 2: INL vs. Code
plt.subplot(1, 3, 2)
plt.plot(codes, inl[:-1], 'r-o', markersize=5, linewidth=1.5, label='INL')
plt.xlabel('Code')
plt.ylabel('INL (LSB)')
plt.title('INL Curve')
plt.grid(True)
plt.axhline(0, color='black', linestyle='--', alpha=0.3)
plt.ylim(-1.2, 0.5)  # Adjust y-axis for visibility
plt.xticks(codes)

# Plot 3: Transfer Curve
v_in = np.linspace(-0.5, 8.5, 1000)  # Slightly beyond the range for visualization
output_code = np.zeros_like(v_in, dtype=int)
# Determine the output code for each input voltage
for i, vin in enumerate(v_in):
    for k in range(num_codes):
        if vin < transition_levels[k+1]:
            output_code[i] = k
            break
    else:
        output_code[i] = num_codes - 1  # If vin >= T(8), output = 7

# Ideal transfer curve for comparison
v_in_ideal = np.linspace(-0.5, 8.5, 1000)
output_code_ideal = np.zeros_like(v_in_ideal, dtype=int)
ideal_transitions = np.arange(num_codes + 1) 
for i, vin in enumerate(v_in_ideal):
    for k in range(num_codes):
        if vin < ideal_transitions[k+1]:
            output_code_ideal[i] = k
            break
    else:
        output_code_ideal[i] = num_codes - 1

plt.subplot(1, 3, 3)
plt.step(v_in, output_code, 'b-', where='post', label='Actual Transfer Curve')
plt.step(v_in_ideal, output_code_ideal, 'r--', where='post', label='Ideal Transfer Curve (without offset)')
plt.xlabel('Input Voltage (LSB)')
plt.ylabel('Output Code')
plt.title('Transfer Curve of 3-Bit ADC')
plt.grid(True)
plt.legend()
plt.xticks(np.arange(0, 8, 1))
plt.yticks(np.arange(0, 8))

plt.tight_layout()
plt.show()
