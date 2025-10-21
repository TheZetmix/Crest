
typedef enum {
    
    KEYWORD,
    ID,
    OPERATION,
    ASSIGN,
    COLON,
    NUMBER,
    HEX_NUMBER,
    SEMICOLON,
    LPAREN,
    RPAREN,
    BODY_OPEN,
    BODY_CLOSE,
    
} toktype;

typedef struct {
    
    toktype type;
    char *literal;
    int pos;
    
} token;
