from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from typing import List, Optional, Any, Union, Dict
from enum import Enum
from whisper_normalizer.english import EnglishTextNormalizer
from whisper_normalizer.basic import BasicTextNormalizer
from whisper_normalizer.indic import DevanagariNormalizer
from whisper_normalizer.indic import HindiNormalizer
from whisper_normalizer.indic import PunjabiNormalizer
from whisper_normalizer.indic import TeluguNormalizer
from whisper_normalizer.indic import GujaratiNormalizer
from whisper_normalizer.indic import OdiaNormalizer
from whisper_normalizer.indic import BengaliNormalizer
from whisper_normalizer.indic import TamilNormalizer
from whisper_normalizer.indic import KannadaNormalizer
from whisper_normalizer.indic import MalayalamNormalizer

class LanguageCodes(str, Enum):
    ENGLISH = 'en'
    BASIC = 'basic'
    DEVANAGARI = 'hi'
    HINDI = 'hi'
    PUNJABI = 'pa'
    TELUGU = 'te'
    GUJARATI = 'gu'
    ODIYA = 'or'
    BENGALI = 'bn'
    TAMIL = 'ta'
    KANNADA = 'kn'
    MALAYALAM = 'ml'

LANGUAGE_NORMALIZER_MAP = {
    LanguageCodes.ENGLISH: EnglishTextNormalizer,
    LanguageCodes.BASIC: BasicTextNormalizer,
    LanguageCodes.HINDI: HindiNormalizer,
    LanguageCodes.BENGALI: BengaliNormalizer,
    LanguageCodes.TAMIL: TamilNormalizer,
    LanguageCodes.TELUGU: TeluguNormalizer,
    LanguageCodes.KANNADA: KannadaNormalizer,
    LanguageCodes.MALAYALAM: MalayalamNormalizer,
    LanguageCodes.PUNJABI: PunjabiNormalizer,
    LanguageCodes.GUJARATI: GujaratiNormalizer,
    LanguageCodes.ODIYA: OdiaNormalizer,
    LanguageCodes.DEVANAGARI: DevanagariNormalizer,
}


class NasalsModeEnum(str, Enum):
    DO_NOTHING = "do_nothing" #default
    TO_ANUSVAARA_STRICT = "to_anusvaara_strict"
    TO_ANUSVAARA_RELAXED = "to_anusvaara_relaxed"
    TO_NASAL_CONSONANTS = "to_nasal_consonants"  


class BasicNormalizerOptions(BaseModel):
    remove_diacritics: bool = False
    split_letters: bool = False

class IndicNormalizerOptions(BaseModel):
    remove_nuktas: bool = False
    nasals_mode: NasalsModeEnum = NasalsModeEnum.DO_NOTHING
    do_normalize_chandras: bool = False
    do_normalize_vowel_ending: bool = False
    tts_mode: bool = False
    
class BengaliNormalizerOptions(IndicNormalizerOptions):
    do_remap_assamese_chars: bool = False

class PunjabiNormalizerOptions(IndicNormalizerOptions):
    do_canonicalize_addak: bool = False
    do_canonicalize_tippi: bool = False
    do_replace_vowel_bases: bool = False

class OdiaNormalizerOptions(IndicNormalizerOptions):
    do_remap_wa: bool = False

Normalisation_Options = Union[BasicNormalizerOptions, IndicNormalizerOptions, BengaliNormalizerOptions, PunjabiNormalizerOptions, OdiaNormalizerOptions]


from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional

class TextNormalisationRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'text': 'Hello, world!',
                'language': 'en'
            }
        }
    )
    
    text: str
    language: LanguageCodes
    options: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Options for normalization. For English: leave empty/null. For other languages: check GET /options/{language}",
        example=None  # This explicitly sets the example to null
    )

class TextNormalisationResponse(BaseModel):
    normalized_text: str
    language_used : str
    options_used: Optional[dict]  =  None 

