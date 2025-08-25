father(juan, maria).
mother(pedro, ana).

parent(X,Y) :- father(X,Y).
parent(X,Y) :- mother(X,Y).

#show parent/2.
