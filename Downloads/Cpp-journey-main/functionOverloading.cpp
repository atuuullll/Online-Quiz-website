#include<iostream>
using namespace std;
int sum(int a, int b){
    cout<<(a+b)<<endl;
    return a+b;
}
int sum(double a, double b){
    cout<<(a+b)<<endl;
    return a+b;
}
int main(){
    sum(5,6);
    sum(5.5,6.3);
    return 0;
}