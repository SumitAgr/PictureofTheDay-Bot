import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize

def summarize_text(image_description):
    stop_words = set(stopwords.words("english"))
    
    words = word_tokenize(image_description)

    frequency_table = dict()

    for word in words: 
        word = word.lower() 
        if word in stop_words: 
            continue
        if word in frequency_table: 
            frequency_table[word] += 1
        else: 
            frequency_table[word] = 1

    complete_sentences = sent_tokenize(image_description)
    complete_sentences_value = dict()

    for sentence in complete_sentences: 
        for word, freq in frequency_table.items(): 
            if word in sentence.lower(): 
                if sentence in complete_sentences_value:
                    complete_sentences_value[sentence] += freq 
                else: 
                    complete_sentences_value[sentence] = freq

    sum_of_values = 0
    for sentence in complete_sentences_value:
        sum_of_values += complete_sentences_value[sentence]

    average = int(sum_of_values / len(complete_sentences_value))

    text_summary = ''

    for sentence in complete_sentences: 
        if (sentence in complete_sentences_value) and (complete_sentences_value[sentence] > (1.2 * average)): 
            text_summary += " " + sentence

    return text_summary
