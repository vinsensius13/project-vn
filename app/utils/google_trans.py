import requests

def translate_google(text, target_lang):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={text}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()[0][0][0]
    except Exception:
        return text
