% === Hechos ===

puerto_abierto(host1, 80).
puerto_abierto(host2, 22).

trafico_sospechoso(host1).
conexion_ssh_externa(host2).

intentos_fallidos(usuario1, 7, 50).
usuario_inactivo(usuario1).

% === Reglas ===

% Regla 1: tráfico sospechoso en puerto 80 implica posible intrusión
posible_intrusion(Host) :-
    puerto_abierto(Host, 80),
    trafico_sospechoso(Host).

% Regla 2: conexión SSH externa en puerto 22 implica posible intrusión
posible_intrusion(Host) :-
    puerto_abierto(Host, 22),
    conexion_ssh_externa(Host).

% Regla 3: más de 5 intentos fallidos en 60 segundos es actividad sospechosa
actividad_sospechosa(User) :-
    intentos_fallidos(User, N, T),
    N > 5,
    T =< 60.

% Regla 4: si hay actividad sospechosa y el usuario está inactivo, es atacante
atacante(User) :-
    actividad_sospechosa(User),
    usuario_inactivo(User).
