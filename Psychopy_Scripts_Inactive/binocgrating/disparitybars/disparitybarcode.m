clear
fname='C:\Users\schollb\Desktop\disparitybars';
verbose = 0;
prob = 0.20;
for trial = 1:10
    fnametrial = [fname,'\trial_',num2str(trial)];
    mkdir(fnametrial)
    
    numImgs = 11 * 15*5; %do batches of 165 (11 disparities (-300:60:300 px)
    nbars = 16;
    barsz = 60; %in px

    rng(trial)
    lookuptable = rand(nbars,numImgs);
    lookuptable(lookuptable<prob) = 0;
    lookuptable(lookuptable>1-prob) = 1; 
    lookuptable((lookuptable>prob) & (lookuptable<(1-prob))) = .5;%turn into -1,0,1
    
    blocks = 1:barsz:960; %bar size is 60px (~4-5 deg)
    for j = 1:numImgs
        im = zeros(960,960);
        for n = 1:nbars
            im(:,blocks(n):blocks(n)+barsz-1) = im(:,blocks(n):blocks(n)+barsz-1)+lookuptable(n,j);
        end
        %look
        if verbose
            win = zeros(960,1920);
            figure(99)
            colormap gray
            subplot(1,2,1)
            win(:,481:1440) = im;
            imagesc(win)
            subplot(1,2,2)
            win(:,(481:1440)+240) = im;
            imagesc(win)
            pause
        end
        %%%%save
        imwrite((im),[fnametrial,'/im_',sprintf('%.3d',j),'.png'],'png')
        fprintf .
    end
    
end