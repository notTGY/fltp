#include <stdio.h>
#include <stdbool.h>
#include <string.h>

int main() {
    int A, N;
    scanf("%d %d", &A, &N);
    int trans[60][26][60];
    int count[60][26];
    memset(count, 0, sizeof(count));
    int M;
    scanf("%d", &M);
    for (int i = 0; i < M; i++) {
        int a, b;
        char c;
        scanf("%d %d %c", &a, &b, &c);
        int idx = c - 'a';
        trans[a][idx][count[a][idx]++] = b;
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
        current[0] = true;
        for (char *p = str; *p; p++) {
            int idx = *p - 'a';
            bool next_set[60] = {false};
            for (int j = 0; j < N; j++) {
                if (current[j]) {
                    for (int k = 0; k < count[j][idx]; k++) {
                        next_set[trans[j][idx][k]] = true;
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
    printf("\n");
    return 0;
}