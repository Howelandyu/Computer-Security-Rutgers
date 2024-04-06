#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/types.h>
#include <dlfcn.h>
#include <string.h>
#include <stdbool.h>

// function pointer
struct dirent * (*real_readdir)(DIR *dirp) = NULL;

// Name:Haoran Yu
// netID: hy318
// RUID: 184001384
// your code for readdir goes here
//  LD_PRELOAD=$PWD/hidefile.so ls
struct dirent *readdir(DIR *dirp) {
    if (real_readdir == NULL)
    {
        char *error;
        real_readdir = dlsym(RTLD_NEXT, "readdir");
        error = dlerror();
        if (error != NULL)
        {
            fprintf(stderr, "%s\n", error);
            exit(1);
        }
    }
    // return (*real_readdir)(dirp);

    char *hidden = getenv("HIDDEN");
    
    bool is_hidden_defined = true;
    
    if (hidden == NULL) {
        is_hidden_defined = false;
    }
    // fprintf(stderr, "%s\n", is_hidden_defined ? hidden : "not");
    struct dirent *curr = (*real_readdir)(dirp);
    if (curr == NULL) {
        return curr;
    }
    // fprintf(stderr, "%s\n", curr->d_name);
    while (curr->d_type != DT_REG) {
        curr = (*real_readdir)(dirp);
        // fprintf(stderr, "%s\n", curr->d_name);
    }
    if (!is_hidden_defined) {
        return curr;
    }
    while (true) {
        curr = (*real_readdir)(dirp);
        if (curr == NULL) {
            return curr;
        }
        if (curr->d_type != DT_REG) {
            continue;
        }
        if (strcmp(curr->d_name, hidden) == 0) {
            continue;
        }
        break;
    }
    return curr;

}