# whisper_normalizer

> A python package for text standardisation/normalization. It uses
> normalization algorithm mentioned in OpenAI whisper paper. Using
> Whisper normalization can cause issues in Indic languages and other
> low resource languages when using
> [`BasicTextNormalizer`](https://kurianbenoy.github.io/whisper_normalizer/basic.html#basictextnormalizer).
> So normalization in Indic languages is also implemented in this
> package which was derived from
> [indic-nlp-library](https://github.com/anoopkunchukuttan/indic_nlp_library).


[![PyPI Downloads](https://static.pepy.tech/personalized-badge/whisper-normalizer?period=total&units=NONE&left_color=BLACK&right_color=ORANGE&left_text=downloads)](https://pepy.tech/projects/whisper-normalizer)
[![Github
license](https://img.shields.io/github/license/kurianbenoy/whisper_normalizer.svg)](https://github.com/kurianbenoy/whisper_normalizer/blob/main/LICENSE)
[![Github
Stars](https://img.shields.io/github/stars/kurianbenoy/whisper_normalizer.svg?colorA=orange&colorB=orange&logo=github)](https://github.com/kurianbenoy/whisper_normalizer/stargazers)
[![PyPI
version](https://img.shields.io/pypi/v/whisper-normalizer.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/whisper-normalizer/)
<!-- [![Downloads](https://static.pepy.tech/badge/whisper-normalizer)](https://github.com/kurianbenoy/whisper_normalizer) -->
<!-- [![python version](https://img.shields.io/badge/Python-%3E=3.7-blue)](https://github.com/kurianbenoy/whisper_normalizer)
[![python version](https://img.shields.io/badge/Python-<3.12-blue)](https://github.com/kurianbenoy/whisper_normalizer) -->

This package is a python implementation of the text
standardisation/normalization approach which is being used in OpenAI
whisper. The code was originally being released as open-source in
[Whisper source code](https://github.com/openai/whisper). More details
about the text normalization approach used by whisper can be found on
Appendix Section C pp.21 the paper [Robust Speech Recognition via
Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf)
by OpenAI team.

## Installation of package

``` sh
pip install whisper_normalizer
```

or from github repository

``` sh
pip install git+https://github.com/kurianbenoy/whisper_normalizer.git
```

## How to use the package

- I made a video walk through on how to use the `whisper_normalizer` python package.

[Colab Notebook Link of walk
through](https://colab.research.google.com/gist/kurianbenoy/7d27d9ec193a4a97ec7821235bddc506/hello-world_whisper_normalizer.ipynb)

[Github Gist Link of walk
through](https://gist.github.com/kurianbenoy/7d27d9ec193a4a97ec7821235bddc506)

[![](https://img.youtube.com/vi/c7trf0zul6g/0.jpg)](https://www.youtube.com/watch?v=c7trf0zul6g)

## Why should we normalize/standardize text?

- In ASR systems it’s important to normalize the text to reduce
  unintentional penalties in metrics like WER, CER etc.
- Text normalization/standardization is process of converting texts in
  different styles into a standardized form, which is a best-effort
  attempt to penalize only when a word error is caused by actually
  mistranscribing a word, and not by formatting or punctuation
  differences.(from [Whisper
  paper](https://cdn.openai.com/papers/whisper.pdf))

## Why use this python package?

This package is a python implementation of the text
standardisation/normalization approach which is being used in OpenAI
whisper text normalizer. If you want to use just text normalization
alone, it’s better to use this instead reimplementing the same thing.
OpenAI approach of text normalization is very helpful and is being used
as normalization step when evaluating competitive models like
[AssemblyAI Conformer-1
model](https://www.assemblyai.com/blog/conformer-1/).

## Models evaluated using Whisper normalization

- OpenAI Whisper
- Massively Multilingual Speech (MMS) models by Meta
- Conformer 1 by AssemblyAI
- Conformer 2 by AssemblyAI

## How to use

OpenAI open source approach of text normalization/standardization is
mentioned in detail Appendix Section C pp.21 the paper [Robust Speech
Recognition via Large-Scale Weak
Supervision](https://cdn.openai.com/papers/whisper.pdf).

Whisper Normalizer by default comes with two classes
[`BasicTextNormalizer`](https://kurianbenoy.github.io/whisper_normalizer/basic.html#basictextnormalizer)
and
[`EnglishTextNormalizer`](https://kurianbenoy.github.io/whisper_normalizer/english.html#englishtextnormalizer)

You can use the same thing in this package as follows:

``` python
from whisper_normalizer.english import EnglishTextNormalizer

english_normalizer = EnglishTextNormalizer()
english_normalizer("I'm a little teapot, short and stout. Tip me over and pour me out!")
```

    'i am a little teapot short and stout tip me over and pour me out'

``` python
from whisper_normalizer.basic import BasicTextNormalizer

normalizer = BasicTextNormalizer()
normalizer("I'm a little teapot, short and stout. Tip me over and pour me out!")
```

    'i m a little teapot short and stout tip me over and pour me out '

## Using BasicTextNormalizer in your mother tongue might be a bad idea

Whisper Text Normalizer is not always recommended to be used. [Dr Kavya
Manohar](https://www.linkedin.com/in/kavya-manohar/) has written a
blogpost on why it might be a bad idea on her [blopost titled Indian
Languages and Text Normalization: Part
1](https://kavyamanohar.com/post/indic-normalizer/).

## This model extends Whisper_normalizer to support Indic languages as well.

The logic for normalization in Indic languages is derived from
[indic-nlp-library](https://github.com/anoopkunchukuttan/indic_nlp_library).
The logic for Malayalam normalization is expanded beyond the Indic NLP
library by
[`MalayalamNormalizer`](https://kurianbenoy.github.io/whisper_normalizer/1b.indic_normalizer.html#malayalamnormalizer).

``` python
from whisper_normalizer.indic_normalizer import MalayalamNormalizer

normalizer = MalayalamNormalizer()
normalizer("എന്റെ കമ്പ്യൂട്ടറിനു് എന്റെ ഭാഷ.")
```

    'എന്റെ കമ്പ്യൂട്ടറിന് എന്റെ ഭാഷ.'
