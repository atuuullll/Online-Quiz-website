#include<iostream>
using namespace std;
int main(){
    // int arr[5]={2,4,6,8,10};
    // for(int i=0;i<5;i++){
    //     cout<<arr[i]<<endl;
    // }


    // int n;
    // cout<<"Enter the size of array: ";
    // cin>>n;
    // int arr[n]={2,4,6,8,10};
    // for(int i=0;i<n;i++){
    //     cout<<arr[i]<<endl;
    // }
    // return 0;

    // int n;
    // cout<<"Enter the size of array: ";
    // cin>>n;
    // int arr[n];
    // for(int i=0;i<n;i++){
    //     cin>>arr[i];
    // }
    // cout<<"The array elements are: "<<endl;
    // for(int i=0;i<n;i++){
    //     cout<<arr[i]<<endl;
    // }
    // return 0;

    // int arr[5]={2,4,6,8,10};
    // cout<<"The array elements are: "<<endl;
    // int i;
    // for(i=0;i<5;i++){
    //     cout<<arr[i]<<endl;
    // }
    // cout<<"The size of array is: "<<sizeof(arr)<<endl;
    // cout<<"The number of elements in array is: "<<sizeof(arr)/sizeof(arr[0])<<endl;
    // return 0;

    int arr[] = {2, 4, 8, 12, 16};
    cout<<"The array elements are: "<<endl;
    int i;
    for(i=0;i<sizeof(arr)/sizeof(arr[0]);i++){
        cout<<arr[i]<<" ";
    }
    cout<<endl;
    cout<<"Fourth element: ";
    cout << arr[3] << " ";
    cout<<endl;
    cout<<"First element: ";
    cout << arr[0];
    cout<<endl;
    cout<<"Last element: ";
    cout << arr[sizeof(arr)/sizeof(arr[0]) - 1];
    cout<<endl;
    
    return 0;
}