import base64
import json
from datetime import datetime
from io import BytesIO

import qrcode
from cryptography.fernet import Fernet
from num2words import num2words


def encrypt_text(text: str, key: str) -> str:
    cipher = Fernet(key.encode())
    encrypted_text = cipher.encrypt(text.encode())
    return encrypted_text.decode()


def generate_qr_base64(data: str) -> str:
    qr = qrcode.make(data)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def amount_to_words(amount):
    """Convert numeric amount to Spanish words."""
    whole_part = int(amount)
    fractional_part = round((amount - whole_part) * 100)  # Get cents

    words = num2words(whole_part, lang='es').capitalize() + " nuevos soles"
    if fractional_part > 0:
        words += f" y {num2words(fractional_part, lang='es')} centavos"

    return words


def choose_period(period_file):
    with open(period_file, 'r', encoding='utf-8') as f:
        period_data = json.load(f)

    periods = period_data["periods"]
    if not periods:
        raise ValueError("❌ No periods found")

    print("📅 Available periods:")
    for period in periods:
        print(f"🌟 {period['id']}: {period['label']}")

    while True:
        chosen_period = input("📝 Enter the desired period ID (or press Enter for the latest): ").strip()
        if not chosen_period:
            return periods[-1]["id"]
        if any(p["id"] == chosen_period for p in periods):
            return chosen_period
        print("⚠️ Invalid period ID. Please try again.")


def calculate_payments(meta_file: str, period_file: str, period: str = None):
    # Read JSON files
    with open(meta_file, 'r', encoding='utf-8') as f:
        meta_data = json.load(f)
    with open(period_file, 'r', encoding='utf-8') as f:
        period_data = json.load(f)

    # Get the last period from the list
    if not period_data["periods"]:
        raise ValueError("No periods found")

    if period:
        period_info = next((p for p in period_data["periods"] if p["id"] == period), None)
        if not period_info:
            raise ValueError(f"Period with id {period} not found")
    else:
        period_info = period_data["periods"][-1]

    period_id = period_info["id"]
    period_name = period_info["label"]

    # Sum common and other expenses
    total_commons = sum(item["total"] for item in period_info.get("commons", []))
    total_others = sum(item["total"] for item in period_info.get("others", []))
    total_expenses = total_commons + total_others

    # Get total apartments and security cost
    total_apartments = len(meta_data["apartments"])
    total_security = period_info.get("security", 0)
    security_per_apartment = round(total_security / total_apartments, 2) if total_apartments else 0

    # Extract expenses details
    commons_expenses = [
        {"concept": meta_data["services"].get(item["concept"], {}).get("shortLabel", item["concept"]),
         "total": item["total"]}
        for item in period_info.get("commons", [])
    ]
    others_expenses = [
        {"concept": item["concept"], "total": item["total"]}
        for item in period_info.get("others", [])
    ]

    # Calculate costs per apartment
    results = []
    total_apt_security = 0
    total_apt_expenses = 0
    total_apt = 0
    for apartment in meta_data["apartments"]:
        factor = apartment["percentage"] / 100
        apartment_expenses = factor * total_expenses
        total_payment = apartment_expenses + security_per_apartment

        total_apt_expenses += apartment_expenses
        total_apt_security += security_per_apartment
        total_apt += total_payment

        results.append({
            "id": apartment["id"],
            "name": apartment["name"],
            "percentage": apartment["percentage"],
            "total_expenses": round(apartment_expenses, 2),
            "total_security": round(security_per_apartment, 2),
            "total": round(total_payment, 2)
        })

    total_commons = sum(item["total"] for item in commons_expenses)
    total_others = sum(item["total"] for item in others_expenses)

    total_expenses = round(total_commons + total_others, 2)

    return {
        "date": datetime.today().strftime('%d/%m/%Y'),
        "period_id": period_id,
        "period_name": period_name,
        "payments": results,
        "expenses": {
            "commons": commons_expenses,
            "others": others_expenses
        },
        "totals": {
            "total_apt_expenses": round(total_apt_expenses, 2),
            "total_apt_security": round(total_apt_security, 2),
            "total_apt": round(total_apt, 2),
            "total_security": total_security,
            "total_expenses": total_expenses,
            "total": round(total_security + total_expenses, 2)
        }
    }
