#ifndef _CORPUS_
#define _CORPUS_

#include <algorithm>
#include <cstring>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <unordered_map>
#include "../../util/include/util.hpp"

using namespace std;

/**
 * A class designed to read the contents of a corpus text file. This class
 * assumes that the file is in .txt format and will process it accordingly.
 * The purpos of this class is to generate a 
*/
class TextCorpusReader {
    private:
        string corpus_name_;
        string file_type_;
        ifstream file_stream_;

    public:  
        /**
         * A map whose keys are the unique words in the corpus and whose
         * values are the frequency of those words in the corpus.
        */
        unordered_map<string, int> words;


        /**
         * Constructor for the class. Accepts the name of a corpus and scans
         * the list of known corpus data directories to open the proper files.
        */
        TextCorpusReader(string name);

        // Functions.
        void GenerateWords();
};

/**
 * Helper function in which we attempt to get a file pointer to a given file
 * path. Raises an error if we cannot open the file. This function prevents
 * us from having to write the same error logic every time we wish to open
 * a file.
*/
ifstream OpenTextFile(string file_path);

#endif