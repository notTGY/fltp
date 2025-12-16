all: test-wc test-anbn

test-anbn: anbn
	echo "aaabbb" | ./anbn && echo "expected: 1"

test-wc: wc
	echo "hello world" | ./wc && echo "expected:\t1\t2\t12"

wc: wc.l
	flex wc.l && gcc lex.yy.c -o wc && rm lex.yy.c

anbn: anbn.l
	flex anbn.l && gcc lex.yy.c -o anbn && rm lex.yy.c
