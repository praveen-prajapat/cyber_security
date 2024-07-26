#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MEM_LEN 3000

void except(char* source, int e) {
    free(source);
    if (e >= 0) exit(e);
}

int interpret(const char* source) {
    int mem = 0, code = 0;
    char memory[MEM_LEN + 1] = {0};
    int source_len = strlen(source);

    while (code < source_len) {
        char c = source[code];
        switch (c) {
            case '>': mem = (mem + 1) % MEM_LEN; break;
            case '<': mem = (mem - 1 + MEM_LEN) % MEM_LEN; break;
            case '+': memory[mem]++; break;
            case '-': memory[mem]--; break;
            case '.': printf("%c", memory[mem]); break;
            case ',': memory[mem] = fgetc(stdin); break;
            case '[':
                if (!memory[mem]) {
                    int open = 1;
                    while (open) {
                        if (++code == source_len) except(NULL, 0);
                        if (source[code] == '[') open++;
                        if (source[code] == ']') open--;
                    }
                }
                break;
            case ']':
                if (memory[mem]) {
                    int close = 1;
                    while (close) {
                        if (--code == -1) except(NULL, 0);
                        if (source[code] == ']') close++;
                        if (source[code] == '[') close--;
                    }
                }
                break;
            default:
                if (!(c == '\t' || c == '\n' || c == ' ')) {
                    fprintf(stderr, "Invalid character: %c\n", c);
                    except(NULL, 1);
                }
        }
        code++;
    }
    except(NULL, -1);
    return 0;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <brainfuck_code>\n", argv[0]);
        exit(1);
    }
    return interpret(argv[1]);
}
