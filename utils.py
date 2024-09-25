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

