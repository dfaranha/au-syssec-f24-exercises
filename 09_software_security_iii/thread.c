#include <assert.h>
#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    size_t thread_id;
    size_t num_threads;
    long* num_primes;
    long max_number;
    pthread_mutex_t* mutex;
} thread_arg_t;

bool is_prime(long n) {
    if (n <= 1) {
        return false;
    }
    long test = 2;
    while (test * test <= n) {
        if (n % test == 0) {
            return false;
        }
        ++test;
    }
    return true;
}

void* thread_function(void* arg) {
    thread_arg_t* thread_arg = arg;
    for (long n = thread_arg->thread_id; n < thread_arg->max_number; n += thread_arg->num_threads) {
        if (is_prime(n)) {
            long num_primes = *thread_arg->num_primes;
            num_primes += 1;
            pthread_mutex_lock(thread_arg->mutex);
            *thread_arg->num_primes = num_primes;
            pthread_mutex_unlock(thread_arg->mutex);
        }
    }
    return NULL;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s <max_number> <num_threads>\n", argv[0]);
        return 1;
    }

    long num_primes = 0;
    long max_number = strtoul(argv[1], NULL, 0);
    size_t num_threads = strtoul(argv[2], NULL, 0);

    pthread_t* threads = calloc(num_threads, sizeof(pthread_t));
    assert(threads != NULL);

    thread_arg_t* thread_args = calloc(num_threads, sizeof(thread_arg_t));
    assert(thread_args != NULL);

    pthread_mutex_t mutex;
    pthread_mutex_init(&mutex, NULL);
    pthread_mutex_unlock(&mutex);

    for (size_t i = 0; i < num_threads; ++i) {
        thread_args[i].thread_id = i;
        thread_args[i].num_threads = num_threads;
        thread_args[i].num_primes = &num_primes;
        thread_args[i].max_number = max_number;
        thread_args[i].mutex = &mutex;
        int ret = pthread_create(&threads[i], NULL, thread_function, &thread_args[i]);
        assert(ret == 0);
    }

    for (size_t i = 0; i < num_threads; ++i) {
        int ret = pthread_join(threads[i], NULL);
        assert(ret == 0);
    }

    printf("there are %ld primes up to %ld\n", num_primes, max_number);

    free(thread_args);
    free(threads);

    return 0;
}
