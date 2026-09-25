// a2_shim.c — C shim for plant A2. Entropy read ONLY (disclosed per task rules).
// Writes 8 volatile bytes (tv_usec) to the caller-provided buffer.
#include <sys/time.h>
void wall8(unsigned long long *p){struct timeval tv;gettimeofday(&tv,0);*p=(unsigned long long)tv.tv_usec;}
