// #include<iostream>
// using namespace std;
// int main(){
//     int a = 10;
//     int *ptr = &a;
//     int **ptr3 = &ptr;
//     cout<<&ptr<<" = "<<ptr3<<endl;
//     return 0;
// }

#include<iostream>
using namespace std;    
void pointer(int *ptr){
    cout<<"Value of pointer is "<<*ptr<<endl;
}
int main(){
    int a=10;
    pointer(&a);
    return 0;
}