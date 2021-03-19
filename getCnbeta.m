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
    % Find Cnbeta 
    for i=1:length(polars)
        interp = scatteredInterpolant(BAL.windOn.(polars{i}).AoA,BAL.windOn.(polars{i}).AoS,BAL.windOn.(polars{i}).J_M1,BAL.windOn.(polars{i}).CYaw);
        beta = 0:h:5;
        alphas = [-1,0,5];
        cps = [1.68,1.8,1.92];
        on = ones(1,length(beta));
        dr = BAL.windOn.(polars{i}).dr;
        if mean(BAL.windOn.(polars{i}).V) < 30
            V = 20;
        else
            V = 40;
        end
        
        for a=1:length(alphas)
            for p=1:length(cps)
                Cnbeta.val(k) = mean(gradient(interp(on*alphas(a),beta,on*cps(p)),h));
                Cnbeta.J(k) = cps(p);
                Cnbeta.alpha(k) = alphas(a);
                Cnbeta.V(k) = V;
                Cnbeta.dr(k) = dr;
                k= k + 1;
            end
        end
    end
end

