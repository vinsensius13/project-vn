import MeCab

wakati = MeCab.Tagger("-Owakati")
mecab = MeCab.Tagger("-Ochasen")

def tokenize_text(text):
    """
    Tokenisasi kalimat Jepang → list kata.
    """
    return wakati.parse(text).strip().split()

def analyze_grammar(text):
    """
    Analisis grammar dengan MeCab.
    Output: list format "kata (POS)"
    """
    parsed_result = []
    node = mecab.parseToNode(text)
    while node:
        surface = node.surface
        features = node.feature.split(",")
        pos = features[0] if features else "Unknown"
        parsed_result.append(f"{surface} ({pos})")
        node = node.next
    return parsed_result 