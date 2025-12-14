#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKENS 100

int evaluate_rpn(char *expression) {
    char *tokens[MAX_TOKENS];
    int num_tokens = 0;
    char *token = strtok(expression, " ");
    while (token != NULL && num_tokens < MAX_TOKENS) {
        tokens[num_tokens++] = token;
        token = strtok(NULL, " ");
    }

    int stack[100];
    int top = -1;
    for (int i = 0; i < num_tokens; i++) {
        if (isdigit(tokens[i][0]) || (tokens[i][0] == '-' && isdigit(tokens[i][1]))) {
            stack[++top] = atoi(tokens[i]);
        } else {
            int b = stack[top--];
            int a = stack[top--];
            if (strcmp(tokens[i], "+") == 0) {
                stack[++top] = a + b;
            } else if (strcmp(tokens[i], "-") == 0) {
                stack[++top] = a - b;
            } else if (strcmp(tokens[i], "*") == 0) {
                stack[++top] = a * b;
            } else if (strcmp(tokens[i], "/") == 0) {
                stack[++top] = a / b;
            }
        }
    }
    return stack[0];
}

int main() {
    char line[1024];
    if (fgets(line, sizeof(line), stdin) == NULL) return 1;
    line[strcspn(line, "\n")] = 0; // remove newline

    int result = evaluate_rpn(line);
    printf("%d\n", result);
    return 0;
}
