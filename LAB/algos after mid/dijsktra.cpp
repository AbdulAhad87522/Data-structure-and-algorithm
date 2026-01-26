#include <iostream>
using namespace std;

#define V 5
#define INF 9999

int minDistance(int dist[], bool visited[]) {
    int min = INF, index;

    for (int i = 0; i < V; i++) {
        if (!visited[i] && dist[i] < min) {
            min = dist[i];
            index = i;
        }
    }
    return index;
}

int main() {
    int graph[V][V] = {
        {0, 10, 0, 0, 5},
        {10, 0, 1, 0, 2},
        {0, 1, 0, 4, 0},
        {0, 0, 4, 0, 3},
        {5, 2, 0, 3, 0}
    };

    int dist[V];
    bool visited[V] = {false};

    for (int i = 0; i < V; i++)
        dist[i] = INF;

    dist[0] = 0;

    for (int count = 0; count < V - 1; count++) {
        int u = minDistance(dist, visited);
        visited[u] = true;

        for (int v = 0; v < V; v++) {
            if (!visited[v] && graph[u][v] != 0 &&
                dist[u] + graph[u][v] < dist[v]) {
                dist[v] = dist[u] + graph[u][v];
            }
        }
    }

    cout << "Vertex   Distance from Source\n";
    for (int i = 0; i < V; i++)
        cout << i << " \t\t " << dist[i] << endl;

    return 0;
}
