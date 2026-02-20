"""
Client HTTP per comunicare con l'inventory-service.

Questo modulo permette all'ai-service di recuperare la lista dei prodotti
dall'inventory-service via rete (chiamata servizio-a-servizio).
In Docker, il servizio è raggiungibile tramite il nome del container.
"""
import logging
import os
from typing import List

import httpx

from .. import schemas

logger = logging.getLogger(__name__)

# URL dell'inventory-service (risolto via Docker network in produzione)
BASE_URL = os.environ.get("PRODUCT_SERVICE_URL", "http://inventory-service:8000")


class ProductServiceClient:
    """
    Client per l'inventory-service.

    Usa httpx.AsyncClient per chiamate non bloccanti.
    Ritorna una lista vuota in caso di errore di rete,
    così gli agenti AI possono gestire il caso "nessun prodotto".
    """

    def __init__(self):
        self.base_url = BASE_URL

    async def get_all_products(self) -> List[dict]:
        """
        Recupera tutti i prodotti dall'inventory-service.

        Ritorna una lista di dict (serializzazione JSON nativa)
        per passarli direttamente al prompt degli agenti AI.
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}/v1/products")
                response.raise_for_status()
                return response.json()

            except httpx.RequestError as exc:
                logger.error("Errore di rete verso inventory-service: %s", exc)
                return []
            except httpx.HTTPStatusError as exc:
                logger.error(
                    "inventory-service ha risposto con errore: %s",
                    exc.response.status_code,
                )
                return []
