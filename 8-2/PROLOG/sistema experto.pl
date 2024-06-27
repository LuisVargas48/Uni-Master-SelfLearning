
es_un(auto,vehiculo).
es_un(moto,vehiculo).
es_un(lancha,vehiculo).
es_un(ford,auto).
es_un(nissan,auto).
es_un(ducati,moto).
es_un(honda,moto).





atributo(vehiculo,puede,transportar).
atributo(auto,tiene,llantas_4).
atributo(auto,necesita,gasolina).
atributo(moto,tiene,llantas_2).
atributo(ducati,es,ligera).





unico(nissan,carroceria,comercial).
unico(nissan,necesita,super).
unico(ferrari,es,rapido).
unico(ducati,es,rapida).
unico(ducati,es,cara).
unico(ford,necesita,diesel).



%reglas


necesita_diesel(X):-es_un(X,auto), not(unico(X,necesita,super)).

moto_cara(X):-es_un(X,moto),unico(X,es,cara),!.

puede_transportar(X):-atributo(X,puede,transportar).
puede_transportar(X):-es_un(X,Y),puede_transportar(Y).

cuatro_llantas(X):-atributo(X,tiene,llantas_4).
cuatro_llantas(X):-es_un(X,Y),cuatro_llantas(Y).
