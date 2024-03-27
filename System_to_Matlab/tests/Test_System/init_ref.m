%% System parameters
g = 9.81;
m2 = 1.866;
m3 = 2.173;
s2 = 0.125;
s3 = 0.131;
l2 = 0.25;
l3 = 0.25;
BS1 = 0.103;
AS2 = 0.0036;
BS2 = 0.0159;
CS2 = 0.017;
AS3 = 0.0021;
BS3 = 0.018;
CS3 = 0.0583;
iG1 = 72;
iG2 = 72;
iG3 = 72;
BM1 = 1.89e-05;
CM2 = 1.89e-05;
CM3 = 1.89e-05;
params = [g, m2, m3, s2, s3, l2, l3, BS1, AS2, BS2, CS2, AS3, BS3, CS3, iG1, iG2, iG3, BM1, CM2, CM3]; 
 
%% Initial conditions
x_ic = [0; 0; 0; 0; 0; 0];
