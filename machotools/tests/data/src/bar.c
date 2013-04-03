#include <stdio.h>

#ifndef BAR_VERSION
#define BAR_VERSION 0
#endif

int bar()
{
	printf("BAR VERSION: %d\n", BAR_VERSION);
	return 0;
}
