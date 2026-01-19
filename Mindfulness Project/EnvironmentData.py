from typing import List, Tuple

class EnvironmentData: # Tones, Button Presses, Miscounts

    def __init__(this, contentsFile, window):
        this.timeWindow = window;

        this.startTime = float(contentsFile[len(contentsFile) - 1].split()[3]);
        this.endTime = float(contentsFile[len(contentsFile) - 1].split()[4]);

        this.tones = [];
        this.buttonPresses = [];
        this.selfIdentifiedMiscounts = [];

        # Because we don't want to count the intial of each as one, so we use '0' to make sure it matches the file
        lastTone = '0';
        lastButtonPress = '0';
        lastMiscount = '0'; 

        for line in contentsFile:
            line = line.split();
 
            if (line[11] != lastTone): # Tone Time Index
                lastTone = line[11];
                this.tones.append(this.adjustedTiming(float(line[11])));

            if (line[5] != lastButtonPress): # Button Count Index
                lastButtonPress = line[5];
                this.buttonPresses.append((this.adjustedTiming(float(line[6])), int(line[5])));
    
            if (line[7] != lastMiscount): # Miscount Count Index
                lastMiscount = line[7];
                this.selfIdentifiedMiscounts.append((this.adjustedTiming(float(line[8])), int(line[7])));
        
        this.tones = this.tones[1:]; # First one isn't a tone
    
    def getTimeIndices(this) -> Tuple[List[int], List[int], List[int]]:
        wanderingIndices = set();
        focusedIndices = set();

        centeredTimes = [t[0] for t in this.selfIdentifiedMiscounts];

        # What do we count as errors: Within 20 Seconds prior of a self delcared miscount & Anything from count 13 -> when miscount was resolved

        # First, prior and post 20 seconds of a self declared miscount
        for miscountTime in this.selfIdentifiedMiscounts:
            for i, tone in enumerate(this.tones):
                if tone < miscountTime[0] and tone > miscountTime[0] - this.timeWindow:
                    wanderingIndices.add(i);
                if tone >= miscountTime[0] and tone < miscountTime[0] + this.timeWindow:
                    focusedIndices.add(i);

        # Now any tones within the 13th button press til they reset their count
        startTime = -1;
        for buttonPresses in this.buttonPresses: 
            if (buttonPresses[1] < 13 and startTime == -1):
                continue;

            if (startTime == -1):
                startTime = buttonPresses[0];
                continue;

            if (buttonPresses[1] == 0): # This means the count was reset
                centeredTimes.append(buttonPresses[0]);
                for i, tone in enumerate(this.tones):
                    if tone < buttonPresses[0] and tone > startTime:
                        wanderingIndices.add(i);
                    if tone >= buttonPresses[0] and tone < buttonPresses[0] + this.timeWindow:
                        focusedIndices.add(i);

                startTime = -1;

        # Make sure there's no overlap between the sets, assume it belongs in the mindful category if there is
        # Though more conservatively it would make more sense to remove it from both lists, given we're not going to have these in the final paper
        # due to low # of them, it's fine to use as a visualizing tool for sanity checks about timing accuracies
        wanderingIndices = wanderingIndices - focusedIndices; 

        centeredTimes = this.removeSimilarTimeFrames(centeredTimes);

        return list(wanderingIndices), list(focusedIndices), centeredTimes; 

    def removeSimilarTimeFrames(this, toAdjust):
        toAdjust.sort();
        cleaned = [toAdjust[0]];

        for i in range(len(toAdjust)):
            if abs(toAdjust[i] - cleaned[-1]) > this.timeWindow:
                cleaned.append(toAdjust[i])

        return cleaned;


    def adjustedTiming(this, currentTime) -> int: # TODO: Add the linear offset adjustment to deal with the weird drift in the data, this is ms drift though so fine for TFQ for now 
        return int((currentTime - this.startTime));


    def __str__(this) -> str:
        return "Start Time: " + str(this.startTime) + " End Time: " + str(this.endTime) + " # of Tones:" + str(len(this.tones)) + " # of Button Presses: " + str(len(this.buttonPresses)) + " # of Miscounts (Self): " + str(len(this.selfIdentifiedMiscounts));