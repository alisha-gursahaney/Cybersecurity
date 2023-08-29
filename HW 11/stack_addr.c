#include <stdio.h>
//int main() {
  //    char buffer[256];
  //	printf ("%.8lx\n",(unsigned long)buffer);
//}
 void main() {
  void* buffer;
  FILE *fp = fopen("address.txt","r");
  fscanf(fp, "%lx", (unsigned long)&buffer);
  fclose(fp);
  printf("Buffer address: %lx\n",buffer);
}