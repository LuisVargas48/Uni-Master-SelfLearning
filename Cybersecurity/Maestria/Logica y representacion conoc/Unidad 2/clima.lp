% Hechos: temperaturas por ciudad
temp(cdmx, 24).
temp(puebla, 24).
temp(leon, 25).
temp(san_luis_potosi, 27).
temp(aguascalientes, 25).
temp(guadalajara, 25).
temp(monterrey, 36).
temp(ciudad_juarez, 29).

% Reglas para clasificar el clima
templado(C) :- temp(C, T), T < 25.
calido(C)   :- temp(C, T), T > 25.

% Mostrar solo las ciudades clasificadas
#show templado/1.
#show calido/1.
