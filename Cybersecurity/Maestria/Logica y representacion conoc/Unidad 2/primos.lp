n(20).  % Límite superior para N. 

% Un número N es compuesto si hay un divisor I entre 2 y N-1
compuesto(N) :- n(L), N = 2..L, I = 2..N-1, N \ I == 0.

% Un número N es primo si no es compuesto
prime(N) :- n(L), N = 2..L, not compuesto(N).

#show prime/1.
