import sys
from fast_langdetect import detect

# Test samples matching Telegram's 'small' profile (15–45 characters)
TEST_SAMPLES = {
    "en": "Hello, how are you doing today?",
    "fr": "Bonjour, comment ça va aujourd'hui?",
    "hi": "नमस्ते, आप आज कैसे हैं?",
    "mr": "नमस्कार, तुम्ही कसे आहात आज?",
    "ta": "வணக்கம், நீங்கள் இன்று எப்படி இருக்கிறீர்கள்?",
    "ar": "مرحبا، كيف حالك اليوم؟"
}

print("=" * 70)
print("🔍 FAST_LANGDETECT OUTPUT STRUCTURE DIAGNOSTIC")
print("=" * 70)
print(f"Python version: {sys.version}\n")

for lang, text in TEST_SAMPLES.items():
    print(f"Target Language : {lang.upper()}")
    print(f"Input Text      : '{text}'")
    
    try:
        # Running standard auto model inference
        raw_output = detect(text, model="auto")
        
        print(f"RAW Output      : {raw_output}")
        print(f"Output Type     : {type(raw_output)}")
        
        # Checking inner elements if it's a collection
        if isinstance(raw_output, list):
            if len(raw_output) > 0:
                print(f"First Element   : {raw_output[0]}")
                print(f"Element Type    : {type(raw_output[0])}")
        elif isinstance(raw_output, dict):
            print(f"Dictionary Keys : {list(raw_output.keys())}")
            
    except Exception as e:
        print(f"❌ Execution Error: {str(e)}")
        
    print("-" * 70)

print("=" * 70)
print("Please run this script and paste the printed console block back here.")
print("=" * 70)

# samples of what output it gives : 
# ======================================================================
# 🔍 FAST_LANGDETECT OUTPUT STRUCTURE DIAGNOSTIC
# ======================================================================
# Python version: 3.13.9 (tags/v3.13.9:8183fa5, Oct 14 2025, 14:09:13) [MSC v.1944 64 bit (AMD64)]

# Target Language : EN
# Input Text      : 'Hello, how are you doing today?'
# RAW Output      : [{'lang': 'en', 'score': 0.9919968843460083}]
# Output Type     : <class 'list'>
# First Element   : {'lang': 'en', 'score': 0.9919968843460083}
# Element Type    : <class 'dict'>
# ----------------------------------------------------------------------
# Target Language : FR
# Input Text      : 'Bonjour, comment ça va aujourd'hui?'
# RAW Output      : [{'lang': 'fr', 'score': 0.9857398867607117}]
# Output Type     : <class 'list'>
# First Element   : {'lang': 'fr', 'score': 0.9857398867607117}
# Element Type    : <class 'dict'>
# ----------------------------------------------------------------------
# Target Language : HI
# Input Text      : 'नमस्ते, आप आज कैसे हैं?'
# RAW Output      : [{'lang': 'hi', 'score': 0.997143030166626}]
# Output Type     : <class 'list'>
# First Element   : {'lang': 'hi', 'score': 0.997143030166626}
# Element Type    : <class 'dict'>
# ----------------------------------------------------------------------
# Target Language : MR
# Input Text      : 'नमस्कार, तुम्ही कसे आहात आज?'
# RAW Output      : [{'lang': 'mr', 'score': 0.9994868636131287}]
# Output Type     : <class 'list'>
# First Element   : {'lang': 'mr', 'score': 0.9994868636131287}
# Element Type    : <class 'dict'>
# ----------------------------------------------------------------------
# Target Language : TA
# Input Text      : 'வணக்கம், நீங்கள் இன்று எப்படி இருக்கிறீர்கள்?'
# RAW Output      : [{'lang': 'ta', 'score': 1.0}]
# Output Type     : <class 'list'>
# First Element   : {'lang': 'ta', 'score': 1.0}
# Element Type    : <class 'dict'>
# ----------------------------------------------------------------------
# Target Language : AR
# Input Text      : 'مرحبا، كيف حالك اليوم؟'
# RAW Output      : [{'lang': 'ar', 'score': 0.9867990016937256}]
# Output Type     : <class 'list'>
# First Element   : {'lang': 'ar', 'score': 0.9867990016937256}
# Element Type    : <class 'dict'>
# ----------------------------------------------------------------------
# ======================================================================
# Please run this script and paste the printed console block back here.
# ======================================================================

# D:\projects\new_era\z.Tests\groupSailBotLanguageDetectionModule\TEST_1>