% Jugadores. 
jugador(x, luis).
jugador(o, olivia).

% Posiciones del tablero (1 a 3 en filas y columnas)
fila(1..3).
col(1..3).

% Jugadas hechas (puedes editar estas para probar)
jugada(1,1,x).
jugada(1,2,x).
jugada(1,3,x).

jugada(2,1,o).
jugada(2,2,o).
jugada(3,1,o).

% Regla: gana X si hay 3 en fila
gana(x) :- jugada(R,1,x), jugada(R,2,x), jugada(R,3,x), fila(R).

% Regla: gana O si hay 3 en fila
gana(o) :- jugada(R,1,o), jugada(R,2,o), jugada(R,3,o), fila(R).

% Regla: gana por columna
gana(x) :- jugada(1,C,x), jugada(2,C,x), jugada(3,C,x), col(C).
gana(o) :- jugada(1,C,o), jugada(2,C,o), jugada(3,C,o), col(C).

% Regla: gana por diagonal
gana(x) :- jugada(1,1,x), jugada(2,2,x), jugada(3,3,x).
gana(x) :- jugada(1,3,x), jugada(2,2,x), jugada(3,1,x).

gana(o) :- jugada(1,1,o), jugada(2,2,o), jugada(3,3,o).
gana(o) :- jugada(1,3,o), jugada(2,2,o), jugada(3,1,o).

%Mostrar el ganador con su nombre. 

ganador(Nombre) :- gana(S), jugador(S,Nombre). 

#show ganador/1.
