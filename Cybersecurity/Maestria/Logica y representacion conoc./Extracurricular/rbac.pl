% Hechos
usuario(ana).
usuario(juan).
usuario(luis).

rol(ana, administrador).
rol(juan, empleado).
rol(luis, visitante).

credencial_valida(ana).
credencial_valida(juan).

horario(dia).

suspendido(luis).

% Reglas de acceso
acceso(U) :-
    rol(U, administrador),
    credencial_valida(U).

acceso(U) :-
    rol(U, empleado),
    horario(dia),
    credencial_valida(U).

% Restricciones
no_acceso(U) :-
    rol(U, visitante).
no_acceso(U) :-
    suspendido(U).

% Analizador lógico de conflictos
conflicto(U) :-
    acceso(U),
    no_acceso(U).
