import random
import nltk
from nltk.tokenize import WhitespaceTokenizer
import re


class TextGenerator:
    def __init__(self):
        self.tokens = []
        self.bigrams = []
        self.trigrams = []
        self.markov = {}
        self.markov_trig = {}

    def tokenize(self):
        with open(input(), "r", encoding="utf-8") as f:
            self.tokens = WhitespaceTokenizer().tokenize(f.read())

    def create_bigrams(self):
        self.bigrams = list(nltk.bigrams(self.tokens))
        # print(f"Number of bigrams: {len(self.bigrams)}")

    def create_trigrams(self):
        trigrams = list(nltk.trigrams(self.tokens))
        for elem in trigrams:
            self.trigrams.append([' '.join(elem[:2]), elem[2]])

    def statistics(self):
        print("Corpus statistics")
        print(f"All tokens: {len(self.tokens)}")
        print(f"Unique tokens: {len(set(self.tokens))}")

    def create_markov(self):
        for head, tail in self.bigrams:
            self.markov.setdefault(head, {})
            self.markov[head].setdefault(tail, 0)
            self.markov[head][tail] += 1
        for head in self.markov:
            self.markov[head] = dict([elem[::-1] for elem in sorted([(value, key) for (key, value) in self.markov[head].items()], reverse=True)])

    def create_markov_trigrams(self):
        for head, tail in self.trigrams:
            self.markov_trig.setdefault(head, {})
            self.markov_trig[head].setdefault(tail, 0)
            self.markov_trig[head][tail] += 1

    def generate_sentences(self):
        def gen_sentence():
            sentence = []
            first = [token for token in self.tokens if re.match(r"^[A-Z]\w*[^.?!]$", token)]
            word = random.choice(first)
            sentence.append(word)
            iters = 1
            while iters < 4 or not any([re.match(r"\w*[.!?]$", tail) for tail in self.markov[word]]):
                new_word = random.choices(list(self.markov[word].keys()), weights=self.markov[word].values())
                sentence.append(new_word[0])
                word = new_word[0]
                iters += 1
            last = [tail for tail in self.markov[word] if re.match(r"\w*[.!?]$", tail)]
            new_word = random.choice(last)
            sentence.append(new_word)
            return sentence

        for _ in range(10):
            print((' ').join(gen_sentence()))

    def generate_sentences_trig(self):
        def gen_sentence():
            sentence = []
            first = [head for head in self.markov_trig.keys() if re.match(r"^[A-Z]\w*[^.?!] \w*[^.?!]$", head)]
            bigram = random.choice(first).split()
            sentence.append(bigram[0])
            sentence.append(bigram[1])
            iters = 1
            while iters < 3 or not any([re.match(r"\w*[.!?]$", tail) for tail in self.markov_trig[' '.join(bigram)]]):
                new_bigram = random.choices(list(self.markov_trig[' '.join(bigram)].keys()), weights=self.markov_trig[' '.join(bigram)].values())
                sentence.append(new_bigram[0])
                bigram[0] = bigram[1]
                bigram[1] = new_bigram[0]
                iters += 1
            last = [tail for tail in self.markov_trig[' '.join(bigram)] if re.match(r"^\w*[.?!]$", tail)]
            new_word = random.choice(last)
            sentence.append(new_word)
            return sentence

        for _ in range(10):
            print((' ').join(gen_sentence()))

    def read_tokens(self):
        while True:
            try:
                command = input()
                if command == "exit":
                    return
                else:
                    number = int(command)
                    print(self.tokens[number])
            except TypeError:
                print("Type Error. Please input an integer")
            except IndexError:
                print("Index Error. Please input an integer that is in the range of the corpus.")
            except ValueError:
                print("Value Error. Could not convert data to an integer.")

    def read_bigrams(self):
        while True:
            try:
                command = input()
                if command == "exit":
                    return
                else:
                    number = int(command)
                    print(f"Head: {self.bigrams[number][0]}\tTail: {self.bigrams[number][1]}")
            except TypeError:
                print("Type Error. Please input an integer")
            except IndexError:
                print("Index Error. Please input a value that is not greater than the number of all bigrams.")
            except ValueError:
                print("Value Error. Could not convert data to an integer.")

    def read_markov(self):
        while True:
            try:
                command = input()
                if command == "exit":
                    return
                else:
                    print(f"Head: {command}")
                    for key, value in self.markov[command].items():
                        print(f"Tail: {key} Count: {value}")
            except TypeError:
                print("Type Error. Please input an integer")
            except IndexError:
                print("Index Error. Please input a value that is not greater than the number of all bigrams.")
            except ValueError:
                print("Value Error. Could not convert data to an integer.")
            except KeyError:
                print("Key Error. The requested word is not in the model. Please input another word.")


text_gen = TextGenerator()
text_gen.tokenize()
# text_gen.create_bigrams()
# text_gen.read_bigrams()
# text_gen.create_markov()
# text_gen.read_markov()
# text_gen.generate_sentences()
text_gen.create_trigrams()
text_gen.create_markov_trigrams()
text_gen.generate_sentences_trig()

