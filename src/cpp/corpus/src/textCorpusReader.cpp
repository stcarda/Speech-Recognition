#include "../include/corpus.hpp"

TextCorpusReader::TextCorpusReader(string name) {
    this->corpus_name_ = name;

    // Get the proper environment variable based on the given name.
    string env_variable_name = ToUpper(name) + "_PATH";

    // Locate the file that is specified by the given name.
    string data_directory;
    if (getenv(env_variable_name.c_str())) {
        data_directory = getenv(env_variable_name.c_str());
    }
    else {
        printf(
            "Error: Environment variable %s is not set\n", env_variable_name.c_str()
        );
        throw runtime_error("");
    }
    
    // Create a file pointer to the corpus directory.
    this->file_stream_ = OpenTextFile(data_directory);
}

void TextCorpusReader::GenerateWords() {
    // Read the entire text file into a string.
    this->file_stream_.seekg(0, ios::end);
    size_t size = this->file_stream_.tellg();
    string buffer(size, ' ');
    this->file_stream_.seekg(0);
    this->file_stream_.read(&buffer[0], size);

    // Convert the read string into a vector of words. We want to separate the
    // text by whitespace here.
    vector<string> total_words = SplitString(buffer, ' ');

    // Count the frequencies of the words in the corpus.
    unordered_map<string, int> test;
    for (string word: total_words) {
        this->words[word + "_"]++;
    }
}

ifstream OpenTextFile(string file_path) {
    ifstream file_stream;
    file_stream.open(file_path.c_str(), ifstream::in);
    if (!file_stream) {
        string err = "Error: Could not open file " + file_path;
        printf("%s\n", err.c_str());
        throw runtime_error(err);
    }
    return file_stream;
}