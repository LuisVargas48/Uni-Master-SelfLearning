#ifndef __automata_
#define __automata_

#include "automata.h"
#include <string>
#include <string>
#include <map>
#include <set>

typedef std::set<unsigned> states;
typedef std::map<char,states> event;
typedef std::map<unsigned, event> transition;


class automata {

  transition delta;
  int init;
  states finals;
  
  void print(states);
  states closure(states);
  states steps(states,char);
  bool acceptance(states);
  states sum(states,states);

public:

  automata ();
  ~automata();

  states S;


  
  bool test(std::string);
  void print(std::string);

  
};
#endif