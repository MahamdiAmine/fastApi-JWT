import logging

from fastapi import FastAPI, HTTPException, Security, Depends
from sqlalchemy.orm import Session

from auth.auth_handler import Auth
from auth.auth_bearer import JWTBearer
from models.user import AuthModel

from database import get_db
from services import get_user, create_user

app = FastAPI()

auth_handler = Auth()
auth_required = [Depends(JWTBearer())]


@app.post('/signup', tags=["public access"])
def signup(user_details: AuthModel, db: Session = Depends(get_db)):
    if get_user(db, user_details.email) is not None:
        return 'Account already exists'
    try:
        user_details.password = auth_handler.encode_password(user_details.password)
        return create_user(db, user_details)
    except Exception as e:
        logging.error(e)
        error_msg = 'Failed to signup user'
        return error_msg


@app.post('/login', tags=["public access"])
def login(user_details: AuthModel, db: Session = Depends(get_db)):
    user = get_user(db, user_details.email)
    if user is None:
        return HTTPException(status_code=401, detail='Invalid email')
    if not auth_handler.verify_password(user_details.password, user.password):
        return HTTPException(status_code=401, detail='Invalid password')

    return {
        'access_token': auth_handler.encode_token(user.email),
        'refresh_token': auth_handler.encode_refresh_token(user.email)
    }


@app.get('/refresh_token', dependencies=auth_required, tags=["restricted access"])
def refresh_token(refresh_token: str):
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}


@app.post('/secret', dependencies=auth_required, tags=["restricted access"])
def secret_data():
    return 'you are authorised to use this endpoint'


@app.get('/public', tags=["public access"])
def not_secret_data():
    return 'No auth is required for this'


