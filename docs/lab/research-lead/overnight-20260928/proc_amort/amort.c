/* amort.c: conventional baseline for the learned-procedure amortization test.
 * Straightforward C implementation of D1 = majority(X1,X2,X3),
 * same input cycling (x = i & 63), same checksum recurrence (acc*31+out).
 * Compiled with gcc -O2. No tricks: no SIMD, no unrolling pragmas.
 */
#include <stdio.h>
#include <stdint.h>
#include <sys/time.h>

static long peak_rss_kb(void) {
  FILE *f = fopen("/proc/self/status", "r");
  long v = 0;
  if (f) {
    char line[256];
    while (fgets(line, sizeof(line), f)) {
      if (sscanf(line, "VmHWM: %ld", &v) == 1) break;
    }
    fclose(f);
  }
  return v;
}

int main(void) {
  const uint64_t N = 67108864ULL;
  uint64_t acc = 0;
  struct timeval t0, t1;
  gettimeofday(&t0, 0);
  for (uint64_t i = 0; i < N; i++) {
    int x = (int)(i & 63);
    int x1 = (x >> 0) & 1;
    int x2 = (x >> 1) & 1;
    int x3 = (x >> 2) & 1;
    int o = ((x1 & x2) | (x2 & x3) | (x1 & x3));
    acc = acc * 31 + (uint64_t)o;
  }
  gettimeofday(&t1, 0);
  long ms = (t1.tv_sec - t0.tv_sec) * 1000 + (t1.tv_usec - t0.tv_usec) / 1000;
  /* sink through a volatile store so the loop cannot be eliminated */
  static volatile uint64_t sink;
  sink = acc;
  printf("arm=B1 ms=%ld chk=%016llx rss=%ld\n",
         ms, (unsigned long long)sink, peak_rss_kb());
  return 0;
}
