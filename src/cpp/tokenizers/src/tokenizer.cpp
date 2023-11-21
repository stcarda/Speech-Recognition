#include "../include/tokenizer.hpp"
#include <chrono>
#include <iostream>

set<string> BytePairTokenizer::Train(
    unordered_map<string, int> words,
    int vocabulary_limit
) {
    using namespace std::chrono;

    auto start = high_resolution_clock::now();

    // Get the unique corpus words.
    vector<string> unique_words;
    for (pair<string, int> entry : words) {
        unique_words.push_back(entry.first);
    }

    // Merge the unique strings into one single string.
    ostringstream joined_str_stream;
    copy(
        unique_words.begin(), 
        unique_words.end(),
        std::ostream_iterator<std::string>(joined_str_stream, "")
    );
    string joined_str = joined_str_stream.str();

    // Take the merged string and compute the unique characters for our
    // initial vocabulary.
    set<char> initial_vocab(
        joined_str.begin(), 
        joined_str.end()
    );

    // We obtained a character set initial vocab, but we need our vocab to 
    // be a set of strings.
    for (char entry : initial_vocab) {
        this->vocabulary.insert(string(1, entry));
    }


    // Count the adjacent pairs in the set of unique words.
    map<pair<string, string>, int> unique_pairs;
    vector<vector<string>> split_words(
        unique_words.size(), 
        vector<string>(0, "")
    );
    for (int idx = 0; idx < unique_words.size(); idx++) {
        string word = unique_words[idx];
        for (char c : word) {
            split_words[idx].push_back(string(1, c));
        }

        for (int jdx = 0; jdx < word.length() - 1; jdx++) {
            unique_pairs[
                pair<string, string>(
                    string(1, word[jdx]), 
                    string(1, word[jdx + 1])
                )
            ] += words[word];
        }
    }

    printf("%zd\n", unique_pairs.size());




    auto end = high_resolution_clock::now();
    auto dur = duration_cast<milliseconds>(end - start);
    cout << "time: " << dur.count() << endl;


    set<string> result;
    return result;  
}