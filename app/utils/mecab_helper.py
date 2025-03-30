import MeCab

wakati = MeCab.Tagger("-Owakati")
grammar = MeCab.Tagger("")

def tokenize_text(text):
    return wakati.parse(text).strip().split()

def analyze_grammar(text):
    result = []
    parsed = grammar.parse(text)
    for line in parsed.split("\n"):
        if "\t" in line:
            word, details = line.split("\t")
            pos = details.split(",")[0]
            result.append(f"{word} ({pos})")
    return result
