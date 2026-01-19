%%
clear all; close all; clc;

for experiment = 1:2
    dataDirectory = 'C:\Users\PL003A\Desktop\Multiple Faces\Data\';
    expChar = 'h';

    if experiment == 2
        dataDirectory = 'C:\Users\PL003A\Desktop\Multiple Faces\Data3\';
        expChar = 'q';
    end
    
    paradigmAcc = [];
    paradigmReaction = [];
        
    limit = numel(dir(dataDirectory)) - 2;
    subject = 0;
    while subject ~= limit
        subject = subject + 1;

        subjectDataIndex = ['P', num2str((60 + (subject - 1))), expChar]; 
        subjectDataFolder = [dataDirectory, subjectDataIndex, '/'];
    
        if ~exist(subjectDataFolder, 'dir')
            limit = limit + 1;
            continue;
        end
        
        cd(subjectDataFolder)
    
        fileID = fopen('RESULTS_FILE.txt');
        rawResultsText = textscan(fileID,'%s','delimiter','\n');
    
        conditionColumn = 8;
        keyPressedColumn = 2;
        reactionColumn = 5;
        
        if experiment == 2
            conditionColumn = 11;
            keyPressedColumn = 5;
            reactionColumn = 8;
        end
        
        [averageAcc, accDev] = getAverageAccuracy(rawResultsText, conditionColumn, keyPressedColumn, experiment, false); 
        [averageReaction, reactionDev] = getAverageReaction(rawResultsText, reactionColumn);
    
        paradigmReaction(end + 1) = averageReaction;
        paradigmAcc(end + 1) = averageAcc;
    end

    fprintf("Experiment #%s \n", num2str(experiment));
    fprintf("Average reaction time across all participants %.4f ± %.2f\n", mean(paradigmReaction), std(paradigmReaction));
    fprintf("Average accuracy across all participants %.4f\n\n", mean(paradigmAcc));
end

function [avgReaction, reactionDev] = getAverageReaction(rawResults, col)
    reactionTimes = [];

    for i = 1:numel(rawResults{1})-1 
        currentLine = rawResults{1}{i+1}; 
        indexedLine = strsplit(currentLine);
        
        currentVal = str2double(indexedLine{col});
        currentTime = str2double(indexedLine{col-1});

        if isnan(currentVal)
            continue;
        end
    
        reactionTimes(end + 1) = (currentVal - currentTime);
    end

    avgReaction = sum(reactionTimes)/length(reactionTimes);
    reactionDev = std(reactionTimes);
end

function [avgAcc, accDev] = getAverageAccuracy(rawResults, conditionColumn, keyPressedColumn, exp, flip)
    accuracies = [];

    initialLine = 1;
    if (exp == 1)
        initialLine = 2;
    end

    for i = initialLine:numel(rawResults{1})-1 
        currentLine = rawResults{1}{i+1}; 
        indexedLine = strsplit(currentLine);

        condition = indexedLine{conditionColumn};
        keyPressed = str2double(indexedLine{keyPressedColumn});

        if isnan(keyPressed)
            continue;
        end

        isCorrect = false;
        if exp == 1
            lastLine = rawResults{1}{i}; 
            lastIndexedLine = strsplit(lastLine);

            lastCondition = lastIndexedLine{conditionColumn};

            isCorrect = ...
                (keyPressed == 1 && strcmp(condition, lastCondition)) || ...
                (keyPressed == 2 && ~strcmp(condition, lastCondition));
            %disp([lastCondition, " ", condition, " ", keyPressed, " ", isCorrect, " ", lastCondition == condition]);
        end

        if exp == 2
            oneButton = 1;
            twoButton = 2;
            
            if flip == true
                oneButton = 2;
                twoButton = 1;
            end

            isCorrect = ...
                (keyPressed == oneButton && strcmp(condition, "C1")) || ...
                (keyPressed == twoButton && ~strcmp(condition, "C1"));
        end
        
        accuracies(end + 1) = isCorrect;
    end

    avgAcc = mean(accuracies);
    accDev = std(accuracies);

    if avgAcc < .16
        avgAcc = getAverageAccuracy(rawResults, conditionColumn, keyPressedColumn, exp, true);
    end
end