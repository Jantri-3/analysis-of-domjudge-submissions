#include <stdlib.h>
#include <limits>
#include <iostream>

using namespace std;

void * p;

int main() {
    int tries[3];
    for (int i = 0; i < 3; i++)
    {
        tries[i] = i;
    }
    tries[2] = tries[2];//selfAssignment

    if (tries[2] == 2);//suspicious semicolon
    {
        tries[1] = 7;
    }
    
    p = malloc(7);//memory leak
    p = 0;

    int j = numeric_limits<int>::max(); //Unused variable
    j += 1;

    cout << "Incorrect solution with all kinds of errors" << "\n";
    

    return 0;
    tries [1] = tries[0];//unreachableCode
}