import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import shapiro

NanReplacementMethod = "mean" 
crSet = pd.read_csv("C:/Users/PL003A/Desktop/Concussion Analysis/Python ML/all.csv")
selectedFeatures = ['Fixation_MainSeqSlopeAll', 'VisuallyGuided_MainSeqSlopeAll', 'AllTasks_MainSeqSlopeAll', 'MemoryGuided_MainSeqSlopeAll', 'Antisaccade_ReactionTime'];

#for col in selectedFeatures:
for col in crSet.columns[3:]:
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

#for col in selectedFeatures:
for col in crSet.columns[3:]: # If it doesn't follow normality it stands to reason we should remove it from this deviation index, but I want to check with Dr. B and make sure this is what he envisioned first
    _, p = shapiro(crSet[col]);
    isNormal = p > 0.5;

#data = crSet[selectedFeatures];
data = crSet.iloc[:, 3:]  # Just the 45 variables
deviationFrame = pd.DataFrame(index=data.index, columns=data.columns);
STDDeviationFrame = pd.DataFrame(index=data.index, columns=data.columns);

for col in data.columns:
    fullStd = data[col].std();
    for i in range(len(data)):
        allExcept = data[col].drop(index=i);
        setMean = allExcept.mean();
        setSTD = allExcept.std();

        if (setSTD == 0):
            zScore = 0;
        else:
            zScore = abs((data.at[i, col] - setMean) / setSTD);

        STDDeviationFrame.at[i, col] = abs(fullStd - setSTD);
        deviationFrame.at[i, col] = zScore;

crSet["DeviationIndex"] = deviationFrame.sum(axis=1) / 45;
crSet["STDDeviationIndex"] = STDDeviationFrame.sum(axis=1) / 45;

crSetSorted = crSet.sort_values("DeviationIndex").reset_index();
colors = ['red' if status == 1 else 'blue' for status in crSetSorted['CONCUSSED']];

#plt.figure(figsize=(12, 6));
plt.scatter(range(len(crSetSorted)), crSetSorted["DeviationIndex"], c=colors, alpha=0.7);

plt.title("Deviation Index for All Trials");

plt.xlabel("Rank Order");
plt.ylabel("Mean Deviation Index");

plt.grid(True);

plt.legend(handles=[
    plt.Line2D([0], [0], marker='o', color='w', label='Concussed', markerfacecolor='red', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Non-concussed', markerfacecolor='blue', markersize=10)
]);

plt.tight_layout();
plt.show();