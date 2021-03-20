function BALcor = apply_BC(BAL)
    Dp = 0.2032; % Prop disc diameter
    Sp = pi*Dp^2/4; % Prop disc area
    load('para/BCpara.mat');
    % CD0,eps_wb_0 ordered in increasing beta: 0,2,5,8,10
    % CLW,delta_CDW,delta_CM_qc,delta_CMqct ordered in increasing alfa: -3,-1,2,5,7
    
    % set up ordered matrices
    Bordershort = [1 2 2 3 3 3 4 4 5];
    Borderlong  = [3 2 2 4 4 1 3 3 3 5 2 2 4 4 3];
    CD0short    = [];
    epswb0short = [];
    for k=Bordershort
        CD0short(end+1)    = CD0(k);
        epswb0short(end+1) = eps_wb_0(k);
    end
    CD0long    = [];
    epswb0long = [];
    for k=Borderlong
        CD0long(end+1)    = CD0(k);
        epswb0long(end+1) = eps_wb_0(k);
    end
    
    Aordershort = [3 2 4 1 3 5 2 4 3];
    Aorderlong  = [3 2 4 2 4 3 1 3 5 3 2 4 2 4 3];
    CLWshort = [];
    delta_alfashort = [];
    delta_CDWshort = [];
    delta_CM_qcshort = [];
    delta_CMqctshort = [];
    for k=Aordershort
%         CLWshort(end+1)         = CLW(k); % not used
        delta_alfashort(end+1)  = delta_alfa(k);
        delta_CDWshort(end+1)   = delta_CDW(k);
        delta_CM_qcshort(end+1) = delta_CM_qc(k);
        delta_CMqctshort(end+1) = delta_CMqct(k);
    end
    CLWlong = [];
    delta_alfalong = [];
    delta_CDWlong = [];
    delta_CM_qclong = [];
    delta_CMqctlong = [];
    
    for k=Aorderlong
%         CLWlong(end+1)         = CLW(k);
        delta_alfalong(end+1)  = delta_alfa(k);
        delta_CDWlong(end+1)   = delta_CDW(k);
        delta_CM_qclong(end+1) = delta_CM_qc(k);
        delta_CMqctlong(end+1) = delta_CMqct(k);
    end
    
    p = fieldnames(BAL.windOn);
    for i=1:length(p)
       CT  = BAL.windOn.(p{i}).CT;
       if length(BAL.windOn.(p{i}).CT) < 14 % Prop off - no slipstream
           eps_ss = 0;
           cd0 = CD0short;
           epswb0 = epswb0short;
           clw = CLWshort;
           del_cdw = delta_CDWshort;
           del_cm_qc = delta_CM_qcshort;
           del_cm_qct = delta_CMqctshort;
           del_alfa = delta_alfashort;
           
       else
           eps_ss = -1*CT./2/sqrt(1+2.*CT); % Prop on
           cd0 = CD0long;
           epswb0 = epswb0long;
           clw = CLWlong;
           del_cdw = delta_CDWlong;
           del_cm_qc = delta_CM_qclong;
           del_cm_qct = delta_CMqctlong;
           del_alfa = delta_alfalong;
       end
       
       qunc    = BAL.windOn.(p{i}).q;
       Vunc    = BAL.windOn.(p{i}).V;
       AoS     = BAL.windOn.(p{i}).AoS;
       CLunc   = BAL.windOn.(p{i}).CL;
       CDunc   = BAL.windOn.(p{i}).CD;
       CMqcunc = BAL.windOn.(p{i}).CMp25c;
       AoAg    = BAL.windOn.(p{i}).AoA; % geometric AoA
       
       % Corrections
       epswbs = 5*S/4/C.*(CDunc-cd0-CDi);
       check  = epswbs>=0;
       epswbs = epswbs.*check;
       eps = eps_ss + eps_sb + epswb0 + epswbs;
       BAL.windOn.(p{i}).q = qunc.*(1+eps).^2;
       BAL.windOn.(p{i}).V = Vunc.*(1+eps);
       BAL.windOn.(p{i}).CL = CLunc.*(1+eps).^(-2);
       BAL.windOn.(p{i}).CD = CDunc.*(1+eps).^(-2);
       BAL.windOn.(p{i}).CMp25c = CMqcunc.*(1+eps).^(-2);
       BAL.windOn.(p{i}).AoA = AoAg + del_alfa;
       
       CDunc = BAL.windOn.(p{i}).CD; % CD is corrected twice
       BAL.windOn.(p{i}).CD = CDunc + del_cdw;
       
       CMqcunc = BAL.windOn.(p{i}).CMp25c; % CM0.25c is corrected twice as well
       BAL.windOn.(p{i}).CMp25c = del_cm_qc + del_cm_qct;

    end
    BALcor = BAL;
    disp('corrections applied')
end