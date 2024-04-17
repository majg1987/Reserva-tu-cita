from fastapi import APIRouter, HTTPException, status, Depends
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from db.models.user import User, UserInDB
from db.schemas.user import user_schema
from db.client import db_client

load_dotenv()

SECRET = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_DURATION = 30


router = APIRouter(prefix="/user",
                   tags=["user"],
                   responses={404: {"message": "Not Found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def search_user(field: str, key):
    print("buscando usuario")
    try: 
        user = db_client.user.find_one({field: key})
        return User(**user_schema(user))
    
    except:
        return {"error": "No se ha encontrado al usuario"}
    
def search_user_in_DB(field: str, key):
    try: 
        user = db_client.user.find_one({field: key})
        return UserInDB(**user_schema(user))
    
    except:
        return {"error": "No se ha encontrado al usuario"}
    
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación no válidas",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try: 
        email = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if email is None:
            raise exception
    
    except JWTError:
        raise exception
    
    return search_user("email", email)

    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario Inactivo"
        )
    return user


@router.post("/", response_model=object, status_code=status.HTTP_201_CREATED)
async def add_user(user: UserInDB):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Usuario ya existente"
        )
    
    user_dict = dict(user)

    encrypted_password =  pwd_context.hash(user_dict["password"]) 
    user_dict["password"] = encrypted_password    

    del user_dict["id"]


    id = db_client.user.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.user.find_one({"_id": id}))
    return {"message": "Usuario registrado correctamente"}

@router.post("/login", response_model=object, status_code=status.HTTP_202_ACCEPTED)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = search_user_in_DB("username", form.username)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Este Usuario no esta registrado"
        )
    
    if not pwd_context.verify(form.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password Incorrecto"
        )
    
    access_token = {
        "sub": user_db.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer"
    }

@router.get("/me")
async def me(user: User = Depends(current_user)):
    return user