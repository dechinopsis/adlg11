import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("KEY")
if not KEY:
    raise ValueError("La clave 'KEY' no está definida en el archivo .env")


def decrypt_text(encrypted_text: str, key: str) -> str:
    cipher = Fernet(key.encode())
    decrypted_text = cipher.decrypt(encrypted_text.encode())
    return decrypted_text.decode()


if __name__ == "__main__":
    encrypted_text = "gAAAAABnsV7INHATsI9hPusMt7bEBfSdhf8z5QYQwZ9tsmYrlYRneKg9qK5tbZ478dXqkL6PqUmVh1PtodV0TO2DnPTq89RpsQ=="
    decrypted_text = decrypt_text(encrypted_text, KEY)
    print(f'Texto desencriptado: {decrypted_text}')
