#include<iostream>
using namespace std;

// void firstfunction(){
//     cout<<"This is my first function code"<<endl;
// }
// int main(){
//     firstfunction();
//     return 0;
// }

void secondfunction(int a, int b){
    cout<<"Value of a is: "<<a<<endl;
    cout<<"Value of b is: "<<b<<endl;
    cout<<"The sum of a and b is: "<<a+b<<endl;
}

void product(int a, int b){
    cout<<"The sum of a and b is: "<<a*b<<endl;
}
void diff(int a, int b){
    cout<<"The difference of a and b is: "<<a-b<<endl;
}
int main(){
    product(4,5);
    diff(5,4);
    return 0;
}