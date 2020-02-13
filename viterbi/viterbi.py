# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words
# q_values is from the return of calc_trigrams()
# e_values is from the return of calc_emissions()
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    tagged = []                    
    def taglist_k(k):
        if k in [-1,0]:
            return(START_SYMBOL)
        else:
            return(taglist)
    #index=0
    taglist_nn = [(i,j) for i in taglist for j in taglist]         
    for sentence_r in brown_dev_words:
        #print(index)
        #index = index+1
        sentence = [word if word in known_words else RARE_SYMBOL\
                      for word in sentence_r]
        tags = []
        viterbi = {}
        backpoint = {}
        viterbi[0] = {('*','*'):0} 
                      
        for step in range(1,len(sentence)+1):
            viterbi[step] = {}
            backpoint[step] ={}
            for s in taglist_k(step):
                for ss in taglist_k(step-1):
                    max_ = float('-Inf')
                    max_pos = None
                    for sss in taglist_k(step-2):
                         if (sentence[step-1],s) in e_values.keys() and viterbi[step-1].get((sss,ss),LOG_PROB_OF_ZERO)+q_values.get((sss,ss,s),LOG_PROB_OF_ZERO)+\
                                e_values.get((sentence[step-1],s))>max_:                         
                            max_ = viterbi[step-1][(sss,ss)]+q_values.get((sss,ss,s),LOG_PROB_OF_ZERO)+e_values[(sentence[step-1],s)]
                            max_pos = sss
                    viterbi[step][(ss,s)] = max_
                    backpoint[step][(ss,s)] = max_pos
           
        max_k = float('-Inf')
        max_pos = []
        for tag in taglist_nn:
            if viterbi[len(sentence)][tag]+ q_values.get((tag[0],tag[1],STOP_SYMBOL),LOG_PROB_OF_ZERO)>max_k:
                max_k = viterbi[len(sentence)][tag]+ q_values.get((tag[0],tag[1],STOP_SYMBOL),LOG_PROB_OF_ZERO)
                max_pos = [tag[0],tag[1]]
        tags = max_pos
        tagss = []
        for k in range(len(sentence),0,-1):
           tags = [backpoint[k][(tags[0],tags[1])]] + tags
        for i in range(len(sentence_r)):
            tagss.append(sentence_r[i]+'/'+ tags[i+2])
        tagged.append(' '.join(tagss)+' \n')
    return tagged
