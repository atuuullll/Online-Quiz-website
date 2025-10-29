#include<iostream>
using namespace std;

void binToDec(int n){
    int decNum = 0;
    int pow =1; // 2^0, 2^1, 2^2, ...
    while(n>0){
        int lastDigit = n%10;
        decNum += lastDigit * pow;
        pow = pow*2;
        n = n/10;
    }
    cout<<"Decimal Number: "<<decNum<<endl;
}


int main(){
    binToDec(1011);
    return 0;
}