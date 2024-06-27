padre(martin,olivia).
padre(martin,mina).
madre(olivia_felix,olivia).
madre(olivia_felix,mina).
madre(olivia,luis).
madre(mina,gisela).
hermano(X,Y):- padre(Z,X), padre(Z,Y),madre(A,X),madre(A,Y).
primo(X,Y):- hermano(Z,A),madre(A,Y),madre(Z,X),not(X=Y).