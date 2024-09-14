% Step 1: Load the image
img = imread('D:\\Program Files\\Coding\\steganography\\images\\house-enc.png'); % Replace with your image file

% Step 2: Extract the RGB channels
red_channel = img(:,:,1);
green_channel = img(:,:,2);
blue_channel = img(:,:,3);

% Step 3: Create a figure for the RGB histogram
figure;
hold on; % Allows overlapping of histograms

% Step 4: Plot histograms for each channel
% Normalize the histograms by setting the 'Normalization' option to 'probability'
histogram(red_channel(:), 256, 'FaceColor', 'r', 'EdgeColor', 'none', 'FaceAlpha', 0.8);
histogram(green_channel(:), 256, 'FaceColor', 'g', 'EdgeColor', 'none', 'FaceAlpha', 0.8);
histogram(blue_channel(:), 256, 'FaceColor', 'b', 'EdgeColor', 'none', 'FaceAlpha', 0.8);

% Step 5: Label the axes and title
xlabel('Pixel Intensity');
ylabel('Frequency');
title('RGB Histogram');

% Set the limits for the x-axis
xlim([0 255]);

% Display the legend
legend('Red Channel', 'Green Channel', 'Blue Channel');

hold off;
