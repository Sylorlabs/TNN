#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
static void w(const char *s){ syscall(1, 1, s, 26); }
int main() {
    struct sock_filter f[] = {
        {0x20,0,0,4},{0x15,1,0,0xc000003e},{0x6,0,0,0x80000000},
        {0x20,0,0,0},{0x15,2,0,318},{0x15,1,0,228},{0x15,0,1,96},
        {0x6,0,0,0x80000000},{0x6,0,0,0x7fff0000},
    };
    struct { unsigned short len; unsigned char p[6]; void *fp; } prog = {9,{0},f};
    syscall(157, 38, 1, 0, 0, 0, 0); // prctl NO_NEW_PRIVS
    if (syscall(317, 1, 0, &prog, 0, 0, 0)) { w("seccomp install failed...."); return 1; }
    w("filter installed..........");
    struct timespec ts;
    int r = clock_gettime(CLOCK_REALTIME, &ts);
    w("glibc clock_gettime ok....");
    // raw syscall must die (proves filter live)
    long rr = syscall(228, 1, &ts, 0, 0, 0, 0);
    w("raw syscall survived?!....");
    return 0;
}
