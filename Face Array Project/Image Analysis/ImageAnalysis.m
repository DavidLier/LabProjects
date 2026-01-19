clear all; close all; clc;

directory = 'C:\Users\PL003A\Desktop\Variance Analysis/';

imageScores = [];
for experiment = 1:2
    stimuliDir = [directory, 'Stimuli_', num2str(experiment)]; 
    cd(stimuliDir)

    %pattern = fullfile(stimuliDir, '*.jpg');
    pattern = fullfile(stimuliDir, '*.JPG'); % exp 2 has everything caps
    images = dir(pattern);

    for j = 1:length(images)
        imgPath = fullfile(images(j).folder, images(j).name);
        fprintf(1, 'Now reading %s\n', imgPath);

        rgbImage = imread(imgPath);
        labImage = CIELABConversion(rgbImage);
        L = labImage(:,:,1);  % L* Perceptual Lightness        
        
        labLightness = mean(mean(L));
        rmsContrast = getRMSContrast(L/100);

        chroma = sqrt(labImage(:,:,2).^2 + labImage(:,:,3).^2);
        saturation = mean(chroma(:) ./ (L(:) + 1e-6));

        slope = getPowerSlope(L);

        fprintf('Perceptual Lightness/Brightness: %.2f, RMS Contrast: %.2f, Saturation/Chroma: %.2f, Fourier Slope: %.2f\n', labLightness, rmsContrast, saturation, slope);
        imageScores = [imageScores, VarianceScore(images(j).name, experiment, labLightness, rmsContrast, saturation, slope)];
    end    
end

save("C:\Users\PL003A\Desktop\Variance Analysis/ImageScores.mat", "imageScores");


function gradientImg = getGradientImage(img)
    labL = img(:, :, 1);
    labA = img(:, :, 2);
    labB = img(:, :, 3);

    gL = gradient(double(labL));
    gA = gradient(double(labA));
    gB = gradient(double(labB));

    gradientImg = zeros(1024, 1024); 
    for i = 1:1024
        for j = 1:1024
            gradientImg(i, j) = max(max(gL(i, j), gA(i, j)), gB(i, j)); 
        end
    end

    %imshow(imcomplement(imadjust(mat2gray(gradientImg))));
end

%https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0122801
function linearSlope = getPowerSlope(img)
    powerSpectrum = abs((fftshift(fft2(img)))).^2; 
    [rows, cols] = size(img);

    yCenter = floor(cols / 2);
    xCenter = yCenter;

    [x, y] = meshgrid(1:cols, 1:rows);
    r = sqrt((x - xCenter).^2 + (y - yCenter).^2); 

    r = round(r); % Have to round since zeros only accepts integer sizes
    rMax = max(r(:));
    radialProfile = zeros(1, rMax);

    for i = 1:rMax
        mask = (r == i);
        radialProfile(i) = mean(powerSpectrum(mask));
    end

    % this is cycles/image
    frequencies = (0:rMax-1) / 1024; % Matlabs dumb and indexes at 1 instead of 0, so -1

    % As defined in the paper for faces - IMPORTANT TO AVOID ARTIFACTS
    lowerRange = 10/1024;
    upperRange = 255/1024;

    freqFiltered = frequencies((frequencies >= lowerRange) & (frequencies <= upperRange));
    powerFiltered = radialProfile((frequencies >= lowerRange) & (frequencies <= upperRange));

    logFreq = log10(freqFiltered);
    logPower = log10(powerFiltered);
    
    binEdges = linspace(min(logFreq), max(logFreq), 34);  % 33 bins
    binnedFreq = [];
    binnedPower = [];

    for i = 1:length(binEdges)-1
        inside = logFreq >= binEdges(i) & logFreq < binEdges(i+1);
        if any(inside)
            binnedFreq(end+1) = mean(logFreq(inside));
            binnedPower(end+1) = mean(logPower(inside));
        end
    end

    p = polyfit(binnedFreq, binnedPower, 1);
    linearSlope = p(1);
end

function rmsContrast = getRMSContrast(img)
        img = double(img);
        avgPixelIntensity = mean(img(:));
        diffSquared = (img - avgPixelIntensity).^2;
        rmsContrast = sqrt(mean(diffSquared(:)));
end

function labImage = CIELABConversion(img)  
    img = double(img) / 255;

    linearRGB = zeros(size(img));
    for c = 1:3
        linearRGB(:,:,c) = arrayfun(@sRGBToLinear, img(:,:,c));
    end

    scaled = linearRGB * 100;
    x = scaled(:,:,1) * 0.4124 + scaled(:,:,2) * 0.3576 + scaled(:,:,3) * 0.1805;
    y = scaled(:,:,1) * 0.2126 + scaled(:,:,2) * 0.7152 + scaled(:,:,3) * 0.0722;
    z = scaled(:,:,1) * 0.0193 + scaled(:,:,2) * 0.1192 + scaled(:,:,3) * 0.9505;

    x = x / 95.047;
    y = y / 100.00;
    z = z / 108.883;

    fx = arrayfun(@xyzToLabTransform, x);
    fy = arrayfun(@xyzToLabTransform, y);
    fz = arrayfun(@xyzToLabTransform, z);

    L = (116 * fy) - 16;
    A = 500 * (fx - fy);
    B = 200 * (fy - fz);

    labImage = cat(3, L, A, B);
end

function val = sRGBToLinear(rgb)
    if rgb > 0.04045
        val = ((rgb + 0.055) / 1.055) ^ 2.4;
    else
        val = rgb / 12.92;
    end
end

function val = xyzToLabTransform(xyz)
    if (xyz > 0.008856)
        val = xyz ^ (1/3);
    else
        val = (7.787 * xyz) + (16/116);
    end
end
