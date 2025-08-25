% Parámetros simbólicos (asignados como hechos)
a(1).
b(1).
c(41).
n(10).

% Regla que aplica el polinomio
p(N, A*N*N + B*N + C) :- 
    a(A), b(B), c(C), n(L), N = 0..L.

#show p/2.
