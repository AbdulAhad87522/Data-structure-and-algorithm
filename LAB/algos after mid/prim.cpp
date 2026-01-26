#include <iostream>
using namespace std;

#define V 5
#define INF 9999

int graph[V][V] = {
    {0, 2, 0, 6, 0},
    {2, 0, 3, 8, 5},
    {0, 3, 0, 0, 7},
    {6, 8, 0, 0, 9},
    {0, 5, 7, 9, 0}
};

int main() {
    int visited[V] = {0};
    visited[0] = 1;

    int edges = 0;
    int minCost = 0;

    cout << "Edges in MST:\n";

    while (edges < V - 1) {
        int min = INF, x = 0, y = 0;

        for (int i = 0; i < V; i++) {
            if (visited[i]) {
                for (int j = 0; j < V; j++) {
                    if (!visited[j] && graph[i][j] != 0 && graph[i][j] < min) {
                        min = graph[i][j];
                        x = i;
                        y = j;
                    }
                }
            }
        }

        cout << x << " - " << y << " : " << graph[x][y] << endl;
        minCost += graph[x][y];
        visited[y] = 1;
        edges++;
    }

    cout << "Minimum Cost = " << minCost << endl;
    return 0;
}
