% --- Hechos del sistema ---
usuario(ana). usuario(juan). usuario(luis).

rol(ana, administrador).
rol(juan, empleado).
rol(luis, visitante).

credencial_valida(ana).
credencial_valida(juan).
% luis no tiene credencial válida

horario(dia).

suspendido(luis).

% --- Políticas de acceso ---

% Los administradores tienen acceso siempre que tengan credencial válida
acceso(U) :- usuario(U), rol(U, administrador), credencial_valida(U).

% Los empleados tienen acceso solo en horario de día y con credencial válida
acceso(U) :- usuario(U), rol(U, empleado), horario(dia), credencial_valida(U).

% Los visitantes no tienen acceso
:- acceso(U), rol(U, visitante).

% Nadie suspendido puede tener acceso
:- acceso(U), suspendido(U).

% --- Consultas ---
#show acceso/1.
