"""
Modulo di sicurezza del Gateway.

Responsabilità:
  - Decodifica e validazione dei token JWT emessi dall'auth-service.
  - Esposizione di una dependency FastAPI (`get_current_user`) da iniettare
    nelle rotte protette, così ogni proxy può accedere all'identità
    dell'utente autenticato in modo uniforme.

Claim JWT attesi:
  - "sub" : id numerico dell'utente (stringa)
  - "exp" : timestamp di scadenza (gestito automaticamente da python-jose)
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings

# Schema OAuth2: il client invia il token nell'header
# "Authorization: Bearer <token>"
# tokenUrl punta all'endpoint di login esposto dal Gateway (proxy → auth-service)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency FastAPI che:
      1. Estrae il Bearer token dall'header Authorization.
      2. Decodifica e valida il JWT usando il segreto condiviso.
      3. Restituisce il payload decodificato (dict con almeno 'sub').

    Se il token è assente, scaduto o firmato con un segreto diverso,
    solleva 401 Unauthorized.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token non valido o scaduto",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        # Il claim "sub" contiene l'id utente (standard JWT)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception

