import string
def tokenizer(sentences):
    vocab = set()
    tokenized_sentences = []
    
    for sentence in sentences:
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        words = sentence.split()
        for i, word in enumerate(words):
            word = word.replace('\u200c','')
            word = word.lower()
            words[i] = word
            vocab.add(word)
        tokenized_sentences.append(words)
    return tokenized_sentences,list(vocab)

def load_data(text_file):
    with open(text_file, 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    english_text = []
    telugu_text = []
    
    for line in lines:
        parts = line.split('++++$++++')
        english_text.append(parts[0].strip())
        telugu_text.append(parts[1].strip())
    
    return english_text, telugu_text