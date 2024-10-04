import string

# Function to load data from a text file
def load_data(text_file):
    # Open the file and read all lines
    with open(text_file, 'r') as f:
        lines = f.readlines()

    # Strip whitespaces from each line
    lines = [line.strip() for line in lines]
    
    # Initialize two lists to hold English and Telugu text
    english_text = []
    telugu_text = []
    
    # Loop through each line and split by a delimiter '++++$++++'
    for line in lines:
        parts = line.split('++++$++++')
        english_text.append(parts[0].strip())  # English sentence before the delimiter
        telugu_text.append(parts[1].strip())   # Telugu sentence after the delimiter
    
    # Return two lists of English and Telugu sentences
    return english_text, telugu_text

# Function to preprocess sentences
def preprocess(sentences):
    preprocessed_sentences = []

    # Loop through each sentence
    for sentence in sentences:
        # Convert the sentence to lowercase
        sentence = sentence.lower()
        # Remove punctuation using str.maketrans
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        # Split sentence into words
        words = sentence.split()
        
        # Remove specific characters and convert to lowercase
        for i, word in enumerate(words):
            word = word.replace('\u200c','')  # Remove zero-width non-joiner
            word = word.lower()  # Convert word to lowercase
            words[i] = word
        
        # Join the words back into a sentence
        sentence = ' '.join(words)
        preprocessed_sentences.append(sentence)

    return preprocessed_sentences

# Function to get a unique vocabulary from sentences
def get_vocab(sentences):
    vocab = set()
    
    # Loop through each sentence and add words to the vocabulary set
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            vocab.add(word)  # Add the word to the vocabulary set
    
    return list(vocab)  # Return as a list

# Function to tokenize input sentences based on a word-to-index dictionary (wtoi)
def tokenize_input(sentences, wtoi):
    tokenized_sentences = []

    # Loop through each sentence
    for sentence in sentences:
        words = sentence.split()
        arr = [wtoi['<sos>']]  # Start token
        
        # Convert words to their corresponding indices
        for word in words:
            if word not in wtoi:
                arr.append(wtoi['<unk>'])  # Unknown word token
            else:
                arr.append(wtoi[word])
        
        arr.append(wtoi['<eos>'])  # End token
        tokenized_sentences.append(arr)
    
    return tokenized_sentences

# Function to tokenize output sentences and shift them for decoder inputs
def tokenize_output(sentences, wtoi):
    tokenized_sentences = []
    shifted_right = []
    
    # Loop through each sentence
    for sentence in sentences:
        words = sentence.split()
        arr = []
        
        # Convert words to their corresponding indices
        for word in words:
            if word not in wtoi:
                arr.append(wtoi['<unk>'])  # Unknown word token
            else:
                arr.append(wtoi[word])
        
        # Append end token and create shifted version for decoder input
        tokenized_sentences.append(arr + [wtoi['<eos>']])
        shifted_right.append([wtoi['<sos>']] + arr)  # Start token shifted
    
    return tokenized_sentences, shifted_right

# Function to detokenize (convert indices back to words) using an index-to-word dictionary (itow)
def detokenize(tokens, itow):
    output = []
    
    # Convert each token (index) to the corresponding word
    for token in tokens:
        output.append(itow[token])
    
    output = ' '.join(output)  # Join the words into a sentence
    
    return output

# Function to assign sentences into buckets based on their lengths
def assign_buckets(x, boundaries, batch_sizes):
    boundaries = [0] + boundaries  # Add 0 as the lower boundary
    bins = list(zip(boundaries, boundaries[1:], batch_sizes))  # Create bins with upper and lower boundaries
    
    # Create a dictionary with bins as keys and empty lists as values
    buckets = {key: [] for key in bins}
    
    # Assign each sentence to the appropriate bucket based on its length
    for i, sentence in enumerate(x):
        length = len(sentence)
        for lower, upper, batch_size in bins:
            if lower < length <= upper:
                buckets[(lower, upper, batch_size)].append(i)  # Add the index of the sentence to the bucket
                break
    
    return buckets
