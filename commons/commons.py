import base64
import csv
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

    # Extract fixes (adjustments)
    fixes = period_info.get("fixes", {})

    # Calculate costs per apartment
    results = []
    total_apt_security = 0
    total_apt_expenses = 0
    total_apt_adjustments = 0
    total_apt = 0

    for apartment in meta_data["apartments"]:
        apt_id = apartment["id"]
        factor = apartment["percentage"] / 100
        apartment_expenses = factor * total_expenses
        adjustment = fixes.get(apt_id, 0)
        total_payment = apartment_expenses + security_per_apartment
        final_total = total_payment + adjustment

        total_apt_expenses += apartment_expenses
        total_apt_security += security_per_apartment
        total_apt_adjustments += adjustment
        total_apt += final_total

        results.append({
            "id": apt_id,
            "name": apartment["name"],
            "percentage": apartment["percentage"],
            "total_expenses": round(apartment_expenses, 2),
            "total_security": round(security_per_apartment, 2),
            "adjustment": round(adjustment, 2),
            "total": round(final_total, 2)
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
            "total_adjustments": round(total_apt_adjustments, 2),
            "total_apt": round(total_apt, 2),
            "total_security": total_security,
            "total_expenses": total_expenses,
            "total": round(total_security + total_expenses + total_apt_adjustments, 2)
        }
    }


def parse_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [name.strip().lstrip('\ufeff') for name in reader.fieldnames]
        return list(reader)


def calculate_balance_and_movements(data, period):
    previous_balance = 0
    current_balance = 0
    movements = []

    period = int(period.replace('/', ''))

    for row in data:
        date = datetime.strptime(row['Date'], '%d/%m/%y')
        month_year = int(date.strftime('%m%Y'))
        movement = round(float(row['Credit'] or 0) - float(row['Debit'] or 0), 2)

        if month_year < period:
            previous_balance = round(previous_balance + movement, 2)

        current_balance = round(current_balance + movement, 2)

        if month_year == period and (
                round(float(row['Debit'] or 0), 2) != 0 or round(float(row['Credit'] or 0), 2) != 0):
            movements.append({
                'Ordinal': row['Ordinal'],
                'Concept': row['Concept'],
                'Reference': row['Reference'],
                'NfDate': date,
                'Date': date.strftime('%b%d').upper(),
                'Debit': float(row['Debit'] or 0),
                'Credit': float(row['Credit'] or 0)
            })

    return previous_balance, current_balance, movements
