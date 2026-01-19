import os;
import pandas as pd;

dataDirectory = "C:/Users/David/Desktop/Heart Contraction/data/";

subjectSystoleCondition = [];
subjectDiastoleCondition = [];

paradigms = ["Faces", "Symbols"];

# Relevant Files
messagesFile = "eb_messages_fixed.txt";
faceFileName = "FACIAL_IMAGE_RESULTS.txt";
symbolFileName = "SYMBOL.txt";

rows = [];

class TrialStructure:
    isSystolic = -1;
    value = "";
    
    def __init__(self, condition, value):
        self.isSystolic = condition;
        self.value = value;
    
def getAccuracy(dataSet):
    if (len(dataSet) < 1):
        print("Warning! A entered set is 0 in length!");
        return 0;
        
    return round(sum(dataSet) / len(dataSet), 2);
    
for folder in os.listdir(dataDirectory):
    fullPath = os.path.join(dataDirectory, folder); # Data Folder for Individual Participants
    
    subjectIndex = fullPath.split('/')[6];
    print("Processing Subject: " + subjectIndex);
 
    faceTrials = [];
    symbolTrials = [];
 
    for p in paradigms:
        fileName = faceFileName if (p == "Faces") else symbolFileName;
        
        with open(os.path.join(fullPath, fileName), encoding="utf-8") as file:    
            next(file);
            for line in file:
                splitLine = line.split();

                if (p == "Faces"):
                    faceTrials.append(TrialStructure((splitLine[5] == "Systolic"), splitLine[2]));
                else:
                    symbolTrials.append(TrialStructure((splitLine[5] == "Systolic"), splitLine[3][0]));
                

    reactions = {
        "face": {
            "overall": {"Systolic": [], "Diastolic": []},
            "1":   {"Systolic": [], "Diastolic": []}, # Angry
            "2": {"Systolic": [], "Diastolic": []}, # Fearful
            "3":     {"Systolic": [], "Diastolic": []}, # Sad
        },
        "symbol": {
            "overall": {"Systolic": [], "Diastolic": []},
            "✖":       {"Systolic": [], "Diastolic": []},
            "◆": {"Systolic": [], "Diastolic": []},
            "✚":    {"Systolic": [], "Diastolic": []},
        }
    };
    
    
    faceIndex = 0;
    symbolIndex = 0;
    
    with open(os.path.join(fullPath, messagesFile), encoding="utf-8") as file:
            previousLine = "";
            for line in file:
                splitLine = line.split();  

                if "press" not in line:
                    previousLine = line;
                    continue;                                
                
                match splitLine[1]:
                    case "Angry" | "Sad" | "Fearful":
                        firstIndex = "face";
                        curTrialStructure = faceTrials[faceIndex];
                        faceIndex += 1;
                    case "✖" | "◆" | "✚":
                        firstIndex = "symbol";
                        curTrialStructure = symbolTrials[symbolIndex];
                        symbolIndex += 1;
                    case _:
                        previousLine = line;
                        continue;
                        
                secondIndex = curTrialStructure.value; 
                thirdIndex = "Systolic" if curTrialStructure.isSystolic else "Diastolic";
                                                
                reactionTime = float(splitLine[0]) - float(previousLine.split()[0])
                
                reactions[firstIndex]["overall"][thirdIndex].append(reactionTime);
                reactions[firstIndex][secondIndex][thirdIndex].append(reactionTime);
                
                previousLine = line;
                
                            
    faceLabels = {"1": "Angry", "2": "Fearful", "3": "Sad"};
    symbolLabels = {"✖": "✖", "◆": "◆", "✚": "✚"};
    
    row = [subjectIndex];
    
    for domain, labels in (("face", faceLabels), ("symbol", symbolLabels)):
        systole = reactions[domain]["overall"]["Systolic"];
        diastole = reactions[domain]["overall"]["Diastolic"];
    
        overallSystole = getAccuracy(systole);
        overallDiastole = getAccuracy(diastole);
    
        row.extend([overallSystole, overallDiastole]);
    
        for key in labels:
            s = reactions[domain][key]["Systolic"];
            d = reactions[domain][key]["Diastolic"];
    
            meanSystole = getAccuracy(s);
            meanDiastole = getAccuracy(d);
    
            row.extend([meanSystole, meanDiastole]);
    
    rows.append(row);


df = pd.DataFrame(rows, columns=["Subject",
                                 "Face Overall Systole", "Face Overall Diastole",
                                 "Angry Systole", "Angry Diastole",
                                 "Fearful Systole", "Fearful Diastole",
                                 "Sad Systole", "Sad Diastole",
                                 "Symbol Overall Systole", "Symbol Overall Diastole",
                                 "✖ Systole", "✖ Diastole",
                                 "◆ Systole", "◆ Diastole",
                                 "✚ Systole", "✚ Diastole"]);
                                            
outPath = os.path.join(os.path.dirname(dataDirectory), "ReactionTimeSummary.xlsx");

with pd.ExcelWriter(outPath, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Accuracies", index=False);
    