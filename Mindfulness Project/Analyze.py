import os
import numpy as np
import mne
from mne.stats import permutation_cluster_1samp_test
from scipy import stats

from EnvironmentData import EnvironmentData
from EventTimes import diodeToRawEvents, rawToneEventsToMNEEvents, rawCentralEventsToMNEEvents
from Methods import erpAnalysis, timeFreqAnalysis, HRVAnalysis, PulmonaryAnalysis
from Plot import tfPlot

sourceDir = ".";  
dataDir = sourceDir + "/data";

window = 10000; # 10 Seconds (Post and Pre)

totalCentralEpochs = [];
timeFreqDiffs = [];
HRVDiffs = []; # RMSSD
bpmDiffs = []; # Breaths per min.
tvDiffs = []; # Tidal Volume

for participantID in os.listdir(dataDir):
    if participantID == "ignore - poor data":
        continue;

    print("Processing Data Folder", participantID);
    participantFolder = dataDir + "/" + participantID;

    # Subject Data
    resultsText = open(participantFolder + "/results/Main_Results.txt");
    resultsTextContents = resultsText.readlines()[1:]; # Header line skip

    resultsData = EnvironmentData(resultsTextContents, window);
    timingResults = resultsData.getTimeIndices();

    # MNE Needs to know these are all EEG channels, so this is just explictly creating a dictionary to make that clear - I miss FieldTrip
    defaultChannelNames = ('Fp1', 'Fz', 'F3', 'F7', 'FT9', 'FC5', 'FC1', 'C3', 'T7', 'TP9', 'CP5', 'CP1', 'Pz', 'P3', 'P7', 'O1', 'Oz', 'O2', 'P4', 'P8', 'TP10', 'CP6', 'CP2', 'Cz', 'C4', 'T8', 'FT10', 'FC6', 'FC2', 'F4', 'F8');
    channelDict = {channel: 'eeg' for channel in defaultChannelNames};

    print(participantID);
    rawData = mne.io.read_raw_brainvision(participantFolder + "/eeg/" + participantID + ".vhdr", misc=['Photo Sensor'], preload=True);
    rawData.set_channel_types(channelDict);

    # Extracting the flashes from the Photo Sensor, and using that to define a list of events
    photoDiode = rawData.copy().pick(picks="Photo Sensor");
    rawPhotoDiode, diodeTimes = photoDiode.get_data(return_times=True);
        
    # Contains onset and offset data in two different Tuples i.e: rawEvents[0][0] = onset samples, vs rawEvents[0][1] = onset time (s), rawEvents[1] is offset
    rawEvents = diodeToRawEvents(rawPhotoDiode, diodeTimes); 

    # Event Declaration - If there was less then 5 flashes through out, it must be an old data set so we use the old method
    sampleEvents = rawToneEventsToMNEEvents(rawEvents, onset=True, oldMethod=(len(rawEvents) < 5), resultsInfo=resultsData); # Just gives a 3xn, required for MNE epoch declaration        

    # to visualize the events - on the new data sets only tho
    # rawData.copy().pick(["Photo Sensor"]).plot(duration=10, n_channels=1, block=True, events=sampleEvents, event_color='red');

    # ERP EEG Analysis
    wanderingERPTimes = timingResults[0];
    focusedERPTimes   = timingResults[1];
    
    # Unfortuntatly only a few sets have a valid # of ERPs to compare the auditory stimulus
    # Need 20-30 in each condition to be valid if Brabosczcz and Delmore are to be believed since we're looking at similiar components,
    # but I can't find where in the source they cite it says that. 20-30 seems awfully low, esp. for late components
    valid = len(wanderingERPTimes) >= 30 and len(focusedERPTimes) >= 30;

    print("ERP Analysis Valid on this Data Set:", valid);
    if (valid == True):
        erpAnalysis(wanderingERPTimes, focusedERPTimes, rawData, sampleEvents);
        continue;

    # Time Frequency Analysis
    centralFocusTimes = timingResults[2];
    sampleEvents = rawCentralEventsToMNEEvents(rawEvents, resultsData, centralFocusTimes);      

    numberOfEpochs = len(sampleEvents);
    if (numberOfEpochs < 13):
       print("Not Valid, Only: ", numberOfEpochs);
       continue;
    
    totalCentralEpochs.append(numberOfEpochs);
    pre, post = timeFreqAnalysis(sampleEvents, rawData, window);
    if (pre is not np.nan) and (post is not np.nan): # Temp since I need to manually verify some epochs and the rejection method is wiping all of them out for some sets
        timeFreqDiffs.append((post - pre));
 
    # HRV Analysis
    if not (os.path.exists(participantFolder + "/biopac/ecg.txt")):
        continue;

    beats = [];
    ECGText = open(participantFolder + "/biopac/ecg.txt"); # TODO: Should use the event checkpoints marked here for central windows, they should be immune to the odd drift issue
    rawECGContents = ECGText.readlines()[1:-1]; # Header line skip and summary line skip
    startTime = float(rawECGContents[0].split()[1]);
    for line in rawECGContents:
        column = line.split();
        beats.append((float(column[1]) - startTime, float(column[2]))); # Time and RR-I, ignoring other calculatable metrics since Shaffer and Ginsberg imply RMSSD is the only to work on this timescale

    RMSSDDiff = HRVAnalysis(beats, centralFocusTimes, window);
    if not (np.isnan(RMSSDDiff)):
        HRVDiffs.append(RMSSDDiff);

    # Pulmonary Analysis
    if not (os.path.exists(participantFolder + "/biopac/pulmonary.txt")):
        continue;

    pulmonaryData = [];
    pulmonaryText = open(participantFolder + "/biopac/pulmonary.txt"); 
    rawPulmonaryContents = ECGText.readlines()[1:-1]; # Header line skip and summary line skip
    startTime = float(rawECGContents[0].split()[1]);
    for line in rawPulmonaryContents:
        column = line.split();

        tv = float(column[4]);
        bpm = float(column[6]);
        it = float(column[7]);

        pulmonaryData.append(((float(column[1]) - startTime), tv, bpm, it)); 

    bpm, tv = PulmonaryAnalysis(pulmonaryData, centralFocusTimes, window);
    if (bpm is not np.nan) and (tv is not np.nan):
        bpmDiffs.append(bpm);
        tvDiffs.append(tv);        

    #break;

