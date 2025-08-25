n(5).  % Cambia esto para calcular hasta ota cantidad de numeros

fac(0, 1).
fac(N1, F1) :- 
    fac(N, F), 
    n(Max), 
    N < Max, 
    N1 = N + 1, 
    F1 = F * N1.

% Mostrar solo los resultados finales (F)
fac_result(F) :- fac(_, F).

#show fac_result/1.
