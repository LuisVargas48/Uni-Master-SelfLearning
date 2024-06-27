progenitor(clara,jose).
progenitor(tomas, jose).
progenitor(tomas,isabel).
progenitor(jose, ana).
progenitor(jose, patricia).
progenitor(patricia,jaime).

abuelo(A,E):- progenitor(B,E),progenitor(A,B).
hermano(E,F):- progenitor(B,E),progenitor(B,F).
tio(D,E):- progenitor(B,E), hermano(D,B).