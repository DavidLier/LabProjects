clear all; close all; clc;

dataDirectory = 'C:\Users\PL003A\Desktop\Concussion Analysis';
fileID = fopen('f1Scores.txt');
scoresFile = textscan(fileID,'%s','delimiter','\n');
currentLine = scoresFile{1}{1}; 
scores = str2double(strsplit(currentLine, ","));
scores = scores * 100;

binEdges = 70:5:100;

figure;
h = histogram(scores, ...
    'BinEdges', binEdges, ...
    'FaceColor', [0.1 0.4 0.7], ... % Sky bluish color
    'EdgeColor', 'k');                

xlim([40 100]);
xticks(40:10:100);
box on; 

avg = mean(scores); 

x1 = xline(avg, 'r', 'LineWidth', 2);
x1.Label = sprintf('Average = %.1f %%', avg); 
x1.LabelVerticalAlignment = 'middle';
x1.LabelHorizontalAlignment = 'center';
x1.FontSize = 12;
x1.Color = 'r';           
x1.LabelColor = 'k'; 
x1.FontName = 'Open Sans';          

x2 = xline(50, '--r', 'LineWidth', 2);
x2.Label = 'Value expected by chance';
x2.LabelVerticalAlignment = 'middle';
x2.LabelHorizontalAlignment = 'center';
x2.FontSize = 12;
x2.Color = 'r';
x2.LabelColor = 'k'; 
x2.FontName = 'Open Sans';

set(gcf, 'Color', 'w');
set(gca, 'TickDir', 'out', ...          
         'Box', 'off', ...              
         'XAxisLocation', 'bottom', ...
         'YAxisLocation', 'left');

set(gca, 'FontName', 'Arial', ...
         'FontWeight', 'normal', ...
         'FontSize', 12);  

xlabel('F1 Score [%]', 'FontName', 'Arial', 'FontWeight', 'normal', 'FontSize', 14);
ylabel('Frequency',     'FontName', 'Arial', 'FontWeight', 'normal', 'FontSize', 14);

print(gcf, 'my_histogram', '-dpng', '-r300');  % 300 DPI PNG
