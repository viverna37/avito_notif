import hmac
import hashlib


def verify_hmac_sha256(raw_body: bytes, secret: str, signature_hex: str | None) -> bool:
    if not secret:
        # если secret не задан — валидацию отключаем
        return True
    if not signature_hex:
        return False
    mac = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature_hex.lower())