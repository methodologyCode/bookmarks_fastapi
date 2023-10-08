import validators
from fastapi import FastAPI, HTTPException, status

from service import InfoHelper
from utils import FailedRequestApi

app = FastAPI()


@app.get("/")
def get_info_page(url):
    if not validators.url(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email syntax"s not valid')
    try:
        data = InfoHelper(url).get_info()
        return data
    except FailedRequestApi:
        return {'response': 'Сервис не доступен'}

