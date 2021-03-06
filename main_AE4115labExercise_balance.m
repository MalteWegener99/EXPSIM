%% Main processing file LTT data AE4115 lab exercise 2020-2021
% T Sinnige
% 26 February 2021

%% Initialization
% clear workspace, figures, command window
clear 
close all
clc

%% Inputs
% enter group number 
groupNo = 23; 

% define root path on disk where data is stored
diskPath      = './group23/group23/BAL';

% get indices balance data files
[idxB] = SUP_getIdx;

% filename(s) of the raw balance files - DEFINE AS STRUCTURE WITH AS MANY FILENAMES AS DESIRED 
% The name of the file must start with "raw_". If the filename starts with
% a character that is not a letter, a plus sign, or a minus sign, the code
% will throw an error in BAL_process.m and you will have to add some code 
% there to handle the exception. (the filenames are used as fields in a 
% structure and these must start with a letter, so you will need to replace
% the first character with a letter. For the + and - signs this has already
% been implemented.
fn_BAL = {'raw_polar1.txt',...
          'raw_polar4.txt',...
          'raw_polar5.txt',...
          'raw_polar6.txt',...
          'raw_polar7.txt',...
          'raw_polar8.txt',...
          'raw_polar9.txt',...
          'raw_polar2.txt',...
          'raw_polar10.txt',...
          'raw_polar11.txt'};
      
% filename(s) of the zero-measurement (tare) data files. Define an entry
% per raw data files. In case multiple zero-measurements are available for
% a datapoint, then add a structure with the filenames of the zero 
% measurements at the index of that datapoint.
fn0 = {'zer_20210226_135105.txt',...
       'zer_20210226_120031.txt',...
       'zer_20210226_120031.txt',...
       'zer_20210226_120031.txt',...
       'zer_20210226_120031.txt',...
       'zer_20210226_120031.txt',...
       'zer_20210226_120031.txt',...
       'zer_20210226_135105.txt',...
       'zer_20210226_135105.txt',...
       'zer_20210226_135105.txt'}; 
 
% manual input of freestream conditions - ONLY USE FOR GROUPS 1-13 !! 
% enter vector of values per measurement file
operManual.vInf = {[40;40;40;40;20;20;20;20;30;30;30;30],...
                   [40;40;40;40;40;40;40;40;40;40;40;40]};
operManual.rhoInf = {[1.2;1.2;1.2;1.2;1.2;1.2;1.2;1.2;1.2;1.2;1.2;1.2],...
                     [1.2;1.2;1.2;1.2;1.2;1.2;1.2;1.2;1.2;1.2;1.2;1.2]};
operManual.tInf = {[288.15;288.15;288.15;288.15;288.15;288.15;288.15;288.15;288.15;288.15;288.15;288.15],...
                   [288.15;288.15;288.15;288.15;288.15;288.15;288.15;288.15;288.15;288.15;288.15;288.15]};

% wing geometry
b     = 1.4*cosd(4); % span [m]
cR    = 0.222; % root chord [m]
cT    = 0.089; % tip chord [m]
S     = b/2*(cT+cR);   % reference area [m^2]
taper = cT/cR; % taper ratio
c     = 2*cR/3*(1+taper+taper^2)/(1+taper); % mean aerodynamic chord [m]

% prop geometry
D        = 0.2032; % propeller diameter [m]
R        = D/2;   % propeller radius [m]

% moment reference points
XmRefB    = [0,0,0.0465/c]; % moment reference points (x,y,z coordinates) in balance reference system [1/c] 
XmRefM    = [0.25,0,0];     % moment reference points (x,y,z coordinates) in model reference system [1/c] 

% incidence angle settings
dAoA      = 0.0; % angle of attack offset (subtracted from measured values)   
dAoS      = 0.0;  % angle of sideslip offset (subtracted from measured values)
modelType = 'aircraft'; % options: aircraft, 3dwing, halfwing
modelPos  = 'inverted'; % options: normal, inverted
testSec   = 5;    % test-section number   

%% Run the processing code to get balance and pressure data
BAL = BAL_process(diskPath,fn_BAL,fn0,idxB,D,S,b,c,XmRefB,XmRefM,dAoA,dAoS,modelType,modelPos,testSec,groupNo,operManual);

%% Turn BAL data into .xls file (Optional)
xls_file_output(BAL,fn_BAL);

%% Write your code here
% Some labels
BAL.windOn.polar4.dr = 0;
BAL.windOn.polar5.dr = 0;
BAL.windOn.polar6.dr = 5;
BAL.windOn.polar7.dr = 5;
BAL.windOn.polar8.dr = 10;
BAL.windOn.polar9.dr = 10;

BAL.windOn.polar1.dr = 0;
BAL.windOn.polar2.dr = 0;
BAL.windOn.polar11.dr = 10;
BAL.windOn.polar10.dr = 10;
% Correct for Drag
BAL = CalcThrustCoeff(BAL,D);


BAL = apply_BC(BAL);

cnbeta = getCnbeta(BAL);