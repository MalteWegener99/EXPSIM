function BAL2 = CalcThrustCoeff(BAL,D)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
BAL2 = BAL;

polars = fieldnames(BAL.windOn);
for i=1:length(polars)
    if length(BAL.windOn.(polars{i}).V) < 14
        continue
    end
    display(polars{i})
    drag20_0 = griddata(round(BAL.windOn.polar2.AoA*20)/20,round(BAL.windOn.polar2.AoS*20)/20,BAL.windOn.polar2.CD,round(BAL.windOn.(polars{i}).AoA*20)/20,round(BAL.windOn.(polars{i}).AoS*20)/20);
    drag40_0 = griddata(round(BAL.windOn.polar1.AoA*20)/20,round(BAL.windOn.polar1.AoS*20)/20,BAL.windOn.polar1.CD,round(BAL.windOn.(polars{i}).AoA*20)/20,round(BAL.windOn.(polars{i}).AoS*20)/20);
    drag20_10 = griddata(round(BAL.windOn.polar11.AoA*20)/20,round(BAL.windOn.polar11.AoS*20)/20,BAL.windOn.polar11.CD,round(BAL.windOn.(polars{i}).AoA*20)/20,round(BAL.windOn.(polars{i}).AoS*20)/20);
    drag40_10 = griddata(round(BAL.windOn.polar10.AoA*20)/20,round(BAL.windOn.polar10.AoS*20)/20,BAL.windOn.polar10.CD,round(BAL.windOn.(polars{i}).AoA*20)/20,round(BAL.windOn.(polars{i}).AoS*20)/20);
    if mean(BAL.windOn.(polars{i}).V) < 30
        if BAL.windOn.(polars{i}).dr == 0
            drag = drag20_0;
        elseif BAL.windOn.(polars{i}).dr == 10
            drag = drag20_10;
        elseif BAL.windOn.(polars{i}).dr == 5
            drag = 0.5*(drag20_0+drag20_10);
        else
            error("Fuck 20")
        end
        tmp = -(BAL2.windOn.(polars{i}).CD-drag).*BAL2.windOn.(polars{i}).q.*BAL2.windOn.(polars{i}).S;
        BAL2.windOn.(polars{i}).CTh = tmp./(BAL2.windOn.(polars{i}).rpsM1).^2./BAL2.windOn.(polars{i}).rho./(D^4);
        BAL2.windOn.(polars{i}).CD = drag;
        BAL2.windOn.(polars{i}).CP = BAL2.windOn.(polars{i}).CTh.*BAL2.windOn.(polars{i}).V./D./BAL2.windOn.(polars{i}).rpsM1;
    elseif mean(BAL.windOn.(polars{i}).V) > 30
        if BAL.windOn.(polars{i}).dr == 0
            drag = drag40_0;
        elseif BAL.windOn.(polars{i}).dr == 10
            drag = drag40_10;
        elseif BAL.windOn.(polars{i}).dr == 5
            drag = 0.5*(drag40_0+drag40_10);
        else
            error("Fuck 40")
        end
        tmp = -(BAL2.windOn.(polars{i}).CD-drag).*BAL2.windOn.(polars{i}).q.*BAL2.windOn.(polars{i}).S;
        BAL2.windOn.(polars{i}).CTh = tmp./(BAL2.windOn.(polars{i}).rpsM1).^2./BAL2.windOn.(polars{i}).rho./(D^4);
        BAL2.windOn.(polars{i}).CD = drag;
        BAL2.windOn.(polars{i}).CP = BAL2.windOn.(polars{i}).CTh.*BAL2.windOn.(polars{i}).V./D./BAL2.windOn.(polars{i}).rpsM1;
    else
        error('Fuck')
    end
end

