#include "automata.h"
#include <cstdio>
#include "cstdlib"
#include <map>
#include <string>
#include <set>
#include <iostream>  

automata::automata() {

  init=1;

  delta[1]['\0'].insert(3);
	delta[1]['b'].insert(2);
	delta[2]['a'].insert(2);
	delta[2]['a'].insert(3);
	delta[2]['b'].insert(3);
  delta[3]['a'].insert(1);
  
  
  S.insert(init);
  
}

automata::~automata() {}

void automata::print(states temp){
  states::iterator x = temp.begin();
  printf("[ ");
  while(x != temp.end()){
    std::cout << *x << " ";
    x++;
  }
  printf("] ");
}


states automata::closure(states S){

   states::iterator x = S.begin();
    while(x != S.end()){
    if(!delta[*x]['\0'].empty()){
      S.insert(delta[*x]['\0'].begin(),delta[*x]['\0'].end());
    }
     
      x++;  
    }

  return S;

}

states automata::steps(states S, char sigma){
  states T;
  states::iterator x = S.begin();
    while(x != S.end()){
      T.insert(delta[*x][sigma].begin(),delta[*x][sigma].end());
      x++;  
    }
    T=closure(T);
  return T;
}

bool automata::acceptance(states S){
  bool flag=false;
  states::iterator x = S.begin();
    while(x != S.end()){
      if(*x==2 || *x==3)flag=true;
      x++;
    }
    return flag;
}

states automata::sum(states A, states B){
   states::iterator x = A.begin();
    while(x != A.end()){
      B.insert(*x);
      x++;
    }

    return B;
}

bool automata::test(std::string cadena){
  S=closure(S);
  states T;
  for(int i=0;i<cadena.length(); i++){
    T=steps(S,cadena[i]);
    S=T;
    T.clear();
  }
  finals = S;
  if(acceptance(finals)) return true;
  else return false;
}


void automata::print(std::string cadena){
  printf("Entrada: %s\n", cadena.c_str());  
  S=closure(S);
  states T;
  printf("Init:   ");
  print(S);
  printf("\n \n");
  for(int i=0;i<cadena.length(); i++){
    T=steps(S,cadena[i]);
    printf("Step %c: ", cadena[i]);
    print(T);
    printf("\n");
    S=T;
    T.clear();
  }

  finals = S;

}