from passlib.context import CryptContext

passwod_context =  CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(plain_password:str)-> str:
    hash = passwod_context.hash(plain_password)
    return hash

def verify_password(plain_password:str, hash: str) -> bool:
    return passwod_context.verify(plain_password, hash)