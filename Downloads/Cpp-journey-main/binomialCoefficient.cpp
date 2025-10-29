#include<iostream>
using namespace std;

int factorial(int n){
    int fact = 1;
    for(int i=1;i<=n; i++){
        fact = fact*i;
    }
    return fact;
}

//Formula: n!/(r!*(n-r)!)
int binCoeff(int n, int r){
    int val1= factorial(n);
    int val2= factorial(r);
    int val3= factorial(n-r);

    int result = val1/(val2*val3);
    cout<<"Binomial Coefficient of "<<n<<" and "<<r<<" is ";
    return result;
}

int main(){
    cout<<binCoeff(5,2)<<endl;
    return 0;
}