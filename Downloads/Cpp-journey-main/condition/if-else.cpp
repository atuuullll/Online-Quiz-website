#include<iostream>
using namespace std;
int main(){
    int age;
    cout<<"Enter your age: ";
    cin>>age;
    if(age<18){
        cout<<"You are a minor"<<endl;
    }
    else{
        cout<<"You are an adult"<<endl;
    }

    cout<<endl;
    cout<<"New code"<<endl;

    int i;
    cout<<"Enter a number: ";
    cin>>i;
    if(i%2==0){
        cout<<i<<" is even"<<endl;
        cout<<i<<" is also divisible by 2"<<endl;
        cout<<i<<" is not odd"<<endl;
        cout<<i<<" is not prime"<<endl;
    }
    else{
        cout<<i<<" is odd"<<endl;
        cout<<i<<" is not divisible by 2"<<endl;
        cout<<i<<" is not even"<<endl;
        cout<<i<<" might be prime"<<endl;
    }
}
