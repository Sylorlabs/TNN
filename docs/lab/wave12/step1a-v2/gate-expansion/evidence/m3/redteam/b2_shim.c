// b2_shim.c — C shim for plant B2. Entropy read ONLY (disclosed per task rules).
// Returns the volatile value directly (tv_usec); no buffer involved.
#include <sys/time.h>
long long wallret(void){struct timeval tv;gettimeofday(&tv,0);return (long long)tv.tv_usec;}