print("Events, AVG: ", np.mean(totalCentralEpochs), "+- ", np.std(totalCentralEpochs), "Min: ", np.min(totalCentralEpochs), "Max: ", np.max(totalCentralEpochs));

# Time Frequenecy Stats
groupTimeFreqDifferences = np.array(timeFreqDiffs);
tOBS, clusters, clusterPVals, H0 = permutation_cluster_1samp_test(groupTimeFreqDifferences, n_permutations=1000);

for i, p in enumerate(clusterPVals):
    if (p < .05):
        print("Significant:");
    print("Cluster: ", i, " p:", p);

# Time Frequency Plot Info (Matching morlet input)   
times = np.linspace(0, 6, 1501); 
freqs = np.linspace(2, 30, 29);

# Preliminary Results Match Compton et al. But this is weird since Braboszcz and Delmore showed the opposite expectation
# And our paradigm matched much more closely with Delmores approach? Compton intro explained possible reasons I think so review
tfPlot(times, freqs, tOBS, clusters, clusterPVals);

# HRV and Pulmonary Stats
tStat, p = stats.ttest_1samp(HRVDiffs, popmean=0);
print("RMSSD Diff P Val:", p); # Pretty much what we suspected unfortunately

tStat, p = stats.ttest_1samp(HRVDiffs, popmean=0);
print("Tidal Volume Diff P Val:", p); 

tStat, p = stats.ttest_1samp(HRVDiffs, popmean=0);
print("RMSSD Diff P Val:", p); 
