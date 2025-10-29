#include <iostream>
#include <vector>
using namespace std;

class Node{
    public:
      int data;
      Node* left;
      Node* right;
    Node(int val)
    {
        data = val;
        left = right = NULL;
    }

};
    Node* insert(Node* root, int data){
        if(root == NULL){
            return new Node(data);
        }
        else{
            if(data < root->data)
            {
                root->left = insert(root->left, data);
            }
            else{
                root->right = insert(root->right, data);
            }
        }
        return root;
    }

    Node* buildBST(vector<int> arr){
        Node* root = NULL;
        for(int data : arr)
        {
            root = insert(root,data);
        }
        return root;
    }

    void inorder(Node* root)
    {
        if(root == NULL)
        {
            return;
        }
        inorder(root->left);
        cout<<root-> data<<",";
        inorder(root->right);
    }

    bool search(Node* root,int key)
    {
        if(root == NULL)
        {
            return false;
        }
        else
        {
            if(root->data == key)
            {
                return true;
            }
            else{
                if(root->data > key)
                {
                    return search(root->left, key);
                }
                    return search(root->right, key);
            }
        }
    }

       Node* getIS(Node* root)
    {
        while (root !=NULL && root->left != NULL)
        {
            root = root->left;
        }
        return root;
    }

    Node* delNOde(Node* root, int key)
    {
        if(root == NULL)
        {
            return root;
        }

        if(key < root->data)
        {
            root->left = delNOde(root->left, key);
        }

        else if(key > root->data)
        {
            root->right = delNOde(root->right, key);
        }

        else
        {
            if(root->left == NULL && root->right) //  mere logic
            // if(root->left == NULL )

            {
                Node* temp = root->right;
                delete root;
                return temp;
            }
            else if(root->left == NULL || root->right == NULL)  // mere logic
            // else if(root->right == NULL)

            {
                // Node* temp = root->left;
                // root->right = temp->right;
                // delete root;  //mere logic
                Node* temp = root->left;
                delete root;
                return temp;
            }
            else{
                Node* IS = getIS(root->right);
                root->data = IS->data;
                root->right = delNOde(root->right, IS->data);
            }
        }
        // return root;
    }

 

int main()
{
    vector<int> arr = {3,2,1,5,6,4};
    Node* root =  buildBST(arr);
    inorder(root);
    cout<<endl;
    if(search(root,2))
    {
        cout<<"true";
    }
    else{
        cout<<"false";
    }
    delNOde(root,1);
    cout<<endl;
    inorder(root);

    return 0 ;
}