import numpy as np
import matplotlib.pyplot as plt

def tfPlot(times, freqs, tOBS, clusters, clusterPVals):
    plt.figure(figsize=(10, 8));

    tOBSPlot = np.nan * np.ones_like(tOBS);

    for c, p in zip(clusters, clusterPVals):
        if p <= 0.1: # Since I need to clean out the epochs still, I'll give a little wiggle room due to the low sample size #TODO: Remember to switch again later
            tOBSPlot[c] = tOBS[c];

    # Gray Scale Non Sig Parts
    plt.imshow(tOBS,
           extent=[times[0], times[-1], freqs[0], freqs[-1]],
           aspect='auto', origin='lower', cmap='gray', alpha=0.3);
    
    # Color Sig Parts
    plt.imshow(tOBSPlot,
           extent=[times[0], times[-1], freqs[0], freqs[-1]],
           aspect='auto', origin='lower', cmap='RdBu_r');

    plt.colorbar(label='T Stat');
    plt.xlabel('Time (s)'); # Remember this is +2 due to borders
    plt.ylabel('Frequency (Hz)');
    plt.title('Focused (After Button Press) vs. Mind Wandering');

    plt.show();