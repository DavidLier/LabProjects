# This is still the prelim data but I need to account for multiple comparisons next I update this when we start updating the stats section (though nothing was significant anyway but maybe something changes with additional data sets)

import os;
import numpy as np
import pandas as pd;
from scipy.stats import ttest_rel
from Figure import Figure

def createFigure(title, barLabels, groupNames, toPlotVals, toPlotErrs, yLabel, pValues, lowerYLim, upperYLim, increment):
    fig = Figure(
        title = title,
        givenLabels = barLabels,
        givenXLabels = groupNames,
        givenValues = toPlotVals,
        givenErrors = toPlotErrs,
        yLabel = yLabel,
        subTexts = pValues
    );
    
    fig.plot(
        width = 0.2,
        offset = 0.05,
        colorOne = "#1A80BB",
        colorTwo = "#EB801C",
        lowerYLim = lowerYLim,
        upperYLim = upperYLim,
        increments = increment
    );

def analyzeSets(df, lower, upper, colA, colB):
    first = df.iloc[lower:upper, colA].dropna();
    second = df.iloc[lower:upper, colB].dropna();
    
    tStat, pValue = ttest_rel(first, second);
    
    printInfo(df, first, second, pValue, colA, colB);
    
    return (first.mean(), second.mean()), (first.sem(), second.sem()), pValue;


def printInfo(mainDF, firstSet, secondSet, pValue, colA, colB):
    print("Comparing: ", mainDF.columns[colA], " and ", mainDF.columns[colB]);
    print("Averages 1:", round(firstSet.mean(), 2), "±", round(firstSet.sem(), 2),
          " 2:", round(secondSet.mean(), 2), "±", round(secondSet.sem(), 2),
          " p =", round(pValue, 4));
    

dataDirectory = "C:/Users/PL003A/Desktop/Heart Contraction/";

# Relevant Files
accuracyFile = "AccuracySummary.xlsx";
reactionFile = "ReactionTimeSummary.xlsx";

accuracyDF = pd.read_excel(accuracyFile);
reactionDF = pd.read_excel(reactionFile);

divider = "P298";
dividerIndex = 0;
for i in range(len(accuracyDF["Subject"])):
    if (accuracyDF["Subject"][i] == divider):
        dividerIndex = i + 1;
        
                              
ranges = [
         (0, len(accuracyDF)), 
         (0, dividerIndex), 
         (dividerIndex, len(accuracyDF))
         ];    
         
selectedRanges = {
                 "100ms & 200ms Combined": ranges[0], 
                 "100ms Only": ranges[1], 
                 "200ms Only": ranges[2]
                 };

for selectedRange in selectedRanges:
    lowerBound = selectedRanges[selectedRange][0];   
    upperBound = selectedRanges[selectedRange][1];
    
    print("---------------------------");
    print("In range: ", selectedRange);
    
    barLabels = ["Systolic", "Diastolic"];

    toPlotVals = [];
    toPlotErrs = [];
    pValues = [];  
    for colA, colB in [(1,2), (9,10)]: # FACES & SYMBOLS - OVERALLS FOR EACH RANGE 
        vals, errs, p = analyzeSets(accuracyDF, lowerBound, upperBound, colA, colB);
    
        toPlotVals.append(vals);
        toPlotErrs.append(errs);
        pValues.append(f"p={round(p,3)}");
    
    groupNames = ["Faces", "Symbols"]
    createFigure((f"Average Systolic and Diastolic Accuracies for Both Paradigms - {selectedRange}"),
              barLabels, groupNames, toPlotVals, toPlotErrs, 
              "Accuracy (%)", 
              pValues, 
              0, 
              100, 
              10);
    
    toPlotVals = [];
    toPlotErrs = [];
    pValues = [];
    for colA, colB in [(3, 4), (5, 6), (7, 8)]: # INDIVIDUAL EMOTIONS FOR EACH RANGE
        vals, errs, p = analyzeSets(accuracyDF, lowerBound, upperBound, colA, colB);            
        
        toPlotVals.append(vals);
        toPlotErrs.append(errs);
        pValues.append(f"p={round(p,3)}");
        
    groupNames = ["Angry", "Fearful", "Sad"];
    createFigure((f"Average Systolic and Diastolic Accuracies for Each Emotion - {selectedRange}"),
              barLabels, groupNames, toPlotVals, toPlotErrs, 
              "Accuracy (%)", 
              pValues, 
              0, 
              100, 
              10);                
    
    toPlotVals = [];
    toPlotErrs = [];
    pValues = [];
    for colA, colB in [(11, 12), (13, 14), (15, 16)]: # INDIVIDUAL SYMBOLS FOR EACH RANGE
        vals, errs, p = analyzeSets(accuracyDF, lowerBound, upperBound, colA, colB);            
        
        toPlotVals.append(vals);
        toPlotErrs.append(errs);
        pValues.append(f"p={round(p,3)}");
        
    groupNames = ["✖", "◆", "✚"]
    createFigure((f"Average Systolic and Diastolic Accuracies for Each Symbol - {selectedRange}"),
              barLabels, groupNames, toPlotVals, toPlotErrs, 
              "Accuracy (%)", 
              pValues, 
              0, 
              100, 
              10);          

