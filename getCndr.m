function Cndr = getCndr(inputArg1,inputArg2)
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
    % Find Cndr
    for i=1:length(polars)
        interp = scatteredInterpolant(BAL.windOn.(polars{i}).AoA,BAL.windOn.(polars{i}).AoS,BAL.windOn.(polars{i}).CP,BAL.windOn.(polars{i}).CYaw);
end

