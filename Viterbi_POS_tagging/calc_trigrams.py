# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags):
    q_values = {}
    bigram_tuples_tag = [list(nltk.bigrams([START_SYMBOL]+sen)) for sen in brown_tags]
    bigram_tuples_flat_tag = [item for sublist in bigram_tuples_tag for item in sublist]
    count_bi_tag = Counter(bigram_tuples_flat_tag)
    
    trigram_tuples_tag = [list(nltk.trigrams([START_SYMBOL, START_SYMBOL]+sen)) for sen in brown_tags]
    trigram_tuples_flat_tag = [item for sublist in trigram_tuples_tag for item in sublist]
    count_tri_tag = Counter(trigram_tuples_flat_tag)
    
    count_bi_tag[(START_SYMBOL,START_SYMBOL)] = len(brown_tags)
    for i in count_tri_tag.keys():
        q_values[i] = math.log(count_tri_tag[i]/count_bi_tag[i[0:2]],2)
    return q_values
