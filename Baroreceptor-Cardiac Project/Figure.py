import numpy as np
import matplotlib.pyplot as plt

class Figure:
    def __init__(self, title, givenLabels, givenXLabels, givenValues, givenErrors, yLabel, subTexts):
        self.title = title;
        self.barLabels = givenLabels;  
        self.xLabels = givenXLabels;           
        self.barValues = np.asarray(givenValues);  
        self.stdErrors = np.asarray(givenErrors);  
        self.yLabel = yLabel;
        self.subTexts = subTexts;
        
    def plot(self, width, offset, colorOne, colorTwo, lowerYLim, upperYLim, increments):
        figure, ax = plt.subplots();
        
        y = self.barValues;
        errors = self.stdErrors;
        
        numberOfGroups, numberOfBars = y.shape;
        indices = np.arange(numberOfGroups)
        
        ax.grid(axis="y", color="#DDDDDD", linewidth=0.7);
        ax.set_axisbelow(True);
        
        groupOffset = .7;
        
        bars = [];
        for i in range(numberOfBars):
            color = colorOne if i % 2 == 0 else colorTwo;
          
            xPositions = groupOffset * indices + (i - (numberOfBars - 1) / 2.0) * (width + offset);

            bar = ax.bar(
                xPositions,
                y[:, i],
                width,
                yerr = errors[:, 1],
                label = self.barLabels[i],
                capsize = 5,
                edgecolor = "none",
                color = color
                );
                
            bars.append(bar);  
            
        ax.set_xticks(indices * groupOffset);
        
        plt.rcParams["text.usetex"] = True;

        ax.set_xticklabels([
            f"{main}\n{sub}"
            for main, sub in zip(self.xLabels, self.subTexts)
        ]);

        plt.rcParams["text.usetex"] = False;

        
        ax.set_ylabel(self.yLabel, fontweight = "bold");
        ax.legend(loc = "upper right", fancybox = False, edgecolor="black");
        
        title = ax.set_title(self.title, fontweight = "bold", pad = 20);
        
        ax.set_ylim(lowerYLim, upperYLim);
        ax.tick_params(axis = "both", labelsize = 12);
        ax.set_yticks(np.arange(lowerYLim, upperYLim + 1, increments)) ;

        for barGroup, errs in zip(bars, errors.T):
            for rect, e in zip(barGroup, errs):
                    height = rect.get_height();
                    
                    x = rect.get_x() + rect.get_width() / 2.0
                    ax.text(
                        x,
                        height + e + 1,           
                        f"{height:.1f}",
                        ha="center",
                        va="bottom",
                        fontsize=10,
                        fontweight="bold",
                    );
                    

        plt.tight_layout();
        plt.show();
        figure.savefig(f"images/{self.title}", dpi=300, bbox_inches="tight", pad_inches=0.25);
