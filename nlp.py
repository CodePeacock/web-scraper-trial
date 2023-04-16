"""This module contains functions that can be used to perform Natural Language Processing tasks."""
from collections import Counter

import nltk as nlp
import pyphen
from nltk.corpus import cmudict, stopwords

text = ""
# Positive Score of the text
def positive_score(text: str):
    """This function takes a string as input and returns the positive score of the text."""
    positive_words = []
    with open("positive-words.txt", "r", encoding="ISO-8859-1") as file:
        positive_words.extend(line.strip() for line in file if not line.startswith(";"))
    positive_words = set(positive_words)
    tokens = nlp.word_tokenize(text)
    pos_score = sum(word in positive_words for word in tokens)
    return int(pos_score)


positive_score(text)

# Negative Score of the text
def negative_score(text):
    """This function takes a string as input and returns the negative score of the text."""
    negative_words = []
    with open("negative-words.txt", "r", encoding="ISO-8859-1") as file:
        negative_words.extend(line.strip() for line in file if not line.startswith(";"))
    negative_words = set(negative_words)
    tokens = nlp.word_tokenize(text)
    neg_score = sum(word in negative_words for word in tokens)
    return int(neg_score)


negative_score(text)
# Polarity Score of the text
def polarity_score():
    """This function takes a string as input and returns the polarity score of the text."""
    return positive_score(text) - negative_score(text)


def polarity():
    """This function takes a string as input and returns the polarity of the text."""
    if polarity_score() > 0:
        return print("Positive : ", polarity_score)
    if polarity_score() < 0:
        return print("Negative: ", polarity_score)
    return print("Neutral: ", polarity_score)


# Subjectivity Score of the text
def subjectivity_score():
    """This function takes a string as input and returns the subjectivity score of the text."""
    return positive_score(text) + negative_score(text)


def subjectivity():
    """This function takes a string as input and returns the subjectivity of the text."""
    if subjectivity_score() > 0:
        return print("Subjective : ", subjectivity_score)
    if subjectivity_score() < 0:
        return print("Objective: ", subjectivity_score)
    return print("Neutral: ", subjectivity_score)


# Average Sentence Length & Average Number of Words per Sentence
def avg_sentence_length_and_avg_words(text):
    """This function takes a string as input and returns the average sentence length of the text."""
    sentences = nlp.sent_tokenize(text)
    words = nlp.word_tokenize(text)
    return len(words) / len(sentences)


# Complex Words Count
def complex_words(text):
    """This function takes a string as input and returns the number of complex words in the text."""
    dic = pyphen.Pyphen(lang="en")
    sentences = nlp.sent_tokenize(text)

    # Tokenize the sentences into words
    words = [nlp.word_tokenize(sentence) for sentence in sentences]

    complex_words = 0
    for sentence in words:
        for word in sentence:
            syllables = len(dic.inserted(word).split("-"))
            if syllables >= 3:
                complex_words += 1
    return complex_words


# Fog Index
def calculate_fog_index(text):
    # Tokenize the text into sentences
    d = cmudict.dict()
    sentences = nlp.sent_tokenize(text)

    # Tokenize the sentences into words
    words = [nlp.word_tokenize(sentence) for sentence in sentences]

    # Calculate the average sentence length in words
    avg_sentence_length = sum(len(sentence) for sentence in words) / len(sentences)

    # Count the number of complex words (words with 3 or more syllables)
    complex_words = 0
    for sentence in words:
        for word in sentence:
            pronunciations = d.get(word.lower(), [])
            if pronunciations and any(x[-1].isdigit() for x in pronunciations):
                syllables = len([x for x in pronunciations if x[-1].isdigit()])
                if syllables >= 3:
                    complex_words += 1

    return 0.4 * (avg_sentence_length + 100 * (complex_words / len(words)))


def syllables(word):
    """This function takes a string as input and returns the number of syllables in the text."""
    count = 0
    vowels = "aeiou"
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if word.endswith("le"):
        count += 1
    if count == 0:
        count += 1
    return count


# Word Count removing stop words and punctuations
def word_count(text):
    """'This function takes a string as input and returns the word count of the text."""

    # Load the stopwords
    stop_words = set(stopwords.words("english"))

    # Tokenize the text into words
    words = text.split()

    # Remove the stopwords
    words = [word for word in words if word.lower() not in stop_words]

    return len(list(Counter(words).keys()))


# Personal Pronoun Count
def personal_pronoun_count(text):
    """This function takes a string as input and returns the number of personal pronouns in the text."""
    personal_pronouns = [
        "i",
        "me",
        "my",
        "mine",
        "we",
        "us",
        "our",
        "ours",
        "you",
        "your",
        "yours",
        "he",
        "him",
        "his",
        "she",
        "her",
        "hers",
        "it",
        "its",
        "they",
        "them",
        "their",
        "theirs",
    ]
    words = nlp.word_tokenize(text)
    return sum(word in personal_pronouns for word in words)


# Average Word Length
def avg_word_length(text):
    """This function takes a string as input and returns the average word length of the text."""
    words = nlp.word_tokenize(text)
    word_length = sum(len(word) for word in words)
    return int(word_length / len(words))
