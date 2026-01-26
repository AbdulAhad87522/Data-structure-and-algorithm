#include <iostream>
using namespace std;

#define V 4   // number of vertices

int graph[V][V] = {
    {0, 1, 1, 0},
    {1, 0, 0, 1},
    {1, 0, 0, 0},
    {0, 1, 0, 0}
};

bool visited[V];

void DFS(int node) {
    cout << node << " ";
    visited[node] = true;

    for (int i = 0; i < V; i++) {
        if (graph[node][i] == 1 && !visited[i]) {
            DFS(i);
        }
    }
}

int main() {
    for (int i = 0; i < V; i++)
        visited[i] = false;

    cout << "DFS Traversal: ";
    DFS(0);

    return 0;
}
