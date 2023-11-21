from collections import Counter
from nltk.tokenize import wordpunct_tokenize
import os
from tokenizers import Tokenizer, models, pre_tokenizers, decoders, trainers, processors
import time


def BytePairTokenize(corpus):
    """
    This function accepts a list of strings comprising our corpus and 
    tokenizes those strings into a vocabulary of tokens.

    Args:
        corpus: a list of strings comprising the corpus.

    Returns:
        vocabulary: a list of strings comprising our corpus' vocabulary.
        merges: an ordered list of tuples comprising the sequence of merges
                we took to generate the vocabulary.

    Raises:

    """
    # ADD ARGUMENT PARSING.

    # Modify the corpus such that each word in the list is concluded with
    # and underscore.
    corpus = [word + "_" for word in corpus]
    
    # Ensure that our corpus only contains unique strings. We also need
    # the frequency of each unique word in the corpus.
    unique_corpus = list(set(corpus))
    corpus_frequencies = Counter(corpus)

    # Split each unique corpus word by characters.
    split_unique_corpus = [list(word) for word in unique_corpus]

    # Create a list in which we will log the merges made by the algorithm.
    merges = []

    # Generate our initial vocabulary which is just the unique characters 
    # contained in our unique corpus.
    vocabulary = list(set(''.join(unique_corpus)))
    while numel(split_unique_corpus) is not len(split_unique_corpus):
        # For all strings in the unique corpus, find the adjacent character
        # pairings that occur most frequently in the corpus.
        adj_pairs = {}
        set_of_pairs = []
        for word in split_unique_corpus:
            for idx in range(len(word) - 1):
                pair = ''.join(word[idx:idx + 2])
                if pair not in list(adj_pairs.keys()):
                    adj_pairs[pair] = corpus_frequencies[''.join(word)]
                    set_of_pairs.append((word[idx], word[idx + 1]))
                else:
                    adj_pairs[pair] += corpus_frequencies[''.join(word)]
        
        # Get the pairing with the max count.
        most_occured_pairing = max(adj_pairs, key=adj_pairs.get)
        pairing_idx = list(adj_pairs.keys()).index(most_occured_pairing)

        # Add the most occured pairing into the vocabulary and add the tuple
        # of tokens to the merge list.
        vocabulary.append(most_occured_pairing)
        merges.append(set_of_pairs[pairing_idx])
        
        # For all words in the split corpus, find the occurances where we see
        # the most occured pairing and replace those indices with the pairing.
        for word in split_unique_corpus:
            for idx in range(len(word) - 1):
                pair = ''.join(word[idx:idx + 2])
                if pair == most_occured_pairing:
                    del word[idx:idx + 2]
                    word.insert(idx, most_occured_pairing)

    return vocabulary, merges


def BytePairSegmenter(sentence, merges):
    # Replace all whitespaces in the sentence with an underscore.
    sentence = sentence.strip().replace(" ", "_") + "_"

    # For each word, apply merges until we cannot apply any more.
    characters = list(sentence)
    for merge in merges:
        characters = ReplacePair(characters, merge)
    return characters


def ReplacePair(arr, pair):
    """
    ** This fuction header needs work...
    This function accepts a generic list and a tuple pair denoting a sublist
    to be replaced in the original list and replaces all instances of the
    sublist in the original list with a merged pair.

    Example.
    arr = ['H', 'e', 'l', 'l', 'o']
    pair = ('ll')
    ReplacePair(arr, pair) = ['H', 'e', 'll', 'o']

    Args:
        arr: a list containing generic elements.
        pair: a tuple of length 2 containing the elements to match against.

    Returns:
        a new array with all instances of the sublist in arr replaces with
        a merged pairing.
    """
    length = len(arr)
    idx = 0
    while idx < length - 1:
        # Get the current pair of tokens.
        adj_pair = (arr[idx], arr[idx + 1])

        # If the pair is a match, delete the two characters and add the joint
        # character pair as one token.
        if adj_pair == pair:
            del arr[idx:idx + 2]
            arr.insert(idx, ''.join(pair))
            
            # Update the length of the array since we have concatenated 
            # elements
            length = len(arr)
        
        # Increment the index.
        idx += 1
    
    # Return the updated array.
    return arr

            


def numel(list_of_lists):
    """
    This function acts the same as the "numel" function in MATLAB whereby
    we can obtain the total number of elements within a multidimensional
    array. In this case, we will to obtain the total number of elements
    within a list of lists.
    
    Args:
        list_of_lists: a list of lists of arbitrary type.

    Returns:
        The total number of elements contained in the list of lists.
    """
    return sum(len(arr) for arr in list_of_lists)



if __name__=='__main__':

    # Initialize a tokenizer
    tokenizer = Tokenizer(models.BPE())

    # Customize pre-tokenization and decoding
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=True)
    tokenizer.decoder = decoders.ByteLevel()
    tokenizer.post_processor = processors.ByteLevel(trim_offsets=True)

    # And then train
    trainer = trainers.BpeTrainer(
        vocab_size=20000,
        min_frequency=2,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet()
    )

    start = time.time()

    tokenizer.train([
        r"C:\Users\Sean Carda\Desktop\Projects\Speech-Recognition\data\corpora\shakespeare\input.txt"
    ], trainer=trainer)

    print(time.time() - start)


