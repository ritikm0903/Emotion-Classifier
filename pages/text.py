import streamlit as st 
import googletrans
from streamlit.components.v1 import html

# HTML for language transition
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Language Transition</title>
<style>
  body {
    margin: 0px;
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 400;
    line-height: 1.6;
    color: rgb(250, 250, 250);
    background-color: rgb(14, 17, 23); /* Background color according to provided information */
    text-size-adjust: 100%;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    -webkit-font-smoothing: auto;
  }
  #word-container {
    position: fixed;
    left: 10px; /* Adjust as per your preference */
    top: 40px; /* Adjust as per your preference */
  }
  #word {
    font-size: 2.8em;
    font-weight: bold;
  }
  .language {
    font-size: 0.6em;
  }
</style>
</head>
<body>

<div id="word-container">
  <div id="word">Hello<span class="language">(English)</span></div>
</div>

<script>
  const wordElement = document.getElementById('word');
  const languages = ['नमस्ते (Hindi)', 'नमस्कार (Marathi)', 'Bonjour (French)', 'こんにちは (Japanese)', 'Hola (Spanish)', 'Hello (English)']; // Adding English as the last language
  let currentLanguageIndex = 0;

  function transitionToNextLanguage() {
    currentLanguageIndex = (currentLanguageIndex + 1) % languages.length;
    const [word, language] = languages[currentLanguageIndex].split(' ');
    wordElement.innerHTML = `${word}<span class="language">${language}</span>`;
  }

  setInterval(transitionToNextLanguage, 1000); // Change language every second

</script>

</body>
</html>
"""

# Display HTML for language transition
st.components.v1.html(html_code)

translator = googletrans.Translator()

def get_key(val):
    for key, value in googletrans.LANGUAGES.items():
        if val == value:
            return key
    return None

# Streamlit components
st.markdown('<style>body{background-color: Blue;}</style>', unsafe_allow_html=True)
option = st.selectbox('Select Language', tuple(googletrans.LANGUAGES.values()), key='language_select')
text = st.text_area('Input the text', key='text_input')
translate_button = st.button("Translate")

# Translation logic
if translate_button:
    if text.strip() and option:
        language_key = get_key(option)
        if language_key:
            translated = translator.translate(text, dest=language_key)
            st.write(translated.text)
        else:
            st.write("Error: Selected language is not valid.")
    else:
        st.write("Error: Input text or selected language is empty.")
