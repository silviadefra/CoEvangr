#include <stdlib.h>
#include <stdio.h>


void h(int z) {
	printf("Hello\n");
}

void g(int y) {
	h(y + 11);
}

void f(int x) {
	if(x > 7)
		g(x - 5);
	else
		h(x * 2);
		printf("%p\n",h);
}

int main() {
	f(3);
	printf("ciao\n");
}
