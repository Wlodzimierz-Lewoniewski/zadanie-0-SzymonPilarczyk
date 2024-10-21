import string
import re
from collections import defaultdict

# Przygotowanie do usuwania interpunkcji i białych znaków
p = string.punctuation  # ciąg wszystkich znaków interpunkcyjnych

# ILE ZDAŃ
n = int(input("Podaj ilość zdań: "))
documents = []

for i in range(n):
    document = input(f"Wprowadź {i + 1} zdanie: ")
    documents.append(document)

# Ilość słów do policzenia
m = int(input("Podaj ilość słów, które chcesz policzyć: "))
count_words = []

for i in range(m):
    word = input(f"Podaj {i + 1} słowo do policzenia: ").lower()  # Zbieramy słowa do policzenia
    count_words.append(word)

# Inicjalizujemy wyniki dla zliczeń
results = defaultdict(lambda: [0] * n)  # Użycie defaultdict

# Zliczanie wystąpień słów w każdym zdaniu
for i in range(n):
    # Usuwamy znaki interpunkcyjne i dzielimy na słowa
    cleaned_document = re.sub(f"[{re.escape(p)}]", " ", documents[i].lower())
    words = cleaned_document.split()  # Dzielimy zdanie na słowa

    # Zliczamy wystąpienia dla każdego z zadanych słów
    for word in count_words:
        results[word][i] = words.count(word)  # Przechowujemy liczbę wystąpień w odpowiednim zdaniu

# Przygotowanie wyników do wyświetlenia
for word in count_words:
    counts = results[word]
    ranking = [i for i in range(n) if counts[i] > 0]  # Generujemy ranking tylko dla zdań, które zawierają słowo
    ranking.sort(key=lambda i: (-counts[i], i))  # Sortujemy po liczbie i zachowujemy kolejność
    print(ranking)  # Wyświetlamy ranking
