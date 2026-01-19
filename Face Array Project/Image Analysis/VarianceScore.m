classdef VarianceScore
    properties
        fileName 
        experiment % 1/2
        perceptualLightness % https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color#:~:text=24%20Answers%20*%20Luminance%20(standard%20for%20certain,+%200.114*B%5E2%20)%20(thanks%20to%20@MatthewHerbst)%20source.
        rmsContrast  %https://en.wikipedia.org/wiki/Contrast_(vision)#RMS_contrast
        saturation
        powerSlope
    end

    methods
        function this = VarianceScore(fileName, experiment, perceptualLightness, rmsContrast, saturation, powerSlope)
            this.fileName = fileName;
            this.experiment = experiment;
            this.perceptualLightness = perceptualLightness;
            this.rmsContrast = rmsContrast;
            this.saturation = saturation;
            this.powerSlope = powerSlope;
        end
    end
end

%BRIGHTNESS/LUMINANCE/LIGHTNESS:
%https://en.wikipedia.org/wiki/Lightness
%AS good as it gets:
%https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color#:~:text=24%20Answers%20*%20Luminance%20(standard%20for%20certain,+%200.114*B%5E2%20)%20(thanks%20to%20@MatthewHerbst)%20source.
%"CIELAB is not a "full" image assessment model by any means. In my post I was trying to cover the basic concepts as completely as possible without venturing into the very deep minutiae. The Hunt model, Fairchild's models, and others do a more complete job, but are also substantially more complex. "
%https://en.wikipedia.org/wiki/CIELAB_color_space
%https://stackoverflow.com/questions/56198778/what-is-the-efficient-way-to-calculate-human-eye-contrast-difference-for-rgb-val/56237498#56237498
%
%CONTRAST:
%Pelli, D. G., & Bex, P. (2013). Measuring contrast sensitivity. Vision research, 90, 10–14. https://doi.org/10.1016/j.visres.2013.04.015
%https://doi.org/10.1016/j.visres.2013.04.015 
%Pelli & Bex. mention that the contrast method best for naturalistic stimuli is RMS Contrast. 
%
%
%COLOR SATURATION:
%https://pubmed.ncbi.nlm.nih.gov/28551362/
%https://www.sciencedirect.com/science/article/pii/S0042698917300901?via%3Dihub
%Schiller, F., Valsecchi, M., & Gegenfurtner, K. R. (2018). An evaluation of different measures of color saturation. Vision research, 151, 117–134. https://doi.org/10.1016/j.visres.2017.04.012
%Schiller et al. determined that the (LUV, LAB, CIECAM02) color space classifications for color saturation 
%were the most effective of those that they evaluated. They also saw that none of the color spaces could predict
%changes in perceptual interpretation of backgrounds which is moot in our use case (no backgrounds behind our face stimuli). 
%
%
%Spatial frequency has been shown to vary perceptual and attentional ERP componenets depending on the observers
%cultural background, so it stands to reason it's important to assess spatial frequency in EEG studies.
%Lin, T., Zhang, X., Fields, E. C., Sekuler, R., & Gutchess, A. (2022). Spatial frequency impacts perceptual and attentional ERP components across cultures. Brain and cognition, 157, 105834. https://doi.org/10.1016/j.bandc.2021.105834
%
%https://dsp.stackexchange.com/questions/41858/how-to-calculate-the-spatial-frequency-of-an-image-in-cycles-per-image 
%https://www.sciencedirect.com/science/article/abs/pii/S014976341730204X
%
%Good description of FFT for Spatial Frequency
%Forouhesh Tehrani, K., Pendleton, E. G., Southern, W. M., Call, J. A., & Mortensen, L. J. (2021). Spatial frequency metrics for analysis of microscopic images of musculoskeletal tissues. Connective tissue research, 62(1), 4–14. https://doi.org/10.1080/03008207.2020.1828381
%


%https://ieeexplore.ieee.org/document/9176999
%A relatively simple measure of the global contrast in natural images, 
% called RMS contrast has been introduced by Bex and Makous [44]. The RMS 
% contrast is based on the standard deviation of the image luminance. This 
% measure has been proven to be a reliable metric in predicting the threshold 
% of human contrast detection in natural scenes. A slight modification of RMS 
% contrast has been introduced in another study by Frasor and Geisler [45]. 
% The global contrast is given by:

%https://www.sciencedirect.com/science/article/abs/pii/S030105111100192X?via%3Dihub