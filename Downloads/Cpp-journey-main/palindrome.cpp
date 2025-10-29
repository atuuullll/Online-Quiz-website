#include<iostream>
using namespace std;
bool isPalindrome(string str){
    int left=0;
    int right=str.length()-1;
    while(left<right){
        if(str[left]!=str[right]){
            return false;
        }
        left++;
        right--;
    }
    return true;
}
int main(){
    string s;
    cout<<"Enter a string: ";
    cin>>s;
    if(isPalindrome(s)){
        cout<<s<<" is a palindrome."<<endl;
    }
    else{
        cout<<s<<" is not a palindrome."<<endl;
    }
    return 0;
}