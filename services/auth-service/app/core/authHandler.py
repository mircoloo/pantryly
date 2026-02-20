"""
Handler JWT per il servizio di autenticazione.

Si occupa di:
  - Generare token JWT firmati con HS256 (sign_jwt).
  - Decodificare e validare token JWT (decode_jwt).

Il claim standard 'sub' (subject) contiene l'id dell'utente,
in linea con le specifiche JWT (RFC 7519) e con la validazione
effettuata dal Gateway.
"""
from datetime import datetime, timedelta, timezone

from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import config

# Configurazione JWT caricata dalle variabili d'ambiente
JWT_SECRET = config.JWT_SECRET
JWT_ALGORITHM = config.JWT_ALGORITHM
JWT_EXPIRATION_TIME = config.JWT_EXPIRATION_TIME  # minuti


class AuthHandler:
    """Utility stateless per la gestione dei token JWT."""

    @staticmethod
    def sign_jwt(user_id: int) -> str:
        """
        Genera un JWT con il claim 'sub' (subject) = user_id.

        Il token scade dopo JWT_EXPIRATION_TIME minuti.
        """
        expiration = datetime.now(timezone.utc) + timedelta(
            minutes=JWT_EXPIRATION_TIME
        )
        payload = {
            # 'sub' è il claim standard per identificare il soggetto del token
            "sub": str(user_id),
            "exp": expiration,
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_jwt(token: str) -> dict:
        """
        Decodifica un JWT e restituisce il payload.

        Ritorna un dict con chiave 'error' se il token è scaduto o non valido.
        """
        try:
            return jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
            )
        except ExpiredSignatureError:
            return {"error": "Token has expired"}
        except JWTError:
            return {"error": "Invalid token"}
        