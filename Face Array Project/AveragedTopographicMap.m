startTime = .1;
endTime = .2;
region = [5,9,10,15,20,21,26,27,16,17,18];

Path = 'C:\Users\PL003A\Desktop\Multiple Faces\Results';
ft_defaults
cd(Path)

for n = 1:36
    if n<10
        Filename = ['Antic_0',num2str(n),'.mat'];
    else
        Filename = ['Antic_',num2str(n),'.mat'];
    end
    
    Subject{n} = load(Filename);
end

cfg = [];
cfg.keepindividual = 'yes';

A1 = cell(1,36); A2 = cell(1,36); A3 = cell(1,36);
for n = 1:36
    A1{n} = Subject{n}.A1;
    A2{n} = Subject{n}.A2;
    A3{n} = Subject{n}.A3;
end

EEG_avgA1 = ft_timelockgrandaverage(cfg, A1{:});
EEG_avgA2 = ft_timelockgrandaverage(cfg, A2{:});
EEG_avgA3 = ft_timelockgrandaverage(cfg, A3{:});

cfg = [];
cfg.parameter = 'individual';
cfg.keepindividual = 'yes';
smallAveraged = ft_timelockgrandaverage(cfg, EEG_avgA2, EEG_avgA3);

cfg = [];
cfg.parameter = 'individual';
cfg.operation = 'x2 - x1';  
differenceWave = ft_math(cfg, EEG_avgA1, smallAveraged);

cfg = [];
%cfg.channel = Region;
cfg.xlim = [startTime, endTime];
cfg.layout = 'acticap-64ch-standard2.mat';
figure
ft_multiplotER(cfg, differenceWave);

figure
cfg = [];
cfg.xlim = [startTime, endTime];
cfg.comment         = 'no';
cfg.zlim            = [-.5, .5];
cfg.marker          = 'off';
cfg.colorbar        = 'southoutside';
cfg.layout = 'acticap-64ch-standard2.mat';
ft_topoplotER(cfg, differenceWave);