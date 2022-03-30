contrastValues =        [0.05 0.20 0.35 0.50 0.65 0.80 0.95];
luminanceValues =       [-0.90 -0.75 -0.60 -0.45 -0.30 -0.15 0];
spatialFrequencies =    [0.04 0.08 0.12 0.16];
disparityPhases =       [0 0.25 0.50 0.75];
directions =            [0 90]; %run changeDir

%generate stimulus combinations
binocStimParams = [];
cnt = 0;
for c1 = 1:length(contrastValues)
    for c2 = 1:length(contrastValues)
        cnt = cnt + 1;
        binocStimParams(cnt,:) = [contrastValues(c1) contrastValues(c2)...
            luminanceValues(c1) luminanceValues(c2)];
    end
end


%increase the frequency of some stimulus combinations (want max of 3)
d = round(binocStimParams(:,1)-binocStimParams(:,2),2);
% figure(1); subplot(1,2,1);hist(d,-1:0.05:1)
dvs = round(unique(d),2);

addbinocStimParams  = [];
for j = 1:length(dvs)
    if sum(d>dvs(j)-.01 & d<dvs(j)+.01)==1
       for cnt = 1:3
           addbinocStimParams = [addbinocStimParams; binocStimParams(d==dvs(j),:)];
       end
    elseif sum(d>dvs(j)-.01 & d<dvs(j)+.01)==2
        addbinocStimParams = [addbinocStimParams; binocStimParams(d==dvs(j),:)];
    elseif sum(d>dvs(j)-.01 & d<dvs(j)+.01)==3
        id = find(d==dvs(j));
        addbinocStimParams = [addbinocStimParams; binocStimParams(id(end),:)];
    end
end

binocStimParams = [binocStimParams; addbinocStimParams];
d = (binocStimParams(:,1)-binocStimParams(:,2));
% figure(1); subplot(1,2,2);hist(d,-1:0.05:1)


%create stimulus arrays
numStim = size(binocStimParams,1) *...
    length(spatialFrequencies) *...
    length(disparityPhases) *...
    length(directions);

stimMat = [];
cnt = 0;
for b = 1:size(binocStimParams,1)
    for s = 1:length(spatialFrequencies)
        for d = 1:length(disparityPhases)
            for dir = 1:2
                cnt = cnt+1;
                stimMat(cnt,:) = [binocStimParams(b,:) ...
                    spatialFrequencies(s) ...
                    disparityPhases(d) ...
                    directions(dir)];
            end
        end
    end
end

%save stimulus arrays
fileloc = 'Y:\Ben\binocMismatchParams\';
for s = 1:size(stimMat,2)
    fileID = fopen([fileloc,'\dataType_',num2str(s),'.txt'],'w');
    fprintf(fileID,'%2f\n',stimMat(:,s))
    fclose(fileID)
    if s==size(stimMat,2)
        id = stimMat(:,s)==90;
        stimMat(id,s) = 270;
        fileID = fopen([fileloc,'\dataType_',num2str(s+1),'.txt'],'w');
        fprintf(fileID,'%2f\n',stimMat(:,s))
        fclose(fileID)
    end
end

%save stimMatrix
save([fileloc,'\stimMat'],'stimMat')


