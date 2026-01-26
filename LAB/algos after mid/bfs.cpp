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

void BFS(int start) {
    int queue[V];
    int front = 0, rear = 0;

    visited[start] = true;
    queue[rear++] = start;

    while (front < rear) {
        int node = queue[front++];
        cout << node << " ";

        for (int i = 0; i < V; i++) {
            if (graph[node][i] == 1 && !visited[i]) {
                visited[i] = true;
                queue[rear++] = i;
            }
        }
    }
}

int main() {
    for (int i = 0; i < V; i++)
        visited[i] = false;

    cout << "BFS Traversal: ";
    BFS(0);

    return 0;
}
