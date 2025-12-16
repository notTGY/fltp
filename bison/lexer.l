%{
#include "parser.tab.h"
void yyerror(char *s);
%}

%%

"(" return LPAREN;
")" return RPAREN;
"[" return LSQUARE;
"]" return RSQUARE;
"{" return LBRACE;
"}" return RBRACE;
[ \t\n] ; /* ignore whitespace */
. { yyerror("invalid character"); return MYYYERROR; }

%%

int yywrap() { return 1; }
