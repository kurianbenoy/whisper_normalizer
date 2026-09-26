from jiwer import wer, cer

asr_output = "I'm a little teapot, short and stout. Tip me over and pour me out!"
ground_truth = "I am a litte teapot, short and stout. tip me over and pour me out."

# **WER  - Word Error Rate**
# **CER - Charater Error Rate**
# ASR evaluation requires - ground truth and ASR output
# WER & CER are calcuated by comparing ground truth and ASR output.
# Both WER & CER - leser is the better
# Accuracy = (1 -WER)*100

print(wer(ground_truth, asr_output))

from whisper_normalizer.english import EnglishTextNormalizer

normalizer = EnglishTextNormalizer()

print(normalizer(asr_output))
print(normalizer(ground_truth))

print(wer(normalizer(ground_truth), normalizer(asr_output)))

## why I don't like BasicTextNormalizer, is because it doesn't work for my mother tongue Malayalam.
from whisper_normalizer.basic import BasicTextNormalizer

n = BasicTextNormalizer()
t = "ഗുണ്ടാവിരുന്നിൽ പങ്കെടുത്ത DySP സാബുവിനെ സസ്‌പെൻഡ് ചെയ്യാൻ നിർദേശം നൽകി മുഖ്യമന്ത്രി"
print(n(t))

# If you need the basic normalizer for Indic or other scripts that use Unicode Mark characters, use BasicTextNormalizer(preserve_marks=True)
n = BasicTextNormalizer(preserve_marks=True)
print(n(t))

# or use Language Specific normalizer like Malayalam
from whisper_normalizer.indic import MalayalamNormalizer

normalizer = MalayalamNormalizer()
print(normalizer(t))
