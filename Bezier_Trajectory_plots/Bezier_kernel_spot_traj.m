t= linspace(0,10,1000);
T = 10;

num = 22;
deg = num-1;
num_graphs = 50

%generate random points 
pts = rand(num_graphs,num,2)

%scale 
%lims = [-3,3];
pts(:,:,2) = -3 + 6*pts(:,:,2);
pts(:,:,1) = 10*pts(:,:,1);

   
[B, dB] = Bezier_kernal(t, deg);
for i= 1: num_graphs
    %condition points
    pts(i,:,1) = sort(pts(i,:,1));
    pts(i, 1, 1) = 0;
    pts(i, end, 1) = T;
    

    %bezier curves:
    P = B*squeeze(pts(i,:,:));
    dP = dB*squeeze(pts(i,:,:))/T;

    % plot
    subplot(2,1,1);
    line(P(:,1),P(:,2));
    line(squeeze(pts(i,:,1)),squeeze(pts(i,:,2)));
    title("Position");
    
    subplot(2,1,2); 
    line(P(:,1),dP(:,2));
    title("Velocity");

    saveas(gcf,compose("Traj_%d.png",i));
    close all;
        
end
% rand(4)* squeeze(pts(1,:,:))



