symbols = ['✖', '✚', '◆'];
background = '✸';

xSize = 8;
ySize = 3;

matrix = [];

arr = [];
for i = 1:xSize
    arr = [arr, background];
end

for i = 1:ySize
    matrix = [matrix; arr];
end

allMatrices = {};
for j = 1:length(symbols)
    for i = 1:xSize*ySize
        curMatrix = matrix;
    
        index = i;
        column = floor(i/xSize) + 1;
    
        if column > ySize
            break
        end
    
        curMatrix(column, (index + 1 - (xSize*(column-1)))) = symbols(j);
        allMatrices = [allMatrices, curMatrix];
    end
end

% Add the missing ones manually
for i = 1:length(symbols)
    curMatrix = matrix;
    curMatrix(1, 1) = symbols(i);
    allMatrices = [allMatrices, curMatrix];
end

outputFolder = 'Symbol Images';

for k = 1:length(allMatrices)
    mat = allMatrices{k};

    fig = figure('Visible', 'off'); 
    fig = figure('Visible', 'off', 'Units', 'inches', 'Position', [1, 1, 12, 4]); % 6×2 inches figure

    axis off;
    
    textStr = '';
    for r = 1:ySize
        textStr = [textStr, mat(r,:), newline];
    end

    text(0.5, 0.5, textStr, 'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'middle', 'FontName', 'ZapfDingbats', 'FontSize', 16);

    axis off;

    curSymbolIndex = floor(k/(xSize * ySize)) + 1;
    if curSymbolIndex > length(symbols)
        curSymbolIndex = length(symbols);
    end

    symbol = symbols(curSymbolIndex);

    filename = fullfile(outputFolder, sprintf('%s_%03d.png', symbol, k)); % Just remember 3 of them are going to be mispelled so fix it manually
    exportgraphics(gca, filename, 'BackgroundColor', 'white', 'Resolution', 900);

    close(fig);
end