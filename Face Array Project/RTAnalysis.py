# Python version of AccInfo.m without accuracy stuff, don't have matlab on this computer but need the individual RT #'s for Analysis ready for later today

import os
import numpy as np
import pandas as pd
from statsmodels.stats.anova import AnovaRM
import pingouin as pg


for experiment in range(2):
    dataDir = "C:\\Users\\PL003A\\Desktop\\Multiple Faces\\Data\\";

    if (experiment == 1):    
        dataDir = "C:\\Users\\PL003A\\Desktop\\Multiple Faces\\Data3\\";


    totalAverage = [];
    rows = [];

    for participant in os.listdir(dataDir):
        print("Processing Data Folder", participant);
        
        participantFolder = dataDir + "\\" + participant;
        resultsText = open(participantFolder + "\\RESULTS_FILE.txt");


        conditionColumn = 7;
        reactionColumn = 4; 

        if experiment == 1:
            conditionColumn = 10;
            reactionColumn = 7;

        resultsTextContents = resultsText.readlines()[1:]; 

        conditionRT = {};
        
        for line in resultsTextContents:
            line = line.split();

            if (len(line[reactionColumn]) == 1): # They didn't select anything
                continue;
    
            trialRT = float(line[reactionColumn]) - float(line[reactionColumn - 1]); # Time displayed is reactionColumn - 1
            condition = line[conditionColumn];

            if (condition not in conditionRT):
                conditionRT[condition] = [trialRT];
                continue;

            conditionRT[condition].append(trialRT);

        avgRT = 0;

        for key in conditionRT.keys():
            conditionAr = np.array(conditionRT[key]);
            avgRT = np.mean(conditionAr);
            
            print(key, " ", avgRT, " ", np.std(conditionAr));    
            rows.append({"subject": participant, "condition": key, "rt": avgRT});


        totalAverage.append(conditionRT);


    dfTrials = pd.DataFrame(rows);
    dfMeans = (
        dfTrials
        .groupby(["subject", "condition"], as_index=False)
        .agg(mean_rt=("rt", "mean"))
    );

    print(dfMeans);

    aov = AnovaRM(
        data=dfMeans,
        depvar="mean_rt",
        subject="subject",
        within=["condition"]
    ).fit();

    print(aov);

    # Sanity Check to make sure this is all the same #s as the MATLAB version
    total = [];
    for arr in totalAverage:
        for key in arr.keys():
            total.extend(arr[key]);

    print(np.mean(np.array(total)), " ", np.std(np.array(total))); 

    posthoc = pg.pairwise_tests(
        data=dfMeans,
        dv="mean_rt",
        within="condition",
        subject="subject",
        padjust="holm",   
        effsize="cohen"
    );

    print(posthoc);
