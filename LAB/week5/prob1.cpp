#include <iostream>
using namespace std;

class Node{
public:
    int data;
    Node* next;

    Node(int val){
        data = val;
        next = NULL;
    }
};

class list{
    Node* head;
    Node* tail;
public:
    list(){
        head = tail = NULL;
    }

    void push_front(int val){
        Node* newnode = new Node(val);
        if(head == NULL)
            {
                head = tail = newnode;
                return;
            }
        else{
            newnode->next = head;
            head = newnode;

        }
    }

    void push_back(int val)
    {
        Node* newnode = new Node(val);
        if(head == NULL)
        {
            head = tail = newnode;
        }
        else
        {
            tail->next = newnode;
            tail  = newnode;    
        }
    }

    void pop_front()
    {
        if(head == NULL)
        {
            cout<<"LIst is empty";
            return;
        }
        else
        {
            Node* temp  = head;
            head = head->next;
            temp->next  = NULL;
            delete temp;
        }
    }

    void pop_back()
    {
        if(head == NULL)
        {
            cout<<"empty list";
            return;
        }
        else{
            Node* temp = head;
            while(temp->next->next != NULL)
            {
                temp = temp->next;
            }
            temp->next = NULL;
            delete tail;
            tail = temp;
        }
    }

    void insert(int val, int pos)
    {
        if(pos<0)
        {
            return;
        }

        else if(pos == 0)
        {
            push_front(val);
        }

        else{
            Node* temp = head;
            for(int i = 0 ; i < pos - 1 ; i++)
            {
                if(temp == NULL)
                {
                    cout<<"invalid pos\n";
                    return;
                }
                temp = temp->next;
            }
            Node* newnode = new Node(val);
            newnode->next = temp->next;
            temp->next = newnode;
        }

    }


    void del(int val)
    {
        while (head != NULL && head->data == val)
        {
            Node* temp = head;
            head = head->next;
            delete temp;
        }

        Node* temp = head;
        while (temp != NULL && temp->next != NULL)
        {
            if (temp->next->data == val)
            {
                Node* toDelete = temp->next;
                temp->next = temp->next->next;
                delete toDelete;
            }
            else
            {
                temp = temp->next;
            }
        }
    }


    int search(int val)
    {
            Node* temp = head;
            int idx = 0;    
            while(temp != NULL)
            {
                if(temp->data == val)
                {
                    return idx;
                }
                temp = temp->next;
                idx++;
            }   
            return -1;
    }

    void print(){
        Node* temp = head;
        while(temp != NULL)
        {
            cout<<temp->data<<" ";
            temp = temp->next;
        }
    }
    
    void reverselist()
    {
        if(head == NULL)
        {
            cout<<"List is empty"<<endl;
            return;
        }
        Node* prev = NULL;
        Node* curr = head;
        Node* next = NULL;

        while (curr != NULL)
        {
            next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;    
        }
      
        head = prev;
    }

    void sortlist()
    {
        Node* temp = head;
        Node* next1 = NULL;
        if(head == NULL)
        {
            cout<<"empty list";
            return;
        }
        while(temp != NULL)
        {
            next1 = temp->next;
            while(next1 != NULL)
            {
                if(temp->data > next1->data)
                {
                    int tempdata= 0;
                    tempdata = temp->data;
                    temp->data = next1->data;
                    next1->data = tempdata;
                }
                next1 = next1->next;
            }
            temp = temp->next;
        }
    }

    // void removeduplicates()
    // {
    //     if(head == NULL)
    //     {
    //         cout<<"list is empty";
    //         return;
    //     }

    //     Node* curr = head;
    //     Node* prev = NULL;
    //     while(curr != NULL )
    //     {
    //         if(curr->next != NULL && curr->next == curr->next->data)
    //         {
    //             int val = curr->data;
    //             while(curr != NULL && curr->data = val)
    //             {
    //                 curr = curr->next;
    //             }
    //             if(prev != NULL)
    //             {
    //                 prev->next = curr;
    //             }
    //             else{
    //                 head = curr;
    //             }
    //         }
    //         else{
    //                 prev= curr;
    //                 curr = curr->next;
    //             }
    //     }
    // }
    void removeAllDuplicates()
{
    if (head == NULL)
    {
        cout << "List is empty" << endl;
        return;
    }

    Node* dummy = new Node(0); // temporary node before head
    dummy->next = head;
    Node* prev = dummy;
    Node* curr = head;

    while (curr != NULL)
    {
        bool duplicate = false;

        // Check if current value has duplicates
        while (curr->next != NULL && curr->data == curr->next->data)
        {
            duplicate = true;
            Node* temp = curr->next;
            curr->next = curr->next->next;
            delete temp;
        }

        if (duplicate)
        {
            // Remove the first occurrence too
            Node* temp = curr;
            curr = curr->next;
            delete temp;
            prev->next = curr;
        }
        else
        {
            // Move normally if no duplicate
            prev = curr;
            curr = curr->next;
        }
    }

    head = dummy->next;
    delete dummy;

    cout << "All duplicates removed successfully!" << endl;
}

};

int main() {
    list ll;
    ll.push_front(2);
    ll.push_front(3);
    ll.push_front(3);
    ll.push_back(7);
    // ll.pop_front();
    // ll.pop_back();
    // ll.insert(9,3);
    // ll.del(3);
    // cout<<ll.search(7);
    cout<<" ";
    ll.print();
    ll.reverselist();
    cout<<endl;
    ll.print();
    cout<<endl;
    ll.sortlist();
    ll.print();

    return 0;
}