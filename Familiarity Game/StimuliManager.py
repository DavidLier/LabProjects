import os
import random

class StimuliManager:
    def __init__(this):
        this.gameStimulus = [];
        this.unseenStimulus = [];

        demographicFolders = os.listdir("Stimuli");
        for folder in demographicFolders:
            demographicStimulus = os.listdir("Stimuli/" + folder);
            demographicStimulus = ["Stimuli/" + folder + "/" + stim for stim in demographicStimulus];

            random.shuffle(demographicStimulus);

            half = int(len(demographicStimulus)/2);

            this.gameStimulus.extend(demographicStimulus[:half]);
            this.unseenStimulus.extend(demographicStimulus[half:]);         

        this.allStimulus = this.gameStimulus.copy();
        this.allStimulus.extend(this.unseenStimulus);

        return;

    def saveStimulusLists(this, participantID):
        if (os.path.exists("participants/" + participantID)):
            print("ERR: Participant already exists, going to add a marker to the participantID in case this was a mistake!");
            participantID = participantID + " - 2";

        os.mkdir("participants/" + participantID);
        with open("participants/" + participantID + "/" + participantID + ".txt", "w") as file:
            file.write(', '.join(this.gameStimulus));
            file.write('\n');
            file.write(', '.join(this.unseenStimulus));