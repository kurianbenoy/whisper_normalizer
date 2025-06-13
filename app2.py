from typing import Literal, Union, Annotated
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

app = FastAPI()
class CatRequest(BaseModel):
    animal: Literal["cat"]
    meows: int = 5

class DogRequest(BaseModel):
    animal: Literal["dog"] 
    barks: int = 3

TestRequest = Annotated[
    Union[CatRequest, DogRequest],
    Field(discriminator='animal')
]

@app.post("/test")
def test_discriminated(request: TestRequest):
    return request