function BAL2 = CalcThrustCoeff(BAL,D)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
BAL2 = BAL;
drag20 = griddata(round(BAL.windOn.polar2.AoA*20)/20,round(BAL.windOn.polar2.AoS*20)/20,BAL.windOn.polar2.CD,round(BAL.windOn.polar4.AoA*20)/20,round(BAL.windOn.polar4.AoS*20)/20);
drag40 = griddata(round(BAL.windOn.polar11.AoA*20)/20,round(BAL.windOn.polar11.AoS*20)/20,BAL.windOn.polar11.CD,round(BAL.windOn.polar4.AoA*20)/20,round(BAL.windOn.polar4.AoS*20)/20);
polars = fieldnames(BAL.windOn);
for i=1:length(polars)
    if length(BAL.windOn.(polars{i}).V) < 14
        continue
    end
    display(polars{i})
    if mean(BAL.windOn.(polars{i}).V) < 30
        tmp = -(BAL2.windOn.(polars{i}).CD-drag20).*BAL2.windOn.(polars{i}).q.*BAL2.windOn.(polars{i}).S;
        BAL2.windOn.(polars{i}).CTh = tmp./(BAL2.windOn.(polars{i}).rpsM1).^2./BAL2.windOn.(polars{i}).rho./(D^4);
        BAL2.windOn.(polars{i}).CD = drag20;
        BAL2.windOn.(polars{i}).CP = BAL2.windOn.(polars{i}).CTh.*BAL2.windOn.(polars{i}).V./D./BAL2.windOn.(polars{i}).rpsM1;
    elseif mean(BAL.windOn.(polars{i}).V) > 30
        tmp = -(BAL2.windOn.(polars{i}).CD-drag40).*BAL2.windOn.(polars{i}).q.*BAL2.windOn.(polars{i}).S;
        BAL2.windOn.(polars{i}).CTh = tmp./(BAL2.windOn.(polars{i}).rpsM1).^2./BAL2.windOn.(polars{i}).rho./(D^4);
        BAL2.windOn.(polars{i}).CD = drag40;
        BAL2.windOn.(polars{i}).CP = BAL2.windOn.(polars{i}).CTh.*BAL2.windOn.(polars{i}).V./D./BAL2.windOn.(polars{i}).rpsM1;
    else
        error('Fuck')
    end
end

