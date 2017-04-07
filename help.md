#include "stdafx.h"
#include "string.h"
int main(){
	char str[111111];
	while (scanf("%s", str) != EOF)	{
		int len = strlen(str);
		int i, cou = 0, j;
		for (i = 1; i <= len / 16; i++)	{
			int start = (i - 1) * 16;
			int end = i * 16 - 1;
			printf("%08X ", (i - 1) * 16);
			for (j = start; j <= end; j++){
				printf(" %X", str[j]);
				if (j - start == 7) printf(" ");
			}
			printf("  ");
			for (j = start; j <= end; j++) printf("%c", str[j]);
			printf("\n");
		}
	}
	return 0;
}
