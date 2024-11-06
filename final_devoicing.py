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
import json

voiceless = ['p','t','k','f','s','x']
voiced = ['b','d','g','v','z','X']
other = ['m','n','l','r','j','w','h']
consonants = voiceless + voiced + other
vowels = ['a','e','i','o','u','A','E','I','O','U']
voiced_to_voiceless = dict(zip(voiced, voiceless))

def phoneme_dict():
    return {'voiceless': voiceless, 'voiced': voiced, 'other': other, 
        'vowels': vowels, 'consonants': consonants}

def make_syllable(n_onset = 1, n_nucleus = 1, n_coda = 1):
    onset = [random.choice(consonants) for i in range(n_onset)]
    nucleus = [random.choice(vowels) for i in range(n_nucleus)]
    coda = [random.choice(consonants) for i in range(n_coda)]
    return onset + nucleus + coda

def has_coda(syllable):
    return syllable[-1] in consonants

def has_onset(syllable):
    return syllable[0] in consonants

def onset_voiced(syllable):
    if not has_onset(syllable):
        return False
    return syllable[0] in voiced

def coda_voiced(syllable):
    if not has_coda(syllable):
        return False
    return syllable[-1] in voiced

def make_stem(word):
    assert len(word) == 2 
    syllable1, syllable2 = word
    if not has_coda(syllable1) and has_onset(syllable2):
        return syllable1 + [syllable2[0]]
    return word

def make_word_and_stem(enforce_stem_not_equal_to_word = False):
    word = make_word(2)
    stem = make_stem(word)
    if enforce_stem_not_equal_to_word:
        while word == stem:
            word = make_word(2)
            stem = make_stem(word)
    return word, stem

def make_word(n_syllables = 1):
    word = []
    for i in range(n_syllables):
        if i > 0: 
            n_onset= 1
        else:
            n_onset = random.choice([0,1])
        n_coda = random.choice([0,1])
        syllable = make_syllable(n_onset = n_onset, n_coda = n_coda)
        syllable = apply_final_devoicing_syllable(syllable)
        word.append(syllable)
    return word

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

def word_to_string(word):
    return ''.join([''.join(syllable) for syllable in word])

def make_dataset(n_words = 100_000, only_unique_words = True):
    X,y = [],[]
    while len(X) < n_words:
        word, stem = make_word_and_stem(enforce_stem_not_equal_to_word = True)
        y_item = int(syllable_needs_final_devoicing(stem))
        word, stem = word_to_string(word), word_to_string(stem)
        x_item = word+'#'+stem
        if len(X) % 10_000 == 0: print(len(X))
        if only_unique_words and x_item in X:
            continue
        X.append(x_item)
        y.append(y_item)
    return X,y

def save_dataset(X,y, filename = 'final_devoicing.json'):
    d = {'X': X, 'y': y, 'phonemes': phoneme_dict()}
    with open(filename, 'w') as f:
        json.dump(d, f)


