#include <stdio.h>
#include <stdbool.h>
#include <string.h>

int main() {
    int A, N;
    scanf("%d %d", &A, &N);
    int trans[60][26];
    memset(trans, -1, sizeof(trans));
    int M;
    scanf("%d", &M);
    for (int i = 0; i < M; i++) {
        int a, b;
        char c;
        scanf("%d %d %c", &a, &b, &c);
        int idx = c - 'a';
        trans[a][idx] = b;
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
        int state = 0;
        bool accept = true;
        for (char *p = str; *p; p++) {
            int idx = *p - 'a';
            if (idx < 0 || idx >= A || trans[state][idx] == -1) {
                accept = false;
                break;
            }
            state = trans[state][idx];
        }
        int result = (accept && terminal[state]) ? 1 : 0;
        if (i > 0) printf(" ");
        printf("%d", result);
    }
    printf("\n");
    return 0;
}