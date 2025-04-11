% Given ramp histogram for a 4-bit ADC (codes 0 to 15)
histogram = [43, 115, 85, 101, 122, 170, 75, 146, 125, 60, 95, 95, 115, 40, 120, 242];

% Define codes (0 to 15) for a 4-bit ADC
num_codes = length(histogram);  % 16 codes (0 to 15)
codes = 0:(num_codes-1);  % Codes 0 to 15

% Step 1: Compute total counts
total_counts = sum(histogram);  % 1749

% Step 2: Compute transition levels (in counts)
% T(k) is the cumulative sum of counts up to code k-1
% T(1) = 0 (before code 0), T(2) = histogram(1), ..., T(16) = sum(histogram(1:15))
cumulative_counts = cumsum(histogram);
transition_levels_counts = [0, cumulative_counts(1:end-1)];  % T(1) to T(16)

% Step 3: End-point correction to eliminate offset and full-scale errors
% The ideal transfer function after end-point correction is a straight line from T(1) to T(16)
% T(1) corresponds to code 0, T(16) corresponds to code 15
% Normalize transition levels to the range [0, 15] (codes 0 to 15)
T_start = transition_levels_counts(1);  % 0
T_end = transition_levels_counts(end);  % sum(histogram(1:15)) = 1507
% Linear mapping: T_corrected = a * T + b, where T_corrected(1) = 0, T_corrected(16) = 15
a = (15 - 0) / (T_end - T_start);  % Slope
b = 0 - a * T_start;  % Intercept
transition_levels_corrected = a * transition_levels_counts + b;

% Step 4: Compute DNL
% DNL(k) = (T(k+1) - T(k)) - 1 LSB
% After correction, 1 LSB = 1 code (since T_corrected ranges from 0 to 15 over 15 steps)
dnl = zeros(1, num_codes);
for k = 1:(num_codes-1)
    step_size = transition_levels_corrected(k+1) - transition_levels_corrected(k);
    dnl(k) = step_size - 1;  % Ideal step size = 1 code (1 LSB)
end
% DNL for the last code (15) is typically not defined or set to 0
dnl(end) = 0;

% Step 5: Compute INL
% INL(k) = T_corrected(k) - ideal_code(k)
% Ideal code for T(k) is (k-1), since T(k) is the transition to code (k-1)
ideal_codes = 0:(num_codes-1);  % Ideal codes for T(1) to T(16) are 0 to 15
inl = transition_levels_corrected - ideal_codes;
% Adjust INL to ensure INL(0) = 0 and INL(15) = 0 (already satisfied by correction)

% Step 6: Peak DNL and INL
peak_dnl = max(abs(dnl));
peak_inl = max(abs(inl));

% Step 7: Check monotonicity
is_monotonic = all(dnl > -1);

% Display results
disp('Part (a): DNL and INL')
disp('DNL (LSB):')
disp(dnl)
disp('INL (LSB):')
disp(inl)

disp('Part (b): Peak DNL and INL')
fprintf('Peak DNL: %.4f LSB\n', peak_dnl)
fprintf('Peak INL: %.4f LSB\n', peak_inl)

disp('Part (c): Monotonicity')
if is_monotonic
    disp('The ADC is monotonic (DNL > -1 LSB for all codes).')
else
    disp('The ADC is NOT monotonic (DNL <= -1 LSB for some codes).')
end

% Plotting
figure('Position', [100, 100, 1200, 800]);

% Plot 1: Ramp Histogram
subplot(2, 2, 1);
bar(codes, histogram, 'FaceColor', 'b');
xlabel('Code');
ylabel('Counts');
title('Ramp Histogram');
grid on;

% Plot 2: Transition Levels
subplot(2, 2, 2);
plot(1:num_codes, transition_levels_corrected, 'r-o', 'MarkerSize', 5);
xlabel('Transition Index (T_k)');
ylabel('Code');
title('Corrected Transition Levels');
grid on;

% Plot 3: DNL vs. Code
subplot(2, 2, 3);
plot(codes, dnl, 'r-o', 'MarkerSize', 5, 'LineWidth', 1.5);
xlabel('Code');
ylabel('LSB');
title('DNL');
grid on;
hold on;
plot(codes, -1*ones(size(codes)), 'k--', 'LineWidth', 1);
hold off;
ylim([-0.7, 0.7]);

% Plot 4: INL vs. Code
subplot(2, 2, 4);
plot(codes, inl, 'r-o', 'MarkerSize', 5, 'LineWidth', 1.5);
xlabel('Code');
ylabel('LSB');
title('INL');
grid on;
ylim([-1, 1.1]);

sgtitle('4-Bit ADC Characterization Using Ramp Histogram');
