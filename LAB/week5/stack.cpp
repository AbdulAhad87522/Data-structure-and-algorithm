#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;

    Node(int val) {
        data = val;
        next = NULL;
    }
};

class Stack {
private:
    Node* top;

public:
    Stack() {
        top = NULL;
    }

    // Push element onto stack
    void push(int val) {
        Node* newnode = new Node(val);
        if (top == NULL) {
            top = newnode;
        } else {
            newnode->next = top;
            top = newnode;
        }
        cout << val << " pushed to stack\n";
    }

    // Pop element from stack
    void pop() {
        if (top == NULL) {
            cout << "Stack underflow: Cannot pop from empty stack\n";
            return;
        } else {
            Node* temp = top;
            int poppedValue = top->data;
            top = top->next;
            temp->next = NULL;
            delete temp;
            cout << poppedValue << " popped from stack\n";
        }
    }

    // Peek at top element without removing
    int peek() {
        if (top == NULL) {
            cout << "Stack is empty\n";
            return -1;
        }
        return top->data;
    }

    // Check if stack is empty
    bool isEmpty() {
        return top == NULL;
    }

    // Get the size of stack
    int getSize() {
        int count = 0;
        Node* temp = top;
        while (temp != NULL) {
            count++;
            temp = temp->next;
        }
        return count;
    }

    // Display stack elements (top to bottom)
    void display() {
        if (top == NULL) {
            cout << "Stack is empty\n";
            return;
        }
        
        Node* temp = top;
        cout << "Stack (top to bottom): ";
        while (temp != NULL) {
            cout << temp->data << " ";
            temp = temp->next;
        }
        cout << endl;
    }

    // Reverse the stack
    void reverseStack() {
        if (top == NULL) {
            cout << "Stack is empty\n";
            return;
        }
        
        Node* prev = NULL;
        Node* curr = top;
        Node* next = NULL;

        while (curr != NULL) {
            next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }
        top = prev;
        cout << "Stack reversed successfully!\n";
    }

    // Sort the stack (using bubble sort)
    void sortStack() {
        if (top == NULL) {
            cout << "Stack is empty\n";
            return;
        }

        Node* temp = top;
        Node* next1 = NULL;
        
        while (temp != NULL) {
            next1 = temp->next;
            while (next1 != NULL) {
                if (temp->data > next1->data) {
                    int tempdata = temp->data;
                    temp->data = next1->data;
                    next1->data = tempdata;
                }
                next1 = next1->next;
            }
            temp = temp->next;
        }
        cout << "Stack sorted successfully!\n";
    }

    // Clear the entire stack
    void clear() {
        while (top != NULL) {
            pop();
        }
        cout << "Stack cleared!\n";
    }

    // Destructor to free memory
    ~Stack() {
        clear();
    }
};

int main() {
    Stack s;
    int choice, value;

    do {
        cout << "\n=== Stack Menu ===" << endl;
        cout << "1. Push" << endl;
        cout << "2. Pop" << endl;
        cout << "3. Peek" << endl;
        cout << "4. Display" << endl;
        cout << "5. Check Empty" << endl;
        cout << "6. Get Size" << endl;
        cout << "7. Reverse Stack" << endl;
        cout << "8. Sort Stack" << endl;
        cout << "9. Clear Stack" << endl;
        cout << "0. Exit" << endl;
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter value to push: ";
                cin >> value;
                s.push(value);
                break;

            case 2:
                s.pop();
                break;

            case 3:
                value = s.peek();
                if (value != -1) {
                    cout << "Top element: " << value << endl;
                }
                break;

            case 4:
                s.display();
                break;

            case 5:
                if (s.isEmpty()) {
                    cout << "Stack is empty" << endl;
                } else {
                    cout << "Stack is not empty" << endl;
                }
                break;

            case 6:
                cout << "Stack size: " << s.getSize() << endl;
                break;

            case 7:
                s.reverseStack();
                break;

            case 8:
                s.sortStack();
                break;

            case 9:
                s.clear();
                break;

            case 0:
                cout << "Exiting program..." << endl;
                break;

            default:
                cout << "Invalid choice! Please try again." << endl;
        }
    } while (choice != 0);

    return 0;
}