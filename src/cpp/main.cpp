#include "corpus/include/corpus.hpp"
#include "tokenizers/include/tokenizer.hpp"
#include <fftw3.h>

using namespace std;

int main(int argc, char* argv[], char* envp[]) {    
    fftw_complex *in, *out;
    fftw_plan p;

    int size_in = 512;
    int N = 1024;

    in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * size_in);
    out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);
    p = fftw_plan_dft_1d(N, in, out, FFTW_FORWARD, FFTW_ESTIMATE);

    fftw_execute(p);

    fftw_destroy_plan(p);
    fftw_free(in); fftw_free(out);

}