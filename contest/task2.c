#include <stdio.h>
#include <stdlib.h>

int sym_to_idx(char c) {
    if (c == 'A') return 0;
    if (c == 'C') return 1;
    if (c == 'G') return 2;
    if (c == 'T') return 3;
    return -1;
}

int main() {
    int n;
    scanf("%d", &n);
    int next_state[101][4];
    char out_symbol[101][4];
    char in_symbol[101][4];
    int dec_next[101][4];
    for (int i = 0; i < 4 * n; i++) {
        int st, nst;
        char sym_in, sym_out;
        scanf("%d %c %d %c", &st, &sym_in, &nst, &sym_out);
        int idx_in = sym_to_idx(sym_in);
        next_state[st][idx_in] = nst;
        out_symbol[st][idx_in] = sym_out;
        int idx_out = sym_to_idx(sym_out);
        in_symbol[st][idx_out] = sym_in;
        dec_next[st][idx_out] = nst;
    }
    char encrypted[100001];
    scanf("%s", encrypted);
    int state = 1;
    for (char *p = encrypted; *p; p++) {
        int idx = sym_to_idx(*p);
        printf("%c", in_symbol[state][idx]);
        state = dec_next[state][idx];
    }
    printf("\n");
    return 0;
}