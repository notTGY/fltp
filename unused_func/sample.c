#include <stdio.h>
#include"other.c"

static void used_leaf(void) {
    printf("used\\n");
}

static void used_mid(void) {
    used_leaf();
}

static void unused_leaf(void) {
    printf("unused\\n");
}

static void unused_mid(void) {
    unused_leaf();
}

static void also_unused(void) {
}

int main(void) {
    used_mid();
    return 0;
}
