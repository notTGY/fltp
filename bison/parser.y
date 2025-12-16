%{
#include <stdio.h>

int depth_round = 0, max_round = 0;
int depth_square = 0, max_square = 0;
int depth_brace = 0, max_brace = 0;
%}

%token LPAREN RPAREN LSQUARE RSQUARE LBRACE RBRACE

%start input

%%

input: expr { printf("() : %d\n[] : %d\n{} : %d\n", max_round, max_square, max_brace); }

expr: 
     | expr LPAREN {if(++depth_round > max_round) max_round = depth_round;} expr RPAREN {depth_round--;}
     | expr LSQUARE {if(++depth_square > max_square) max_square = depth_square;} expr RSQUARE {depth_square--;}
     | expr LBRACE {if(++depth_brace > max_brace) max_brace = depth_brace;} expr RBRACE {depth_brace--;}
;

%%

int main() {
    yyparse();
    return 0;
}

void yyerror(char *s) {
    fprintf(stderr, "error: %s\n", s);
}
