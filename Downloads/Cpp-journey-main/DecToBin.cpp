#include<iostream>
using namespace std;
void decToBin(int n){
    int binNum = 0;
    int pow = 1; // 10^0, 10^1, 10^2, ...
    while(n>0){
        int rem = n%2;
        binNum += rem * pow;
        n = n/2;
        pow = pow*10;
    }
    cout<<"Binary Number is "<<"= "<<binNum<<endl;
}
int main(){
    decToBin(11);
    return 0;
}