for selectedRange in selectedRanges:
    lowerBound = selectedRanges[selectedRange][0];   
    upperBound = selectedRanges[selectedRange][1];
    
    print("---------------------------");
    print("In range: ", selectedRange);
    
    barLabels = ["Systolic", "Diastolic"];

    toPlotVals = [];
    toPlotErrs = [];
    pValues = [];  
    for colA, colB in [(1,2), (9,10)]: # FACES & SYMBOLS - OVERALLS FOR EACH RANGE 
        vals, errs, p = analyzeSets(reactionDF, lowerBound, upperBound, colA, colB);
    
        toPlotVals.append(vals);
        toPlotErrs.append(errs);
        pValues.append(f"p={round(p,3)}");
    
    groupNames = ["Faces", "Symbols"]
    createFigure((f"Average Systolic and Diastolic Reaction Times for Both Paradigms - {selectedRange}"),
              barLabels, groupNames, toPlotVals, toPlotErrs, 
              "Reaction Time (ms)", 
              pValues, 
              1000, 
              1500, 
              100);
    
    
    
    toPlotVals = [];
    toPlotErrs = [];
    pValues = [];
    for colA, colB in [(3, 4), (5, 6), (7, 8)]: # INDIVIDUAL EMOTIONS FOR EACH RANGE
        vals, errs, p = analyzeSets(reactionDF, lowerBound, upperBound, colA, colB);            
        
        toPlotVals.append(vals);
        toPlotErrs.append(errs);
        pValues.append(f"p={round(p,3)}");
        
    groupNames = ["Angry", "Fearful", "Sad"]
    createFigure((f"Average Systolic and Diastolic Reaction Times for Each Emotion - {selectedRange}"),
              barLabels, groupNames, toPlotVals, toPlotErrs, 
              "Reaction Time (ms)", 
              pValues, 
              1000, 
              1500, 
              100);             
    
    
    toPlotVals = [];
    toPlotErrs = [];
    pValues = [];
    for colA, colB in [(11, 12), (13, 14), (15, 16)]: # INDIVIDUAL SYMBOLS FOR EACH RANGE
        vals, errs, p = analyzeSets(reactionDF, lowerBound, upperBound, colA, colB);            
        
        toPlotVals.append(vals);
        toPlotErrs.append(errs);
        pValues.append(f"p={round(p,3)}");
        
    groupNames = ["✖", "◆", "✚"]
    createFigure((f"Average Systolic and Diastolic Reaction Times for Each Symbol - {selectedRange}"),
              barLabels, groupNames, toPlotVals, toPlotErrs, 
              "Reaction Time (ms)", 
              pValues, 
              1000, 
              1500, 
              100);