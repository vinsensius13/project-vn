from flask import Blueprint, request, Response
import json
from langdetect import detect
from app.utils.google_trans import translate_google  # Updated import
from app.utils.flan_refiner import refine_japanese
from app.utils.mecab_helper import tokenize_text, analyze_grammar

router = Blueprint('main', __name__)

@router.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    target_lang = data.get("target", "ja")
    refine = data.get("refine", True)  # Allow user to control refine

    # Ganti translate_google ke translate_facebook
    translated = translate_google(text, target_lang) or text

    # Refine hanya jika target bahasa Jepang dan input emang Jepang
    if target_lang == "ja" and refine and detect(translated) == "ja":
        translated = refine_japanese(translated) or translated

    # Safety check
    if not isinstance(translated, str):
        return Response(
            json.dumps({"error": "Translation failed"}, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        ), 500

    # Tokenizer & Grammar → hanya kalau teks JAPANESE
    if detect(translated) == "ja":
        tokens = tokenize_text(translated)
        grammar = analyze_grammar(translated)
    else:
        tokens = translated.split()
        grammar = []

    return Response(
        json.dumps({
            "original": text,
            "translated": translated,
            "target_lang": target_lang,
            "tokenized": tokens,
            "grammar_analysis": grammar
        }, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )
