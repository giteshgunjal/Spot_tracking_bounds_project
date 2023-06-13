%Hello! this will plot Bezier curve for n control points 
%This is a replacement of the program 'Parametic Cubic Bezier Curve'
%submitted before ...Bezier for any number of points ...enjoy 
clear all 
clc
n=input('Enter no. of points  ');
w=input('Press 1 for entry through mouse or 2 for keyboard repectively-->');
deg=n-1;
if w==1
    axis([0 10 -3 3])
    [p]=ginput(n);
end
if w==2
    [p]=input('Enter co-odinates of points within brackets ->[x1 y1;x2 y2;x3 y3;...;xn yn] ');
     end
% lets consider only 10sec traj
% T =10;
t = linspace(0,1,1000)' ;
size(t)
B = zeros(length(t), deg + 1);
dB = zeros(length(t), deg + 1);
for i = 0:deg
    coeff = factorial(deg)/factorial(i)/factorial(deg - i);
    B(:, i + 1) = coeff.*(1 - t).^(deg - i).*t.^i;
    
    % All of these conditionals fix an annoying thing where
    % 0.*t.^(-1) = NaN if t = 0, which makes this way of applying the
    % power rule for derivatives not work.
    
    if (deg - i > 0)
        dB(:, i + 1) = dB(:, i + 1) + coeff.*(1 - t).^(deg - i - 1).*(deg - i).*-1.*t.^i;
    end
    if (i > 0)
        dB(:, i + 1) = dB(:, i + 1) + coeff.*(1 - t).^(deg - i).*t.^(i - 1).*i;
    end
    
end
%pts = p;

%pts(:,1) = (pts(:,1) - p(1,1))/(p(end,1)-p(1,1));
P=B*p;
dp = dB*p/(p(end,1)-p(1,1));
Diff = diff(P(:,2))/(0.001* (p(end,1)-p(1,1)))


%p(end,1)-p(1,1)
%dp(:,1) = p(1,1) + (p(end,1)-p(1,1))*dp(:,1)
% line(P(:,1),dp(:,2))
% % line(P(1:length(Diff),1),Diff, 'Color','red')
% line(P(:,1),P(:,2))
% line(p(:,1),p(:,2))

% books for reference on the subject of cad/cam author Roger Adams  ,
% Ibrahim Zeid 
%Prepared by Mechanical engg. student NIT Allahabad , India
% for any questions feel free to mail me at slnarasimhan89@gmail.com