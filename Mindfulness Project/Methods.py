import mne
import numpy as np
from mne.time_frequency import tfr_morlet

def erpAnalysis(wanderingERPTimes, focusedERPTimes, rawData, sampleEvents):
     for indice in wanderingERPTimes:
        sampleEvents[indice, 2] = 1;
     for indice in focusedERPTimes:
        sampleEvents[indice, 2] = 2;

     erpData = rawData.copy();
     erpData.filter(l_freq=1.0, h_freq=30); 
     erpData.notch_filter(freqs=[60, 120, 180]);

     epochs = mne.Epochs(
          erpData.pick(["P7", "P3", "O1", "O2", "P4", "P8"]),
          sampleEvents,
          tmin=-.25,
          tmax=.5,
          #reject=reject_criteria,
          detrend=1    
     );

     wanderingEpochs = epochs['1'];
     focusedEpochs = epochs['2'];

     wanderingERPs = wanderingEpochs.iter_evoked();
     focusedERPs = focusedEpochs.iter_evoked();

     mne.viz.plot_compare_evokeds(
     {"Wandering Epochs": list(wanderingERPs), "Focused Epochs": list(focusedERPs)}, 
     picks=["P7", "P3", "O1", "O2", "P4", "P8"], combine="mean", ci=.95);


def timeFreqAnalysis(sampleEvents, rawData, window):
    picks = ["P7", "P3", "O1", "O2", "P4", "P8"];
    tfData = rawData.copy().pick(picks);
    
    tfData.filter(l_freq=1.0, h_freq=40); 
    tfData.notch_filter(freqs=[60, 120, 180]);

    epochs = mne.Epochs(
        tfData,
        sampleEvents,
        tmin=-(window/1000),
        tmax=(window/1000),
        detrend=1,
        preload=True,
        baseline=None
    );

    #epochs.plot_image();

    freqs = np.linspace(2, 30, 29);
    nCycles = 7;

    if (len(epochs) == 0): # Means all of them got removed by the auto filtering 
        return np.nan, np.nan;

    power = tfr_morlet(
       epochs,
       freqs=freqs,
       n_cycles=nCycles,
       return_itc=False,
       average=False,
       decim = 2
    );

    print(power.data.shape);

    times = power.times; 

    # Trying to avoid edge affects 
    # Braboszcz specifically did the same but looking at 2-8, I should look into where that boundary realistically needs to be drawn
    wanderingWindow  = (times >= -8.0) & (times <= -2.0);   
    focusedWindow = (times >=  2.0) & (times <= 8.0);

    dataPre  = power.data[:, :, :, wanderingWindow].mean(axis=0).mean(axis=0); # Average across epochs, and then across channels
    dataPost = power.data[:, :, :, focusedWindow].mean(axis=0).mean(axis=0);

    return (10 * np.log10(dataPre)), (10 * np.log10(dataPost));


def HRVAnalysis(beats, centralFocusTimes, window):    
    window = window / 1000;
    epochs = [];

    for i in centralFocusTimes:
        i = i/1000; 

        print(i);
        preWindow = [];
        postWindow = [];

        for j in beats:
            if (i-window) <= j[0] < (i):
                preWindow.append(j[1]);
            if (i) <= j[0] <= (i + window):
                postWindow.append(j[1]);

        # Artifact Rejection
        if (len(preWindow) < 3 or len(postWindow) < 3): # Means artifacts were removed in BIOPAC software, so there's gaps in the time data
            continue;
        if (np.max(preWindow) > 1.5 or np.max(postWindow) > 1.5): # Typical RR-I intervals shouldn't exceed 1.5 (or else they need a doctors appointment)
            continue;
        if (np.min(preWindow) < 0.4 or np.min(postWindow) < 0.4): # Same reasoning as above - but this is arbitrary, need to review the literature (though >150bpm resting is crazy)
            continue;

        preRMSSD = np.sqrt(np.mean(np.square(np.diff(preWindow)))); 
        postRMSSD = np.sqrt(np.mean(np.square(np.diff(postWindow))));

        epochs.append(np.log(postRMSSD) - np.log(preRMSSD));

    return np.mean(epochs);


def PulmonaryAnalysis(pulmonaryData, centralFocusTimes, window):
    bpmEpochs = [];
    tvEpochs = [];

    # Simplest method I can think of for removing extreme tidal volume artifacts, though I should either crop manually or see if the literatures got a better method
    allTidalVolumes = [i[1] for i in pulmonaryData];
    tvMean = np.mean(allTidalVolumes);
    tvSTD = np.std(allTidalVolumes);

    for i in centralFocusTimes:
        i = i/1000; 
        
        preBPMWindow = [];
        postBPMWindow = [];
        preTVWindow = [];
        postTVWindow = [];

        for j in pulmonaryData:
            if (j[3] <= 0): # This is the it value, for some reason it falls negative which should be impossible so this is just a quick artifact rejection
                continue;

            if (i-window) <= j[0] < (i):
                preTVWindow.append(j[1]);
                preBPMWindow.append(j[2]);
            if (i) <= j[0] <= (i + window):
                postTVWindow.append(j[1]);
                postBPMWindow.append(j[2]);
        
        # Given the limited sample size it would make sense to seperate these checks for the 
        # statistical power but I need to look into the reliability of one metric if the other is damaged so 
        # I'll leave it like this for now
        if (len(preBPMWindow) * len(postBPMWindow) * len(preTVWindow) * len(postTVWindow)) == 0: 
            continue;
    
        artifact = False;
        for j in preTVWindow:
            if (abs(j - tvMean) > (3*tvSTD)):
                artifact = True;
        for j in postTVWindow:
            if (abs(j - tvMean) > (3*tvSTD)):
                artifact = True;
        if (artifact):
            continue;

        bpmEpochs.append(np.mean(postBPMWindow) - np.mean(preBPMWindow));
        tvEpochs.append(np.mean(postTVWindow) - np.mean(preTVWindow));
    
    return bpmEpochs, tvEpochs;
