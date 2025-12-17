all: test-wc test-anbn


bench-wc: test.txt
	time (cat test.txt | ./wc) && \
	time (cat test.txt | wc)

test.txt:
	python3 -c "open('test.txt', 'w').write((('a'*1000 + " ") * 10 + '\n') * 100)"

test-anbn: anbn
	echo "aaabbb" | ./anbn && echo "expected:\n1"

test-wc: wc
	echo "hello world" | ./wc && echo "expected:\n\t1\t2\t12"

wc: wc.l
	flex wc.l && gcc lex.yy.c -o wc && rm lex.yy.c

anbn: anbn.l
	flex anbn.l && gcc lex.yy.c -o anbn && rm lex.yy.c
