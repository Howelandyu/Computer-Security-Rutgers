#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <dirent.h>
#include <dlfcn.h>

// Name:Haoran Yu
// netID:hy318
// RUID:184001384
// your code for time() goes here

time_t (*real_time)(time_t *t) = NULL;

time_t time(time_t *t) {
    static int num_calls = 0;

    if (real_time == NULL) {
        char *error;
        real_time = dlsym(RTLD_NEXT, "time");
        error = dlerror();
        if (error != NULL)
        {
            fprintf(stderr, "%s\n", error);
            exit(1);
        }
    }

    if (num_calls == 0) {
        num_calls++;
        // 09/01/2020 @ 12:00am (UTC)
        time_t fake_t = 1598918400;
        if (t != NULL) {
            *t = fake_t;
        }
        return fake_t;
    } else {
        num_calls++;
        time_t real_t;
        real_t = (*real_time)(NULL);
        if (t != NULL) {
            *t = real_t;
        }
        return real_t;
    }
}
