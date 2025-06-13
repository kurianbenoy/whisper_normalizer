from pydantic import BaseModel 
from fastapi import FastAPI, HTTPException
from typing import List, Optional, Any 
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

app = FastAPI()
@app.post("/")
def welcome_message()->str:
    return "Welcome to the Text Normalization API"


