#ifndef _TOKENIZER_
#define _TOKENIZER_

#include <iterator>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

class BytePairTokenizer {
    private:


    public:
        /**
         * The set of tokens comprising the vocabulary for the loaded corpus
         * output from the BPE algorithm.
        */
        set<string> vocabulary;

        /**
         * The list of token pairs denoting the merges performed during the 
         * BPE algorithm.   
        */
        vector<pair<string, string>> merges;
        
        /**
         * This function accepts a Corpus object and trains the tokenizer 
         * by generating the tokens comprising the vocabulary for that corpus.
        */
        set<string> Train(
            unordered_map<string, int> words,
            int vocabulary_limit
        );

        /**
         * This function tokenizes a given sentence string using the merges 
         * and vocabulary computed from the initial training.
        */
        vector<string> Tokenize(string sentence);
        
};

#endif