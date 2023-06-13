function [B, dB] = Bezier_kernel(t, deg)
    t = reshape(t, length(t), 1);
    B = zeros(length(t), deg + 1);
    dB = zeros(length(t), deg + 1);
    % ddB = zeros(length(t), deg + 1);
%     B = sym(B); dB = sym(dB); ddB = sym(ddB);
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
        
        % if (deg - i - 1 > 0)
        %     ddB(:, i + 1) = ddB(:, i + 1) + coeff.*(1 - t).^(deg - i - 2).*(deg - i - 1).*(deg - i).*t.^i;
        % end
        % if (deg - i > 0 && i > 0)
        %     ddB(:, i + 1) = ddB(:, i + 1) + 2.*coeff.*(1 - t).^(deg - i - 1).*(deg - i).*-1.*t.^(i - 1).*i ;
        % end
        % if (i - 1 > 0)
        %     ddB(:, i + 1) = ddB(:, i + 1) + coeff.*(1 - t).^(deg - i).*t.^(i - 2).*i.*(i - 1);
        % end
    end
end
