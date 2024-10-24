''' BOOIJ, G. E. (1995). The phonology of Dutch. 
p22 (33) 
The syllable is the domain of phonological rules
    - final devoicing (Auslautverhaertung)
        obstruents are voiceless at the end of the syllable
In early generative phonological publications on Dutch, 
final devoicing was sometimes formulated as a word-final rule, 
because we only find alternations between voiced and voiceless
obstruents in word-final position
'''


import random

voiceless = ['p','t','k','f','s','x']
voiced = ['b','d','g','v','z','X']
other = ['m','n','l','r','j','w','h']
consonants = voiceless + voiced + other
vowels = ['a','e','i','o','u','A','E','I','O','U']
voiced_to_voiceless = dict(zip(voiced, voiceless))

def make_syllable(n_onset = 1, n_nucleus = 1, n_coda = 1):
    onset = [random.choice(consonants) for i in range(n_onset)]
    nucleus = [random.choice(vowels) for i in range(n_nucleus)]
    coda = [random.choice(consonants) for i in range(n_coda)]
    return onset + nucleus + coda

def make_word(n_syllables = 1):
    for i in range(n_syllables):
        if i != n_syllables - 1:
            syllable = apply_final_devoicing(make_syllable())
    word = [make_syllable() for i in range(n_syllables)]

def syllable_needs_final_devoicing(syllable):
    return syllable[-1] in voiced

def word_needs_final_devoicing(word):
    return any([syllable_needs_final_devoicing(syllable) for syllable in word])

def apply_final_devoicing_syllable(syllable):
    if syllable_needs_final_devoicing(syllable):
        syllable[-1] = voiced_to_voiceless[syllable[-1]]
    return syllable

def apply_final_devoicing_word(word):
    syllables = word
    syllables[-1] = apply_final_devoicing_syllable(syllables[-1])
    return syllables


def make_dataset(n_words = 10_000):
    dataset = []
    for i in range(n_words):
        word = make_word()
        y = int(word_needs_final_devoicing(word))
        dataset.append((word, y))
    return dataset
