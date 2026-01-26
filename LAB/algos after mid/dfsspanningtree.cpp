#include <iostream>
using namespace std;

#define V 4

int graph[V][V] = {
    {0, 1, 1, 0},
    {1, 0, 0, 1},
    {1, 0, 0, 0},
    {0, 1, 0, 0}
};

bool visited[V];

void DFS_SpanningTree(int u) {
    visited[u] = true;

    for (int v = 0; v < V; v++) {
        if (graph[u][v] == 1 && !visited[v]) {
            cout << u << " - " << v << endl;   // edge of spanning tree
            DFS_SpanningTree(v);
        }
    }
}

int main() {
    for (int i = 0; i < V; i++)
        visited[i] = false;

    cout << "Spanning Tree Edges:\n";
    DFS_SpanningTree(0);

    return 0;
}
