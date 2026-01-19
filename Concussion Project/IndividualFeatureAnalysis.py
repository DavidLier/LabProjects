import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import mannwhitneyu
    
NanReplacementMethod = "mean" ;
crSet = pd.read_csv("C:/Users/PL003A/Desktop/Concussion Analysis/Python ML/all.csv");

for j in range(len(crSet.columns)):
    if (j < 3):
        continue;
    col = crSet.columns[j];
    for i in range(2):  
        classSeries = crSet[crSet['CONCUSSED'] == i][col].dropna();
    
        mean = classSeries.mean();
        median = classSeries.median();
        mode = classSeries.mode().mean(); # Deals with ties
    
        val = 0;
        match NanReplacementMethod:
            case "mean":
                val = mean;
            case "median":
                val = median;
            case "mode":
                val = mode;
    
        newCol = np.where(crSet[col].isnull(), val, crSet[col]);
        crSet[col] = newCol;
    
    data = crSet[col];
    crSetSorted = crSet.sort_values(col).reset_index();
    colors = ['red' if status == 1 else 'blue' for status in crSetSorted['CONCUSSED']];
    
    ranks = np.arange(len(crSetSorted));
    labels = crSetSorted["CONCUSSED"].to_numpy();
    concussedRanks = ranks[labels == 1];
    nonConcussedRanks = ranks[labels == 0];

    uStat, p = mannwhitneyu(concussedRanks, nonConcussedRanks, alternative="two-sided");
    if (p < .05):
        print (col, " is significant");