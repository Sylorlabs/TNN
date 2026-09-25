#define _GNU_SOURCE
#include <stdio.h>
#include <time.h>
#include <dlfcn.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
int main() {
    // resolve the vDSO symbol directly
    void *h = dlopen("linux-vdso.so.1", RTLD_NOW);
    printf("vdso handle=%p\n", h);
    int (*vcgt)(clockid_t, struct timespec*) = NULL;
    if (h) vcgt = dlsym(h, "__vdso_clock_gettime");
    printf("__vdso_clock_gettime=%p\n", (void*)vcgt);
    // install the M1 filter via seccomp(2)
    struct sock_filter f[] = {
        {0x20,0,0,4},{0x15,1,0,0xc000003e},{0x6,0,0,0x80000000},
        {0x20,0,0,0},{0x15,2,0,318},{0x15,1,0,228},{0x15,0,1,96},
        {0x6,0,0,0x80000000},{0x6,0,0,0x7fff0000},
    };
    struct { unsigned short len; unsigned char p[6]; void *fp; } prog = {9,{0},f};
    syscall(321, 38, 1, 0, 0, 0, 0); // prctl PR_SET_NO_NEW_PRIVS via raw syscall
    if (syscall(317, 1, 0, &prog, 0, 0, 0)) { perror("seccomp"); return 1; }
    printf("filter installed\n");
    struct timespec ts;
    if (vcgt) {
        int r = vcgt(CLOCK_REALTIME, &ts);
        printf("direct vDSO call SURVIVED r=%d t=%ld\n", r, (long)ts.tv_sec);
    } else {
        printf("no vDSO symbol; trying glibc clock_gettime\n");
        clock_gettime(CLOCK_REALTIME, &ts);
        printf("glibc clock_gettime SURVIVED t=%ld\n", (long)ts.tv_sec);
    }
    return 0;
}
