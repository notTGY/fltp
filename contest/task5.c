#include <stdio.h>
#include <stdbool.h>
#include <string.h>

int main() {
    int A, N;
    scanf("%d %d", &A, &N);
    int trans[60][26][60];
    int count_trans[60][26];
    memset(count_trans, 0, sizeof(count_trans));
    int eps_trans[60][60];
    int count_eps[60];
    memset(count_eps, 0, sizeof(count_eps));
    int M;
    scanf("%d", &M);
    for (int i = 0; i < M; i++) {
        int a, b;
        char buf[10];
        scanf("%d %d %s", &a, &b, buf);
        if (strcmp(buf, "E") == 0) {
            eps_trans[a][count_eps[a]++] = b;
        } else {
            int idx = buf[0] - 'a';
            trans[a][idx][count_trans[a][idx]++] = b;
        }
    }
    bool eps_reach[60][60];
    memset(eps_reach, 0, sizeof(eps_reach));
    for (int i = 0; i < N; i++) {
        eps_reach[i][i] = true;
        for (int j = 0; j < count_eps[i]; j++) {
            eps_reach[i][eps_trans[i][j]] = true;
        }
    }
    for (int k = 0; k < N; k++) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (eps_reach[i][k] && eps_reach[k][j]) {
                    eps_reach[i][j] = true;
                }
            }
        }
    }
    bool terminal[60] = {false};
    int T;
    scanf("%d", &T);
    for (int i = 0; i < T; i++) {
        int x;
        scanf("%d", &x);
        terminal[x] = true;
    }
    int K;
    scanf("%d", &K);
    for (int i = 0; i < K; i++) {
        char str[8193];
        scanf("%s", str);
        bool current[60] = {false};
        for (int j = 0; j < N; j++) {
            if (eps_reach[0][j]) {
                current[j] = true;
            }
        }
        for (char *p = str; *p; p++) {
            int idx = *p - 'a';
            bool next_set[60] = {false};
            for (int j = 0; j < N; j++) {
                if (current[j]) {
                    for (int k = 0; k < count_trans[j][idx]; k++) {
                        int to = trans[j][idx][k];
                        for (int l = 0; l < N; l++) {
                            if (eps_reach[to][l]) {
                                next_set[l] = true;
                            }
                        }
                    }
                }
            }
            memcpy(current, next_set, sizeof(current));
        }
        bool accept = false;
        for (int j = 0; j < N; j++) {
            if (current[j] && terminal[j]) {
                accept = true;
                break;
            }
        }
        if (i > 0) printf(" ");
        printf("%d", accept ? 1 : 0);
    }
    printf("\n");
    return 0;
}