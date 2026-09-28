// rdtsc_shim.c — tiny C shim providing the rdtsc instruction for P07.
// Build: gcc -shared -fPIC -O2 -o librdtsc_m3.so rdtsc_shim.c
// Pure-Zag cannot emit rdtsc; this is test infrastructure for one plant.
// The plant's Zag code calls it only through m3_rdtsc(), which emits
// T-READ CLOCK (the method's detection point).
#include <stdint.h>
#if defined(__x86_64__)
#include <x86intrin.h>
uint64_t m3_rdtsc_u64(void){ return __rdtsc(); }
#else
uint64_t m3_rdtsc_u64(void){ return 0; }
#endif
