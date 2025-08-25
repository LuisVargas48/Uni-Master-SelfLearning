% Hechos 
padre(ana, juan). 
padre(juan, karina). 
padre(juan, dany). 

% Regla para deducir hijo. 

hijo(X,Y) :- padre(Y,X). 

% Mostrar la relacion hijo. 

#show hijo/2.