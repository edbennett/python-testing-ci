def word_count(text, word=""):
    """
    Count the number of occurences of ``word`` in a string.
    If ``word`` is not set, count all words.

    Args:
        text (str): the text corpus to search through
        word (str): the word to count instances of

    Returns:
        int: the count of ``word`` in ``text``
    """
    if word:
        count = 0
        for text_word in text.split():
            if text_word == word:
                count += 1
        return count
    else:
        return len(text.split())
