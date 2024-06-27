#include <iostream>
#include <map>
#include <string>
#include "automata.h"

using namespace std;


int main(int argc, const char * argv[]) {

    automata autom;
    autom.print("aaabbb");
    autom.test("aaabbb") ? printf("Aceptado") : printf("Rechazado");

	return 0;
}