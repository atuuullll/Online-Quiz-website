#include<iostream>
using namespace std;
void fibonacci(int n){
    cout<<"Fibonacci series is: ";
    int a=0;
    cout<<a<<" ";
    int b=1;
    cout<<b<<" ";
    int k=a+b;
    while (k <= n) {
        cout << k << " ";
        a = b;
        b = k;
        k = a + b;
    }
    cout<<endl;
}
int main(){
    int a;
    cout<<"Enter a number: ";
    cin>>a;
    fibonacci(a);
    return 0;
}