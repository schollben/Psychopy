clear
fname='Y:\Ben\spatialcloudstimulus\';

savematimages = 1;
savepngs = 1;

%%%%notes for 2017-Oct-30: 
%%%%going to draw a 700x700 pixel image in PsychoPy so that means
%%%%that 50 x 50 checker will be 14.5 x 14.5 pixels per checker on the screen
%%%%and we assume RFs ~10 deg (~145 true pixels)
%%%%also: plan on stimulating a 4Hz or 8Hz (while imaging at 30Hz)
% % % % STIM PARAMETERS
% % % w = 50;
% % % h = 50; 
% % % spatial_scale = 10; 
% % % num_frames = 10e3; %4000 or 10000 frame chunks?

%%%%notes for 2018-Jan-25: 
%%%%going to draw a 1080x1080 pixel image in PsychoPy so that means
%%%%that 48 x 48 checker will be 22.5 x 22.5 pixels per checker on the screen
%%%%plan here is to overlap the wn-dense stimulus over this one
%%%%5 trials non-thresholded and 5 thresholded?

%%%%notes for 2018-June-04
%%%%

w = 48;
h = 48; 
spatial_scale = 10; 
num_frames = 50001; 

for trial = 1:4
    fnametrial = [fname,'\px_',num2str(w),'_spatscal_',num2str(spatial_scale),'_trial_',num2str(trial)];
    mkdir(fnametrial)
    
    seed = trial;
    rng(seed);
    
    % Start with gaussian white noise (on larger square)
    L = max([w h]);
    noise_stim = randn(num_frames,L,L);
    
    % Start with gaussian white noise (on larger square)
    L = max([w h]);
    noise_stim = randn(num_frames,L,L);
    
    % 2-D Gaussian mask
    xs=(0:(L-1))-L/2;  %%%%%%%%%%%%%%%
    r2s = xs'.^2*ones(1,L) + ones(L,1)*xs.^2;
    rad1 = 2*L/pi/spatial_scale;
    mask1 = exp(-r2s/(2*rad1^2));
    mask1 = mask1/max(mask1(:));
    
    stim = zeros(num_frames,w,h);
    
    for k =	1:num_frames
        %im1 = baserand2(:,:,k);
        im1 = squeeze(noise_stim(k,:,:));
        manip1 = fftshift(fft2(im1));
        % figure; imagesc(fx,fy,log(abs(manip1))); colorbar;
        manip2 = mask1.*manip1;
        im2 = ifft2(ifftshift(manip2)); %%%%%%%%%%
        stim(k,:,:) = im2(1:w,1:h);
    end
    stim = stim/std(stim(:));
   
    stim = stim - min(stim(:));
    stim = stim./max(stim(:));
    
    if savematimages
        saveloc = 'Y:\Ben\spatialcloudstimulus\matimages\2018-Jun-04\';
        save([saveloc,'\stim_trial',num2str(trial)],'stim')
    end
    
    
    if savepngs
    for j = 1:num_frames
        im = squeeze(stim(j,:,:));
        imwrite((im),[fnametrial,'\im_',sprintf('%.4d',j),'.png'],'png')
        fprintf .
    end
    end
end
disp DONE