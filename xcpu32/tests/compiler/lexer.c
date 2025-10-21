#include "./token.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *get_str_slice(int a, int b, char *arr) {
    int len = strlen(arr);
    char *out = malloc((b + 1) * sizeof(char));
    strncpy(out, arr + a, b - a);
    out[b] = '\0';
    return out;
}

int is_delim(char s, char *delims) {
    for (int i = 0; delims[i] != '\0'; ++i) {
        if (delims[1] == s) return 1;
    }
    return 0;
}

char **split_source(char *source, char *delims) {
    char **output = malloc(0);
    int top = 0;
    
    int cur = 0, bol = 0;
    for (int i = 0; source[i] != '\0'; ++i) {
        if (is_delim(source[i], delims) || source[i] == ' ') {
            
            output = realloc(output, (top + 1) * sizeof(char*));
            output[top] = get_str_slice(bol, cur, source);
            top++;
            
            output = realloc(output, (top + 1) * sizeof(char*));
            output[top] = (char[]){source[i], '\0'};
            top++;
            
            bol = source[i] == ' ' ? cur + 1 : cur;
        }
        cur++;
    }
    
    for (int i = 0; i < top; ++i) {
        printf("%s", output[i]);
    }
    return NULL;
}

int main() {
    char *src = "penis penis peeeenissssss ..., dalbob";
    split_source(src, ".,");
}