def get_normalizer(language: LanguageCodes, options: Optional[dict] = None):
    if language not in LANGUAGE_NORMALIZER_MAP:
        raise HTTPException(status_code=400, detail="Invalid language codes. Supported Languages are: " + ", ".join(LANGUAGE_NORMALIZER_MAP.keys()))
    
    normalizer_class = LANGUAGE_NORMALIZER_MAP[language]

    if not options:
        return normalizer_class()
    
    try:

        if language == LanguageCodes.ENGLISH:
            if options is not None:
                raise HTTPException(status_code=400, detail="English normalizer does not take any options")
            return normalizer_class()

        elif language == LanguageCodes.BASIC: 
            validated_options = BasicNormalizerOptions(**options)
            return normalizer_class(**validated_options.model_dump())
        
        elif language == LanguageCodes.BENGALI:
                validated_options = BengaliNormalizerOptions(**options)
                return normalizer_class(**validated_options.model_dump())
                
        elif language == LanguageCodes.PUNJABI:
            validated_options = PunjabiNormalizerOptions(**options)
            return normalizer_class(**validated_options.model_dump())
                
        elif language == LanguageCodes.ODIYA:
            validated_options = OdiaNormalizerOptions(**options)
            return normalizer_class(**validated_options.model_dump())
                
        else:
            validated_options = IndicNormalizerOptions(**options)
            return normalizer_class(**validated_options.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid options for {language.value} normalizer: {str(e)}")
    


        

app = FastAPI()
@app.get("/")
def welcome_message()->str:
    return "Welcome to the Text Normalization API"

@app.get('/example')
def get_example_requests() -> dict:
    """Get example requests for different languages"""
    return {
        "examples": [
            {
                "description": "English (no options needed)",
                "request": {
                    "text": "Hello, world!",
                    "language": "en"
                }
            },
            {
                "description": "Basic normalizer with options",
                "request": {
                    "text": "Café naïve",
                    "language": "basic",
                    "options": {
                        "remove_diacritics": True,
                        "split_letters": False
                    }
                }
            },
            {
                "description": "Hindi with TTS mode",
                "request": {
                    "text": "नमस्ते दुनिया 123 रुपये",
                    "language": "hi",
                    "options": {
                        "tts_mode": True,
                        "nasals_mode": "to_anusvaara_relaxed"
                    }
                }
            }
        ],
        "tip": "Use GET /options/{language} to see all available options for any language"
    }

@app.get('/languages')
def get_supported_languages() -> dict:
    return {
        "supported_languages": [
            {"code": lang.value, "name": lang.name} for lang in LanguageCodes
        ]
    }

@app.post('/normalize',response_model=TextNormalisationResponse)
def normalize_text(request: TextNormalisationRequest) -> TextNormalisationResponse:

    try:
        normalizer = get_normalizer(request.language , request.options)
        normalized_text = normalizer(request.text)
        return TextNormalisationResponse(normalized_text=normalized_text, language_used=request.language.value, options_used= request.options)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/nasals_modes')
def get_nasals_modes() -> dict:
    """Get available nasals_mode options with descriptions"""
    return {
        "nasals_mode_options": [
            {
                "value": NasalsModeEnum.DO_NOTHING,
                "description": "No nasal normalization (default)"
            },
            {
                "value": NasalsModeEnum.TO_ANUSVAARA_STRICT,
                "description": "Convert nasal consonants to anusvaara (strict rules)"
            },
            {
                "value": NasalsModeEnum.TO_ANUSVAARA_RELAXED,
                "description": "Convert nasal consonants to anusvaara (relaxed rules)"
            },
            {
                "value": NasalsModeEnum.TO_NASAL_CONSONANTS,
                "description": "Convert anusvaara to nasal consonants"
            }
        ]
    }

@app.get('/options/{language}')
def get_language_options(language: LanguageCodes) -> dict:
    
    option_schemas = {
        LanguageCodes.BASIC: BasicNormalizerOptions.model_json_schema(),
        LanguageCodes.ENGLISH: {"message": "EnglishTextNormalizer takes no additional options"},
        LanguageCodes.BENGALI: BengaliNormalizerOptions.model_json_schema(),
        LanguageCodes.PUNJABI: PunjabiNormalizerOptions.model_json_schema(),
        LanguageCodes.ODIYA: OdiaNormalizerOptions.model_json_schema(),
    }
    
    # For other Indic languages, use common options
    if language not in option_schemas:
        return {
            "language": language.value,
            "available_options": IndicNormalizerOptions.model_json_schema()
        }
    
    return {
        "language": language.value,
        "available_options": option_schemas[language]
    }