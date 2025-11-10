#include<iostream>
#include<string>
#include <iomanip>
#include <conio.h>

using namespace std;

#define KEY_UP    72
#define KEY_DOWN  80
#define KEY_LEFT  75
#define KEY_RIGHT 77
#define KEY_ENTER 13

class Node{
public:
    string val;
    Node* up;
    Node* down;
    Node* left;
    Node* right;
    Node(){
        up = down = left = right = NULL;
        val = "";
    }
    Node(string value){
        up = down = left = right = NULL;
        val = value;
    }
};

class Sheet{
    int rows;
    int cols;

    int r;
    int c;

    Node* topLeft;
    Node* current;

    void divider() {
        cout << "------+";
        for (int j = 0; j < cols; ++j) {
            cout << "----------+";
        }
        cout << "\n";
    }
public:
    Sheet(int row,int col): rows(row), cols(col), r(0),c(0){
        topLeft = new Node();
        Node* itr = topLeft;
        for(int j=1;j<cols;j++){
            itr->right = new Node();
            itr->right->left = itr;
            itr = itr->right;
        }

        Node* aboveRowFirst = topLeft;

        for(int i=1;i<rows;i++){
            Node* newRowFirst = new Node();
            aboveRowFirst->down = newRowFirst;
            newRowFirst->up = aboveRowFirst;

            Node* aboveNode = aboveRowFirst;
            Node* currentNode = newRowFirst;

            for(int j=1;j<cols;j++){
                aboveNode = aboveNode->right;

                currentNode->right = new Node();
                currentNode->right->left = currentNode;

                currentNode->right->up = aboveNode;
                aboveNode->down = currentNode->right;

                currentNode = currentNode->right;
            }

            aboveRowFirst = newRowFirst;
        }

        current = topLeft;
    }
    ~Sheet(){
        Node* rowStart = topLeft;
        while(rowStart != NULL){
            Node* currentNode = rowStart;
            Node* nextRowStart = rowStart->down; // Save pointer to next row

            while(currentNode != NULL){
                Node* nextNode = currentNode->right; // Save pointer to next node
                delete currentNode;                  // Delete current node
                currentNode = nextNode;
            }
            rowStart = nextRowStart;
        }
    }
    void moveUp(){
        if(current->up != NULL){
            current = current->up;
            r --;
        }
    }
    void moveDown(){
        if(current->down != NULL){
            current = current->down;
            r ++;
        }
    }
    void moveRight(){
        if(current->right != NULL){
            current = current->right;
            c ++;
        }
    }
    void moveLeft(){
        if(current->left != NULL){
            current = current->left;
            c --;
        }
    }
    void editCell(string content){
        current->val = content;
    }
    void clear(){
        Node* rowFirst = topLeft;
        while(rowFirst != NULL){
            Node* currentNode = rowFirst;
            while(currentNode != NULL){
                currentNode->val = "";
                currentNode = currentNode->right;
            }
            rowFirst = rowFirst->down;
        }
    }

    string getCurrentCell(){
        return (char)('A' + c) + to_string(r+1);
    }

    void displaySheet() {
        system("cls");

        cout << "========= C++ CONSOLE SPREADSHEET =========\n";
        cout << "Active Cell: " << setw(4) << left << getCurrentCell() 
                  << " | Value: " << current->val << "\n\n";

        cout << "      |";
        for (int j = 0; j < cols; ++j) {
            cout << "    " << (char)('A' + j) << "     |";
        }
        cout << "\n";
        divider();

        Node* rowStart = topLeft;
        for (int i = 0; i < rows; ++i) {
            cout << setw(5) << (i + 1) << " |";
            
            Node* currentNode = rowStart;
            for (int j = 0; j < cols; ++j) {
                bool isActive = (currentNode == current);
                
                string displayVal = "";
                if (currentNode) {
                    displayVal = currentNode->val;
                    if (displayVal.length() > 8) {
                        displayVal = displayVal.substr(0, 8) + "..";
                    }
                }

                cout << (isActive ? "[" : " ");
                cout << setw(8) << left << displayVal;
                cout << (isActive ? "]" : " ");
                cout << "|";
                
                if (currentNode) currentNode = currentNode->right;
            }
            cout << "\n";
            divider();
            
            if (rowStart) rowStart = rowStart->down;
        }

        cout << "\nControls: Arrow Keys (Move) | Enter (Edit) | 'c' (Clear All) | 'q' (Quit)\n";
    }
};

int main(){
    Sheet s(15,15);
    bool ON = true;
    string input;
    while(ON){
        s.displaySheet();

        int ch = _getch();
        
        if (ch == 224) { 
            ch = _getch();
            if (ch == KEY_UP) {
                s.moveUp();
            } else if (ch == KEY_DOWN) {
                s.moveDown();
            } else if (ch == KEY_LEFT) {
                s.moveLeft();
            } else if (ch == KEY_RIGHT) {
                s.moveRight();
            }
        } else {
            if (ch == KEY_ENTER) {
                cout<<"Enter value to edit: ";
                getline(cin,input);
                s.editCell(input);
            } else if (ch == 'c' || ch == 'C') {
                s.clear();
            } else if (ch == 'q' || ch == 'Q') {
                ON = false;
            }
        }
    }
    cout<<"Made by: Hussain Shahbaz"<<endl;
    return 0;
}