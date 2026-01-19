import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

NanReplacementMethod = "mean" 
crSet = pd.read_csv("C:/Users/PL003A/Desktop/Concussion Analysis/Python ML/all.csv")

selectedFeature = ['Fixation_SaccadeRate'];
selectedFeature = ['Fixation_Saccade_Amplitude'];
selectedFeature = ['AllTasks_MainSeqSlopeAll'];
#selectedFeature = ['MemoryGuided_MainSeqSlopeAll'];
#selectedFeature = ['Antisaccade_ReactionTime'];
#selectedFeature = ['FreeViewing_SaccadeRate'];# EXAMPLE OF A "BAD" VARIABLE
#selectedFeature = ['Pursuit_MainSeqSlopeAll'];

col = selectedFeature;
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

data = crSet[selectedFeature];
crSetSorted = crSet.sort_values(col).reset_index();
colors = ['red' if status == 1 else 'blue' for status in crSetSorted['CONCUSSED']];

plt.scatter(range(len(crSetSorted)), crSetSorted[col], c=colors, alpha=0.7);

plt.title("Sorted Order for Selected Feature: " + col[0]);

plt.xlabel("Rank Order");
plt.ylabel("Value");

plt.grid(True);

plt.legend(handles=[
    plt.Line2D([0], [0], marker='o', color='w', label='Concussed', markerfacecolor='red', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Non-concussed', markerfacecolor='blue', markersize=10)
]);

plt.tight_layout();
plt.show();
