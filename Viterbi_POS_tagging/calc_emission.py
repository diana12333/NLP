# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set (should not include start and stop tags)
def calc_emission(brown_words_rare, brown_tags):
    e_values = {}
    taglist = set([])
    word_tag = []
    brown_words_rares_flat = [item for sublist in brown_words_rare for item in sublist]
    brown_tag_flat = [item for sublist in brown_tags for item in sublist]
    for i in range(len(brown_words_rares_flat)):
        word_tag.append((brown_words_rares_flat[i],brown_tag_flat[i]))
    count_tag = Counter(brown_tag_flat)
    count_word_tag = Counter(word_tag)
    for key in count_word_tag.keys():
        e_values[key] = math.log2(count_word_tag[key]/count_tag[key[1]])
    taglist = [tag for tag in count_tag.keys() if tag not in [START_SYMBOL,STOP_SYMBOL]]
    return e_values, taglist
