def split_text(text, max_words=100):
    """
    Split big text into list of chunks, each about max_words words.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i+max_words])
        chunks.append(chunk)
    return chunks
