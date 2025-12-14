#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    int *states;
    int size;
} Group;

int main() {
    int n, t, l;
    scanf("%d %d %d", &n, &t, &l);
    bool terminal[1000] = {false};
    for (int i = 0; i < t; i++) {
        int x;
        scanf("%d", &x);
        terminal[x] = true;
    }
    int trans[1000][26];
    memset(trans, -1, sizeof(trans));
    for (int i = 0; i < n * l; i++) {
        int s1, s2;
        char b;
        scanf("%d %c %d", &s1, &b, &s2);
        int idx = b - 'a';
        trans[s1][idx] = s2;
    }
    int max_groups = 1000;
    Group *P = malloc(sizeof(Group) * max_groups);
    int P_count = 0;
    int *F = malloc(sizeof(int) * n);
    int F_count = 0;
    int *Q_F = malloc(sizeof(int) * n);
    int Q_F_count = 0;
    for (int i = 0; i < n; i++) {
        if (terminal[i]) {
            F[F_count++] = i;
        } else {
            Q_F[Q_F_count++] = i;
        }
    }
    if (F_count > 0) {
        P[P_count].states = F;
        P[P_count].size = F_count;
        P_count++;
    }
    if (Q_F_count > 0) {
        P[P_count].states = Q_F;
        P[P_count].size = Q_F_count;
        P_count++;
    }
    int *group_id = malloc(sizeof(int) * n);
    for (int g = 0; g < P_count; g++) {
        for (int i = 0; i < P[g].size; i++) {
            group_id[P[g].states[i]] = g;
        }
    }
    int max_wl = 1000;
    int *worklist = malloc(sizeof(int) * max_wl);
    int wl_head = 0, wl_tail = 0;
    for (int g = 0; g < P_count; g++) {
        worklist[wl_tail++] = g;
    }
    bool *in_A = malloc(sizeof(bool) * n);
    bool *in_X = malloc(sizeof(bool) * n);
    while (wl_head < wl_tail) {
        int a_idx = worklist[wl_head++];
        if (a_idx == -1) continue; // removed
        memset(in_A, 0, sizeof(bool) * n);
        for (int i = 0; i < P[a_idx].size; i++) {
            in_A[P[a_idx].states[i]] = true;
        }
        for (int k = 0; k < l; k++) {
            memset(in_X, 0, sizeof(bool) * n);
            for (int s = 0; s < n; s++) {
                if (in_A[trans[s][k]]) {
                    in_X[s] = true;
                }
            }
            for (int y = 0; y < P_count; y++) {
                if (P[y].size == 0) continue;
                int *Y = P[y].states;
                int Y_size = P[y].size;
                int *Y1 = malloc(sizeof(int) * Y_size);
                int Y1_count = 0;
                int *Y2 = malloc(sizeof(int) * Y_size);
                int Y2_count = 0;
                for (int i = 0; i < Y_size; i++) {
                    int s = Y[i];
                    if (in_X[s]) {
                        Y1[Y1_count++] = s;
                    } else {
                        Y2[Y2_count++] = s;
                    }
                }
                if (Y1_count > 0 && Y2_count > 0) {
                    free(P[y].states);
                    P[y].states = Y1;
                    P[y].size = Y1_count;
                    if (P_count == max_groups) {
                        max_groups *= 2;
                        P = realloc(P, sizeof(Group) * max_groups);
                    }
                    P[P_count].states = Y2;
                    P[P_count].size = Y2_count;
                    int new_g = P_count;
                    P_count++;
                    for (int i = 0; i < Y1_count; i++) {
                        group_id[Y1[i]] = y;
                    }
                    for (int i = 0; i < Y2_count; i++) {
                        group_id[Y2[i]] = new_g;
                    }
                    bool was_in_wl = false;
                    for (int w = wl_head; w < wl_tail; w++) {
                        if (worklist[w] == y) {
                            worklist[w] = -1;
                            was_in_wl = true;
                            break;
                        }
                    }
                    if (was_in_wl) {
                        if (wl_tail + 2 > max_wl) {
                            max_wl *= 2;
                            worklist = realloc(worklist, sizeof(int) * max_wl);
                        }
                        worklist[wl_tail++] = y;
                        worklist[wl_tail++] = new_g;
                    } else {
                        if (wl_tail + 1 > max_wl) {
                            max_wl *= 2;
                            worklist = realloc(worklist, sizeof(int) * max_wl);
                        }
                        if (Y1_count <= Y2_count) {
                            worklist[wl_tail++] = y;
                        } else {
                            worklist[wl_tail++] = new_g;
                        }
                    }
                } else {
                    free(Y1);
                    free(Y2);
                }
            }
        }
    }
    printf("%d\n", P_count);
    for (int g = 0; g < P_count; g++) {
        free(P[g].states);
    }
    free(P);
    free(group_id);
    free(worklist);
    free(in_A);
    free(in_X);
    return 0;
}