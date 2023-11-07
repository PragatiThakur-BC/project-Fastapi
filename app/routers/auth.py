from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schema, models, services, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# "python-jose[cryptography]" we need this to work with JWT
router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schema.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # This is how the request form will store the data username can be anything here!
    # {
    #     "username": "asdf",
    #     "password": "alsdjf"
    # }
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    if not services.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Creating token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


