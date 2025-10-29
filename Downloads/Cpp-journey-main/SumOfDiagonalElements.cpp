#include <iostream>
using namespace std;

int diagonalSum(int matrix[10][10], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum = sum + matrix[i][i];
    }
    return sum;
}

int main() {
    int matrix[10][10], n;

    cout << "Enter size of square matrix (n x n): ";
    cin >> n;

    cout << "Enter elements of the matrix:\n";
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << "Element [" << i + 1 << "][" << j + 1 << "]: ";
            cin >> matrix[i][j];
        }
    }

    cout << "\nMatrix:\n";
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << matrix[i][j] << "\t";
        }
        cout << endl;
    }

    // Call function
    int sum = diagonalSum(matrix, n);

    cout << "\nSum of main diagonal elements = " << sum << endl;

    return 0;
}
