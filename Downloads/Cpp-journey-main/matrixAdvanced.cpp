#include<iostream>
using namespace std;
void inputMatrix(int matrix[10][10], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << "Element [" << i + 1 << "][" << j + 1 << "]: ";
            cin >> matrix[i][j];
        }
    }
}
void displayMatrix(int matrix[10][10], int n) {
    cout << "\nMatrix:\n";
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << matrix[i][j] << "\t";
        }
        cout << endl;
    }
}

//sum of diagonal elements
int sumDiagonal(int matrix[10][10], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += matrix[i][i];
    }
    return sum;
}
//sum of upper triangular matrix
int sumUpperTriangular(int matrix[10][10], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            sum += matrix[i][j];
        }
    }
    return sum;
}

//sum of lower triangular matrix
int sumLowerTriangular(int matrix[10][10], int n) {
    int sum = 0;
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            sum += matrix[i][j];
        }
    }
    return sum;
}

int main() {
    int matrix[10][10], n;
    cout << "Enter size of square matrix (n x n): ";
    cin >> n;
    cout << "Enter elements of the matrix:\n";
    inputMatrix(matrix, n);
    displayMatrix(matrix, n);
    int sum = sumDiagonal(matrix, n);
    cout << "\nSum of main diagonal elements = " << sum << endl;
    int upperSum = sumUpperTriangular(matrix, n);
    cout << "Sum of upper triangular elements = " << upperSum << endl;
    int lowerSum = sumLowerTriangular(matrix, n);
    cout << "Sum of lower triangular elements = " << lowerSum << endl;

    return 0;
}