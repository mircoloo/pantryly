"""
Helper per l'hashing delle password con bcrypt.

Regole di sicurezza:
  - Non loggare MAI password in chiaro o hash nei log.
  - Usare sempre bcrypt (adaptive hashing) per resistenza al brute-force.
"""
from bcrypt import checkpw, hashpw, gensalt


class HashHelper:
    """Utility stateless per hashing e verifica password."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Confronta la password in chiaro con il suo hash bcrypt."""
        return checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )

    @staticmethod
    def get_password_hash(plain_password: str) -> str:
        """Genera un hash bcrypt dalla password in chiaro."""
        return hashpw(
            plain_password.encode("utf-8"),
            gensalt(),
        ).decode("utf-8")