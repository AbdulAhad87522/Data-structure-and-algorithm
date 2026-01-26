#include <iostream>
using namespace std;

#define TABLE_SIZE 9
#define EMPTY -1

class HashTable {
    int table[TABLE_SIZE];

public:
    HashTable() {
        for (int i = 0; i < TABLE_SIZE; i++)
            table[i] = EMPTY;
    }

    // First hash function
    int h1(int key) {
        return key % TABLE_SIZE;
    }

    // Second hash function
    int h2(int key) {
        return 8 - (key % 8);
    }

    // Insert using double hashing
    void insert(int key) {
        int index = h1(key);

        // Collision detected
        if (table[index] != EMPTY) {
            cout << "Collision detected for key " << key << " at index " << index << endl;

            // int st   ep = h2(key);
            int i = 1;

            while (table[index] != EMPTY) {
                index = (h1(key) + i * h2(key)) % TABLE_SIZE;
                i++;
            }
        }

        table[index] = key;
    }

    void display() {
        cout << "\nHash Table:\n";
        for (int i = 0; i < TABLE_SIZE; i++) {
            cout << i << " -> ";
            if (table[i] == EMPTY)
                cout << "EMPTY";
            else
                cout << table[i];
            cout << endl;
        }
    }
};

int main() {
    HashTable ht;

    ht.insert(10);
    ht.insert(20);
    ht.insert(30);
    ht.insert(17);  // collision example
    ht.insert(17);
    ht.insert(17);
    ht.insert(17);

    ht.display();

    return 0;
}
