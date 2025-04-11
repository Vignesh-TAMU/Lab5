import numpy as np
import matplotlib.pyplot as plt

# Given data
Vref = 1.0  # Full-scale reference voltage (not directly used here, but for context)
LSB = 0.1  # Ideal LSB = 100 mV
codes = np.arange(8)  # Codes 0 to 7
ideal_outputs = codes * LSB  # Ideal outputs: [0, 0.1, 0.2, ..., 0.7] V
actual_outputs = np.array([-0.01, 0.105, 0.195, 0.28, 0.37, 0.48, 0.6, 0.75])  # Measured outputs

# Part (c): End-Point Correction, DNL, and INL

# Step 1: Offset correction (make actual output at code 0 = 0 V)
offset = actual_outputs[0]  # -0.01 V
offset_corrected = actual_outputs - offset  # Add 0.01 V to all outputs
print("Offset-corrected outputs (V):", offset_corrected)

# Step 2: Gain correction (make actual output at code 7 = 0.7 V)
actual_at_code7 = offset_corrected[-1]  # 0.76 V
ideal_at_code7 = ideal_outputs[-1]  # 0.7 V
gain = ideal_at_code7 / actual_at_code7  # 0.7 / 0.76 ≈ 0.92105
corrected_outputs = offset_corrected * gain
print("End-point corrected outputs (V):", corrected_outputs)

# Step 3: Compute end-point corrected codes
corrected_codes = corrected_outputs / LSB
print("End-point corrected codes:", corrected_codes)

# Step 4: Compute DNL
# DNL = (corrected code at k - corrected code at k-1) - 1 LSB (in codes)
dnl = np.zeros_like(codes, dtype=float)
for k in range(1, len(codes)):
    step_size = corrected_codes[k] - corrected_codes[k-1]
    dnl[k] = step_size - 1  # Ideal step size = 1 code (1 LSB)
dnl[0] = 0  # DNL at code 0 is typically 0 or undefined
print("DNL (LSB):", dnl)

# Step 5: Compute INL
# INL = corrected code - ideal code
inl = corrected_codes - codes
print("INL (LSB):", inl)

# Part (d): Maximum DNL and INL
max_dnl = np.max(np.abs(dnl))
max_inl = np.max(np.abs(inl))
print("\nPart (d):")
print(f"Maximum DNL: {max_dnl:.4f} LSB")
print(f"Maximum INL: {max_inl:.4f} LSB")

# Plotting
plt.figure(figsize=(12, 10))

# Plot 1: Ideal vs. Actual Outputs
plt.subplot(2, 2, 1)
plt.plot(codes, ideal_outputs, 'b-o', label='Ideal Output', markersize=5)
plt.plot(codes, actual_outputs, 'r-o', label='Actual Output', markersize=5)
plt.xlabel('Code')
plt.ylabel('Output Voltage (V)')
plt.title('Ideal vs. Actual Outputs')
plt.grid(True)
plt.legend()

# Plot 2: End-Point Corrected Outputs
plt.subplot(2, 2, 2)
plt.plot(codes, ideal_outputs, 'b-o', label='Ideal Output', markersize=5)
plt.plot(codes, corrected_outputs, 'g-o', label='Corrected Output', markersize=5)
plt.xlabel('Code')
plt.ylabel('Output Voltage (V)')
plt.title('Ideal vs. End-Point Corrected Outputs')
plt.grid(True)
plt.legend()

# Plot 3: DNL vs. Code
plt.subplot(2, 2, 3)
plt.plot(codes, dnl, 'm-o', markersize=5)
plt.xlabel('Code')
plt.ylabel('DNL (LSB)')
plt.title('Differential Non-Linearity (DNL)')
plt.grid(True)
plt.axhline(0, color='black', linestyle='--', alpha=0.3)

# Plot 4: INL vs. Code
plt.subplot(2, 2, 4)
plt.plot(codes, inl, 'c-o', markersize=5)
plt.xlabel('Code')
plt.ylabel('INL (LSB)')
plt.title('Integral Non-Linearity (INL)')
plt.grid(True)
plt.axhline(0, color='black', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()
