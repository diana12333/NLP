
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
    word_flat = [item for sublist in brown_words for item in sublist]
    count_uni = Counter(word_flat)
    known_words = set([key for key in count_uni.keys() if count_uni[key]>RARE_WORD_MAX_FREQ])
    return known_words


# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace(word, wordset,rare):
    if word in wordset:
        return(word)
    else:
        return(rare)
    
def replace_rare(brown_words, known_words):
    brown_words_rare = []
    for sen in brown_words:
        brown_words_rare.append([replace(word,known_words,RARE_SYMBOL) for word in sen])
    return brown_words_rare
