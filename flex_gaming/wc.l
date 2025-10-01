ws      [ \t]
nonws   [^ \t\n]

%option main noyywrap
%%
        int cc = 0, wc = 0, lc = 0;

{nonws}+        cc += yyleng; ++wc;

{ws}+   cc += yyleng;

\n      ++lc; ++cc;

<<EOF>> {
        printf("\t%d\t%d\t%d\n", lc, wc, cc);
        yyterminate();
        }
