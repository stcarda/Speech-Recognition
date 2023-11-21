"""
    corpus = [
        "low",
        "low",
        "low",
        "low",
        "low", 
        "lowest", 
        "lowest",
        "newer",
        "newer",
        "newer",
        "newer",
        "newer",
        "newer", 
        "wider", 
        "wider",
        "wider",
        "new",
        "new"
    ]
    vocabulary, merges = BytePairTokenize(corpus)
    print(vocabulary)
    print(BytePairSegmenter("    lowerlaero  ", merges))

    print(os.path.dirname(os.path.realpath(__file__)))
    f = open(
        r"C:\Users\Sean Carda\Desktop\Projects\Speech-Recognition\data\corpora\shakespeare\input.txt", 
        "r"
    )

    shakespeare = f.read().split(" ")

    #test = wordpunct_tokenize(f.read())

    vocabulary, merges = BytePairTokenize(shakespeare)
    """