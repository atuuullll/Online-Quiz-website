#include<iostream>
using namespace std;
int main(){
    int i=1;
    while(i<=10){
        cout<<i<<endl;
        i++;
    }

    cout<<"New code"<<endl;
    cout<<"This is a Fibonacci series"<<endl;

    int a=0;
    int b=1;
    while(a<=10){
        cout<<a<<endl;
        int c=a+b;
        a=b;
        b=c;
    }

    cout<<"New code"<<endl;
    cout<<"This is a multiplication table of 7"<<endl;

    int n=7;
    int j=1;
    while(j<=10){
        cout<<n*j<<endl;
        j++;
    }

    cout<<"New code"<<endl;
    cout<<"This is a series of odd numbers"<<endl;

    int k=1;
    while(k<=10){
        cout<<k<<endl;
        k=k+2;
    }

    cout<<"New code"<<endl;
    cout<<"This is a series of even numbers"<<endl;

    int x=0;
    while(x<=10){
        cout<<x<<endl;
        x=x+2;
    }
}

