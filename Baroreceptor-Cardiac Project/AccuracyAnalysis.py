import os;
import pandas as pd;

dataDirectory = "C:/Users/David/Desktop/Heart Contraction/data/";

subjectSystoleCondition = [];
subjectDiastoleCondition = [];

# Relevant Files
symbolFileName = "SYMBOL.txt";
faceFileName = "FACIAL_IMAGE_RESULTS.txt";
badTrialsFileName = "BAD_TRIALS.txt";

rows = [];

def getAccuracy(dataSet):
    return round(sum(dataSet) / len(dataSet) * 100, 2);
    
for folder in os.listdir(dataDirectory):
    fullPath = os.path.join(dataDirectory, folder); 
    
    subjectIndex = fullPath.split('/')[6];
    print("Processing Subject: " + subjectIndex);
    
    badTrialIndices = [];
    with open(os.path.join(fullPath, badTrialsFileName)) as file:
        for line in file:
            processedLine = line.replace(" ", "").strip().split(",");
            if len(processedLine) > 0:
                for l in processedLine:
                    badTrialIndices.append(int(l));
                    
    # Facial Accuracy
    with open(os.path.join(fullPath, faceFileName)) as file:    
        overallSystole = [];
        overallDiastole = [];

        angrySystoleAccuracy = [];
        angryDiastoleAccuracy = [];
        
        fearfulSystoleAccuracy = [];
        fearfulDiastoleAccuracy = [];
        
        sadSystoleAccuracy = [];
        sadDiastoleAccuracy = [];
        
        next(file);
        for line in file:
            splitLine = line.split();
            
            heartCondition = splitLine[5];
            correct = splitLine[2] == splitLine[4]

            match splitLine[2]: # Which Face Emotion
                case "1":
                    if heartCondition == "Systolic":
                        angrySystoleAccuracy.append(correct);
                    else: 
                        angryDiastoleAccuracy.append(correct);
                case "2":
                    if heartCondition == "Systolic":
                        fearfulSystoleAccuracy.append(correct);
                    else: 
                        fearfulDiastoleAccuracy.append(correct);
                case "3":
                    if heartCondition == "Systolic":
                        sadSystoleAccuracy.append(correct);
                    else: 
                        sadDiastoleAccuracy.append(correct);
                        
            if heartCondition == "Systolic":
                overallSystole.append(correct);
            else:
                overallDiastole.append(correct);           
                        
        print(f"Systole Angry Accuracy {sum(angrySystoleAccuracy)/len(angrySystoleAccuracy)*100:.2f}% "
            f"Diastole Angry Accuracy {sum(angryDiastoleAccuracy)/len(angryDiastoleAccuracy)*100:.2f}%");
        
        print(f"Systole Fearful Accuracy {sum(fearfulSystoleAccuracy)/len(fearfulSystoleAccuracy)*100:.2f}% "
            f"Diastole Fearful Accuracy {sum(fearfulDiastoleAccuracy)/len(fearfulDiastoleAccuracy)*100:.2f}%");
        
        print(f"Systole Sad Accuracy {sum(sadSystoleAccuracy)/len(sadSystoleAccuracy)*100:.2f}% "
            f"Diastole Sad Accuracy {sum(sadDiastoleAccuracy)/len(sadDiastoleAccuracy)*100:.2f}%");
            
        rows.append(
            [subjectIndex, getAccuracy(overallSystole), getAccuracy(overallDiastole),
                           getAccuracy(angrySystoleAccuracy), getAccuracy(angryDiastoleAccuracy),
                           getAccuracy(fearfulSystoleAccuracy), getAccuracy(fearfulDiastoleAccuracy),
                           getAccuracy(sadSystoleAccuracy), getAccuracy(sadDiastoleAccuracy)]);
     
     
    # Symbols Accuracy
    with open(os.path.join(fullPath, symbolFileName), encoding="utf-8") as file:    
        overallSystole = [];
        overallDiastole = [];
        
        xSystoleAccuracy = [];
        xDiastoleAccuracy = [];
        
        diamondSystoleAccuracy = [];
        diamondDiastoleAccuracy = [];
        
        plusSystoleAccuracy = [];
        plusDiastoleAccuracy = [];
        
        next(file);
        for line in file:
            splitLine = line.split();
            
            heartCondition = splitLine[5];
            correct = splitLine[3][0] == splitLine[4]
            
            match splitLine[3][0]: # Which Symbol
                case "✖":
                    if heartCondition == "Systolic":
                        xSystoleAccuracy.append(correct);
                    else: 
                        xDiastoleAccuracy.append(correct);
                case "◆":
                    if heartCondition == "Systolic":
                        diamondSystoleAccuracy.append(correct);
                    else: 
                        diamondDiastoleAccuracy.append(correct);
                case "✚":
                    if heartCondition == "Systolic":
                        plusSystoleAccuracy.append(correct);
                    else: 
                        plusDiastoleAccuracy.append(correct);
            
            if heartCondition == "Systolic":
                overallSystole.append(correct);
            else:
                overallDiastole.append(correct);            
                        
        print(f"Systole ✖  Accuracy {sum(xSystoleAccuracy)/len(xSystoleAccuracy)*100:.2f}% "
            f"Diastole ✖  Accuracy {sum(xDiastoleAccuracy)/len(xDiastoleAccuracy)*100:.2f}%");
        
        print(f"Systole ◆ Accuracy {sum(diamondSystoleAccuracy)/len(diamondSystoleAccuracy)*100:.2f}% "
            f"Diastole ◆ Accuracy {sum(diamondDiastoleAccuracy)/len(diamondDiastoleAccuracy)*100:.2f}%");
        
        print(f"Systole ✚ Accuracy {sum(plusSystoleAccuracy)/len(plusSystoleAccuracy)*100:.2f}% "
            f"Diastole ✚ Accuracy {sum(plusDiastoleAccuracy)/len(plusDiastoleAccuracy)*100:.2f}%");        
            
        rows[-1].extend(
            [getAccuracy(overallSystole), getAccuracy(overallDiastole),
             getAccuracy(xSystoleAccuracy), getAccuracy(xDiastoleAccuracy),
             getAccuracy(diamondSystoleAccuracy), getAccuracy(diamondDiastoleAccuracy),
             getAccuracy(plusSystoleAccuracy), getAccuracy(plusDiastoleAccuracy)]);
            
df = pd.DataFrame(rows, columns=["Subject", 
                                            "Faces Systole Accuracy", "Faces Diastole Accuracy",
                                            "Angry Systole Accuracy", "Angry Diastole Accuracy", 
                                            "Fearful Systole Accuracy", "Fearful Diastole Accuracy",
                                            "Sad Systole Accuracy", "Sad Diastole Accuracy",
                                            "Symbols Systole Accuracy", "Symbols Diastole Accuracy",
                                            "✖  Systole Accuracy", "✖  Diastole Accuracy",         
                                            "◆ Systole Accuracy", "◆ Diastole Accuracy",
                                            "✚ Systole Accuracy", "✚ Diastole Accuracy"]);
                                            
outPath = os.path.join(os.path.dirname(dataDirectory), "AccuracySummary.xlsx");
with pd.ExcelWriter(outPath, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Accuracies", index=False);
    