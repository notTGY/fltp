A      a
B   b

%option main noyywrap
%%
        int a = 0, b = 0;

{A}        a++;

{B}   b++;

<<EOF>> {
        printf("%d\n", a == b);
        yyterminate();
        }
