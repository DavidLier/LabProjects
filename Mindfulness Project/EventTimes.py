from typing import List, Tuple
import numpy as np

def diodeToRawEvents(rawPhotoDiode, diodeTimes) -> List[Tuple[Tuple[int, float], Tuple[int, float]]]:   
    events = [];
    inEvent = False;

    eventOnset = 0;
    eventOffset = 0;

    for sample, power in enumerate(rawPhotoDiode[0]):
        if (abs(power) > .03):
            if (inEvent == True):
                continue;
            
            inEvent = True
            eventOnset = (sample, diodeTimes[sample]);
        else:
            if (inEvent == True):
                eventOffset = (sample, diodeTimes[sample]);
                inEvent = False;
    
                events.append((eventOnset, eventOffset));
    
    return events; # TODO: Remove first flash? It might be the start time flash, I need to confirm manually!

def rawToneEventsToMNEEvents(events, onset=True, oldMethod=False, resultsInfo=None) -> np.ndarray:
    # Extract the end time and then remove it from the events list
    eegEndTime = events[1][0][0];

    events = events[2:];

    if (oldMethod == False):
        samples = np.array([ev[0][0] for ev in events], dtype=int)

        if (onset == False):
            samples = np.array([ev[1][0] for ev in events], dtype=int)

        mneEvents = np.zeros((len(samples), 3), dtype=int)
        mneEvents[:, 0] = samples;

        return mneEvents;

    # Necessary adjustments for old data sets due to timing errors
    adjustedToneTimes = [x / 2 for x in resultsInfo.tones];
    adjustedToneTimes = [x + (eegEndTime - ((resultsInfo.endTime -resultsInfo.startTime)/2)) for x in adjustedToneTimes];
    adjustedToneTimes = [adjustedToneTimes[i + 1] + (.199 * (i+1) - 14.3) for i in range(len(adjustedToneTimes)-1)];
    
    samples = np.array(adjustedToneTimes, dtype=int);
    
    mneEvents = np.zeros((len(samples), 3), dtype=int);
    mneEvents[:, 0] = samples;

    return mneEvents;

# This version is specifically for center bound timing windows - there's no flash associated to these, though should be able to get from the other synced PC with the ECG and Pulmonary
def rawCentralEventsToMNEEvents(events, resultsInfo, centerTimes) -> np.ndarray:
    # Still relies on the extraction of the end time, this varies per subject since sometimes people wouldn't end the EEG recording right away 
    eegEndTime = events[1][0][0];

    # Necessary adjustments for old data sets due to timing errors
    adjustedToneTimes = [x / 2 for x in centerTimes];
    adjustedToneTimes = [x + (eegEndTime - ((resultsInfo.endTime -resultsInfo.startTime)/2)) for x in adjustedToneTimes];
    adjustedToneTimes = [adjustedToneTimes[i + 1] + (.199 * (i+1) - 14.3) for i in range(len(adjustedToneTimes)-1)];
    
    samples = np.array(adjustedToneTimes, dtype=int);
    
    mneEvents = np.zeros((len(samples), 3), dtype=int);
    mneEvents[:, 0] = samples;

    return mneEvents;
