#include <iostream>
using namespace std;

#define V 4
#define E 5

int parent[V];

int find(int i) {
    while (parent[i] != i)
        i = parent[i];
    return i;
}

void unionSet(int a, int b) {
    parent[find(a)] = find(b);
}

int main() {
    int edges[E][3] = {
        {0, 1, 10},
        {0, 2, 6},
        {0, 3, 5},
        {1, 3, 15},
        {2, 3, 4}
    };

    for (int i = 0; i < V; i++)
        parent[i] = i;

    // Simple bubble sort by weight
    for (int i = 0; i < E - 1; i++) {
        for (int j = 0; j < E - i - 1; j++) {
            if (edges[j][2] > edges[j + 1][2]) {
                for (int k = 0; k < 3; k++)
                    swap(edges[j][k], edges[j + 1][k]);
            }
        }
    }

    int minCost = 0;
    cout << "Edges in MST:\n";

    for (int i = 0; i < E; i++) {
        int u = edges[i][0];
        int v = edges[i][1];
        int w = edges[i][2];

        if (find(u) != find(v)) {
            cout << u << " - " << v << " : " << w << endl;
            minCost += w;
            unionSet(u, v);
        }
    }

    cout << "Minimum Cost = " << minCost << endl;
    return 0;
}
