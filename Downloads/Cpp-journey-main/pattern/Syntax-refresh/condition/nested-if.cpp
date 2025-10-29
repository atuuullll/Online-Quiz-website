#include<iostream>
using namespace std;
int main(){
    int i;
    cout<<"Enter a number: ";
    cin>>i;
    if(i%2==0){
        cout<<i<<" is even"<<endl;
        if(i%4==0){
            cout<<i<<" is divisible by 4"<<endl;
        }
        if(i%3==0){
            cout<<i<<" is divisible by 3"<<endl;
        }
        if(i%5==0){
            cout<<i<<" is divisible by 5"<<endl;
        }
    }
    if(i%2!=0){
        cout<<i<<" is odd"<<endl;
        if(i%3==0){
            cout<<i<<" is divisible by 3"<<endl;
        }
        if(i%5==0){
            cout<<i<<" is divisible by 5"<<endl;
        }
    }
}