#include "corpus/include/corpus.hpp"
#include "tokenizers/include/tokenizer.hpp"

using namespace std;

int main(int argc, char* argv[], char* envp[]) {    
    TextCorpusReader speare = TextCorpusReader("shakespeare");

    speare.GenerateWords();

    printf("Length of words: %zd\n", speare.words.size());

    unordered_map<string, int> words({
        {"low_", 5},
        {"lowest_", 2},
        {"newer_", 6},
        {"wider_", 3},
        {"new_", 2}
    });

    BytePairTokenizer tokenizer;
    tokenizer.Train(speare.words, 20000);
    //tokenizer.Train(words, 20000);
}