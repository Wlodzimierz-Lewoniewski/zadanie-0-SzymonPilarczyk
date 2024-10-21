import nltk
import math
from collections import defaultdict
from urllib.request import urlopen

# Pobranie zasobu punkt
nltk.download('punkt')

# Funkcja do lematyzacji
def load_lemmatization_dict(url):
    lemmatization_dict = {}
    response = urlopen(url)
    for line in response.read().decode('utf-8').splitlines():
        parts = line.strip().split('\t')
        if len(parts) == 2:
            lemmatization_dict[parts[0]] = parts[1]
    return lemmatization_dict

# Tokenizacja i lematyzacja
def tokenize_and_lemmatize(text, lemmatization_dict):
    tokens = nltk.word_tokenize(text)
    lemmatized_tokens = [lemmatization_dict.get(token.lower(), token.lower()) for token in tokens]
    return lemmatized_tokens

# Obliczanie TF
def compute_tf(doc):
    tf = defaultdict(int)
    max_freq = 0
    for word in doc:
        tf[word] += 1
        if tf[word] > max_freq:
            max_freq = tf[word]
    if max_freq > 0:
        for word in tf:
            tf[word] /= max_freq
    return tf

# Obliczanie IDF
def compute_idf(documents):
    idf = defaultdict(int)
    N = len(documents)
    for doc in documents:
        unique_words = set(doc)
        for word in unique_words:
            idf[word] += 1
    for word in idf:
        idf[word] = math.log10(N / idf[word]) if idf[word] > 0 else 0
    return idf

# Obliczanie TF-IDF
def compute_tfidf(documents):
    tfidf = []
    idf = compute_idf(documents)
    for doc in documents:
        tf = compute_tf(doc)
        tfidf_doc = {word: tf[word] * idf[word] for word in tf}
        tfidf.append(tfidf_doc)
    return tfidf

# Główna funkcja przetwarzająca
def process_documents_and_queries():
    lemmatization_url = "https://lewoniewski.info/diffs.txt"
    lemmatization_dict = load_lemmatization_dict(lemmatization_url)

    n = int(input("Podaj liczbę dokumentów: ").strip())
    documents = []
    for _ in range(n):
        title = input("Podaj tytuł dokumentu: ").strip()
        content = input("Podaj treść dokumentu: ").strip()
        # Tokenizacja i lematyzacja
        title_tokens = tokenize_and_lemmatize(title, lemmatization_dict)
        content_tokens = tokenize_and_lemmatize(content, lemmatization_dict)
        documents.append((title_tokens, content_tokens))  # Przechowujemy osobno tytuł i treść

    m = int(input("Podaj liczbę zapytań: ").strip())
    queries = []
    for _ in range(m):
        query = input("Podaj zapytanie: ").strip()
        queries.append(tokenize_and_lemmatize(query, lemmatization_dict))

    # Obliczanie TF-IDF
    tfidf = compute_tfidf([title + content for title, content in documents])

    # Przetwarzanie zapytań
    results = []
    for query in queries:
        scores = []
        for idx, (title_tokens, content_tokens) in enumerate(documents):
            # Sprawdzanie, czy zapytanie zawiera jakiekolwiek słowo w tytule lub treści
            if any(term in title_tokens or term in content_tokens for term in query):
                score = sum(tfidf[idx].get(term, 0) * 2 for term in query)  # Waga 2x dla tytułu
                scores.append((idx, score))

        # Sortowanie według wyniku
        scores.sort(key=lambda x: (-x[1], x[0]))  # Sortuj malejąco po score, a rosnąco po indeksie
        results.append([idx for idx, score in scores if score > 0])  # Tylko dokumenty z dodatnim wynikiem

    # Wyświetlanie wyników
    for result in results:
        print(result)

# Uruchomienie programu
if __name__ == "__main__":
    process_documents_and_queries()
