function Cnbeta = getCnbeta(BAL)
    p = fieldnames(BAL.windOn);
    j = 1;
    for i=1:length(p)
        if length(BAL.windOn.(p{i}).V) < 14
            continue
        end
        polars{j} = p{i};
        j=j+1;
    end
    k = 1;
    h = 0.2;
    data = {};
    % Find Cnbeta 
    for i=1:length(polars)
        for j=1:15
            data.Cn(k,1) = BAL.windOn.(polars{i}).CMy(j)';
            data.Cp(k,1) = BAL.windOn.(polars{i}).CMr(j)';
            data.J(k,1) = (BAL.windOn.(polars{i}).J_M1(j)*10)/10;
            data.a(k,1) = (BAL.windOn.(polars{i}).AoA(j));
            data.ac(k,1) = round(BAL.windOn.(polars{i}).AoA(j));
            data.b(k,1) = (BAL.windOn.(polars{i}).AoS(j));
            data.bc(k,1) = (BAL.windOn.(polars{i}).AoS(j));
            data.V(k,1) = round(BAL.windOn.(polars{i}).V(j)/10)*10;
            data.dr(k,1) = BAL.windOn.(polars{i}).dr;
            data.CT(k,1) = BAL.windOn.(polars{i}).CTh(j);
            k = k+1;
        end
    end
    writetable(struct2table(data), 'datapoints.csv')
    
    %% new section
    p = fieldnames(BAL.windOn);
    j = 1;
    for i=1:length(p)
        if length(BAL.windOn.(p{i}).V) > 10
            continue
        end
        polars{j} = p{i};
        j=j+1;
    end
    k = 1;
    h = 0.2;
    data = {};
    % Find Cnbeta 
    for i=1:length(polars)
        for j=1:9
            data.Cn(k,1) = BAL.windOn.(polars{i}).CMy(j)';
            data.Cp(k,1) = BAL.windOn.(polars{i}).CMr(j)';
            data.J(k,1) = (BAL.windOn.(polars{i}).J_M1(j)*10)/10;
            data.a(k,1) = (BAL.windOn.(polars{i}).AoA(j));
            data.ac(k,1) = round(BAL.windOn.(polars{i}).AoA(j));
            data.b(k,1) = (BAL.windOn.(polars{i}).AoS(j));
            data.bc(k,1) = (BAL.windOn.(polars{i}).AoS(j));
            data.V(k,1) = round(BAL.windOn.(polars{i}).V(j)/10)*10;
            data.dr(k,1) = BAL.windOn.(polars{i}).dr;
            data.CT(k,1) = 0;
            k = k+1;
        end
    end
    writetable(struct2table(data), 'datapoints-unpowered.csv')
end

