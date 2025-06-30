import jwt
from datetime import datetime, timedelta
from bcrypt import gensalt,hashpw
import bcrypt


from src.config.settings import jwt_config



def encode_jwt(
        payload: dict,
        private_key: str = jwt_config.secret_key,
        algorithm: str = jwt_config.algorithm,
        expire_minutes: int = jwt_config.expire
    ):
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=int(expire_minutes))
    to_encode.update({'exp' : expire})
    encoded = jwt.encode(to_encode,private_key,algorithm=algorithm)
    return encoded

def decode_jwt(
    token: str | bytes,
    public_key: str = jwt_config.secret_public_key,
    algorithm: str = jwt_config.algorithm
):
    decoded = jwt.decode(token,public_key,algorithms=[algorithm])
    return decoded




def hash_password(password: str) -> bytes:
    return  hashpw(password = password.encode(),salt = gensalt())

def validate_password(
        password: str,
        hash_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hash_password
)




