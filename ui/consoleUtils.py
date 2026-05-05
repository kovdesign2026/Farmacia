from datetime import datetime
from babel.dates import format_datetime

# Obtiene un prefijo con la hora actual para registrar información
def getLogPrefix () -> str:
    now = datetime.now()
    timestamp = format_datetime(now, locale='es_ES')
    return f"[Farmacia | {timestamp}] - "

# Registra información en la terminal
def log (message: str) -> None:
    print(f"{getLogPrefix()}{message}")