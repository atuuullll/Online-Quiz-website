#include<iostream>
using namespace std;
void longModifierDemo(){
    cout<<"size of int: "<<sizeof(int)<<" bytes"<<endl;
    cout<<"Long size demo:"<<endl;
    cout<<"size of long int: "<<sizeof(long int)<<" bytes"<<endl;
    cout<<"Size of long: "<<sizeof(long)<<" bytes"<<endl;
}
void shortModifierDemo(){
    cout<<"Short size demo:"<<endl;
    cout<<"size of short int: "<<sizeof(short int)<<" bytes"<<endl;
    cout<<"Size of short: "<<sizeof(short)<<" bytes"<<endl;
}
void signedModifierDemo(){
    cout<<"Signed size demo:"<<endl;
    cout<<"size of signed int: "<<sizeof(signed int)<<" bytes"<<endl;
    cout<<"Size of signed: "<<sizeof(signed)<<" bytes"<<endl;
}
void unsignedModifierDemo(){
    cout<<"Unsigned size demo:"<<endl;
    cout<<"size of unsigned int: "<<sizeof(unsigned int)<<" bytes"<<endl;
    cout<<"Size of unsigned: "<<sizeof(unsigned)<<" bytes"<<endl;
}
void longLongModifierDemo(){
    cout<<"Long Long size demo:"<<endl;
    cout<<"size of long long int: "<<sizeof(long long int)<<" bytes"<<endl;
    cout<<"Size of long long: "<<sizeof(long long)<<" bytes"<<endl;
}
int main(){
    longModifierDemo();
    shortModifierDemo();
    signedModifierDemo();
    unsignedModifierDemo();
    longLongModifierDemo();
    return 0;
}