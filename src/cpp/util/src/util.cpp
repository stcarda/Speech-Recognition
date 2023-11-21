#include "../include/util.hpp"

vector<string> SplitString(string str, char delimiter) {
    // Create a string stream from the given string.
    stringstream test(str);

    // Construct a vector of strings which will be used to store the elements
    // of our string split.
    vector<string> arr;

    // Push the delimited elements, retrieved from the string stream, onto the
    // result array.
    string item;
    while (getline(test, item, delimiter)) {
        arr.push_back(item);
    }

    // Push the final word contained in the list onto the returned array.
    //arr.push_back(str);
    return arr;
}

string ToUpper(string str) {
    for (int idx = 0; idx < str.length(); idx++) {
        str[idx] = toupper(str[idx]);
    }
    return str;
}