function CnCp = getCnCp(BAL)
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
    % Find Cnbeta 
    for i=1:length(polars)
        interp = scatteredInterpolant(BAL.windOn.(polars{i}).AoA,BAL.windOn.(polars{i}).AoS,BAL.windOn.(polars{i}).CP,BAL.windOn.(polars{i}).J_M1);
        beta = [0,2.5,5];
        alphas = [-3,0,5];
        cps = linspace(min(BAL.windOn.(polars{i}).CP),max(BAL.windOn.(polars{i}).CP),10);
        cps = cps(3:7);
        h = cps(2)-cps(1);
        on = ones(1,length(cps));
        dr = BAL.windOn.(polars{i}).dr;
        if mean(BAL.windOn.(polars{i}).V) < 30
            V = 20;
        else
            V = 40;
        end
        
        for a=1:length(alphas)
            for p=1:length(beta)
                CnCp.val(k) = mean(gradient(interp(on*alphas(a),beta(p)*on,cps),h));
                CnCp.beta(k) = beta(p);
                CnCp.alpha(k) = alphas(a);
                CnCp.V(k) = V;
                CnCp.dr(k) = dr;
                k= k + 1;
            end
        end
    end
end

