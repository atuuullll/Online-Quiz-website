#include<iostream>
using namespace std;
void oddEven(int n){
    if(n%2==0){
        cout<<n<<" is an even number."<<endl;
    }
    else{
        cout<<n<<" is an odd number."<<endl;
    }
}
int main(){
    int a;
    cout<<"Enter a number: ";
    cin>>a;
    oddEven(a);
    return 0;
}