#include<iostream>
using namespace std;
int main(){
    //print the following pattern
    // 1 1 1 1 
    // 2 2 2 2 
    // 3 3 3 3 
    // 4 4 4 4
    // for(int i=1;i<=4;i++){
    //     for(int j=1;j<=4;j++){
    //         cout<<i<<" ";
    //     }
    //     cout<<endl;
    // }


    //print half pyramid
    //  *
    //  * *
    //  * * *
    //  * * * *
    // for(int i=1;i<=4;i++){
    //     for(int j=1;j<=i;j++){
    //         cout<<" *";
    //     }
    //     cout<<endl;
    // }


    //print inverted half pyramid
    //  * * * * *
    //  * * * *
    //  * * *
    //  * *
    //  *
    // int n=5;
    // for(int i=n;i>=1;i--){
    //     for(int j=1;j<=i;j++){
    //         cout<<" *";
    //     }
    //     cout<<endl;
    // }


    //print first half pyramid with numbers
    // 1 
    // 1 2 
    // 1 2 3 
    // 1 2 3 4 
    // cout<<"Enter the number: ";
    // int n;
    // cin>>n;
    // for(int i=1;i<=n;i++){
    //     for(int j=1;j<=i;j++){
    //         cout<<j<<" ";
    //     }
    //     cout<<endl;
    // }


    //print alphabet pattern
    // A 
    // B C 
    // D E F 
    // G H I J
    // int n=4;
    // char ch='A';
    // for(int i=1;i<=n;i++){
    //     for(int j=1;j<=i;j++){
    //         cout<<ch<<" ";
    //         ch++;   
    //     }
    //     cout<<endl;
    // }


    //print hollow rectangle
    //  * * * * *
    //  *       *
    //  *       *
    //  *       *
    //  * * * * *
    // int row,col;
    // cout<<"Enter the number of rows: ";
    // cin>>row;
    // cout<<"Enter the number of columns: ";
    // cin>>col;
    // for(int i=1;i<=row;i++){
    //     for(int j=1;j<=col;j++){
    //         if(i==1 || i==row || j==1 || j==col){
    //             cout<<" *";
    //         }
    //         else{
    //             cout<<"  ";
    //         }
    //     }
    //     cout<<endl;
    // }


    //print inverted and rotated half pyramid
    //        *
    //      * *
    //    * * *
    //  * * * *
    // for(int i=1;i<=4;i++){
    //     for(int j=1;j<=4-i;j++){
    //         cout<<"  ";
    //     }
    //     for(int k=1;k<=i;k++){
    //         cout<<" *";
    //     }
    //     cout<<endl;
    // }
    // return 0;


    // Floyd's triangle
    // 1 
    // 2 3 
    // 4 5 6 
    // 7 8 9 10
    // int n=4;
    // int num=1;
    // for(int i=1;i<=n;i++){
    //     for(int j=1;j<=i;j++){
    //         cout<<num++<<" ";
    //     }
    //     cout<<endl;
    // }


    //inverted and rotated half pyramid with stars
    //        *
    //      * *
    //    * * *
    //  * * * *
    // int n=4;
    // for(int i=1;i<=n;i++){
    //     for(int j=1;j<=n-i;j++){
    //         cout<<"  ";
    //     }
    //     for(int k=1;k<=i;k++){
    //         cout<<" *";
    //     }
    //     cout<<endl;
    // }
    // return 0;


    //Print diamond pattern
    //        *
    //      * * *
    //    * * * * *
    //  * * * * * * *
    //  * * * * * * *
    //    * * * * *
    //      * * *
    //        *
    // int n=4;
    // for(int i=1;i<=n;i++){
    //     for(int j=1;j<=n-i;j++){
    //         cout<<"  ";
    //     }
    //     for(int k=1;k<=2*i-1;k++){
    //         cout<<" *";
    //     }
    //     cout<<endl;
    // }
    // for(int i=n;i>=1;i--){
    //     for(int j=1;j<=n-i;j++){
    //         cout<<"  ";
    //     }
    //     for(int k=1;k<=2*i-1;k++){
    //         cout<<" *";
    //     }
    //     cout<<endl;
    // }
    // return 0;


    //print the following pattern
    // 1 2 3 4 5 
    // 2 3 4 5 
    // 3 4 5 
    // 4 5 
    // 5 
    // int n;
    // cout<<"Enter the number of rows: ";
    // cin>>n;
    // for(int i=1;i<=n;i++){
    //     for(int j=i;j<=n;j++){
    //         cout<<j<<" ";
    //     }
    //     cout<<endl;
    // }


    //print the following pattern
    // 1 
    // 2 2 
    // 3 3 3 
    // 4 4 4 4 
    // 5 5 5 5 5 
    // int n;
    // cout<<"Enter the number of rows: ";
    // cin>>n;
    // for(int i=1;i<=n;i++){
    //     for(int j=1;j<=i;j++){
    //         cout<<i<<" ";
    //     }
    //     cout<<endl;
    // }

    //print the following pattern
    // 5 4 3 2 1 
    // 5 4 3 2 
    // 5 4 3 
    // 5 4 
    // 5 
    // cout<<"Enter the number of rows: ";
    // int n;
    // cin>>n;
    // for(int i=1;i<=n;i++){
    //     for(int j=n;j>=i;j--){
    //         cout<<j<<" ";
    //     }
    //     cout<<endl;
    // }

    //print the following pattern
    // 1 2 3 4 5 
    // 1 2 3 4 
    // 1 2 3 
    // 1 2 
    // 1 
    // int n;
    // cout<<"Enter the number of rows: ";
    // cin>>n;
    // for(int i=1;i<=n;i++){
    //     for(int j=1;j<=n-i+1;j++){
    //         cout<<j<<" ";
    //     }
    //     cout<<endl;
    // }

    // int n;
    // cout<<"Enter the number of rows: ";
    // cin>>n;
    // for(int i=1;i<=n;i++){
    //     for(int j=1;j<=n-i+1;j++){
    //         cout<<j<<" ";
    //     }
    //     cout<<endl; 
    // }

    int n;
    cout<<"Enter the number of N: ";
    cin>>n;
    for(int i=1;i<=n;i++){
        for(int j=1;j<=i;j++){
            cout<<j<<" ";
        }
    }


}

