import json
import os
from datetime import datetime

from dotenv import load_dotenv
from jinja2 import Template
from weasyprint import HTML

from commons.commons import calculate_payments, amount_to_words, encrypt_text, generate_qr_base64, parse_csv, \
    calculate_balance_and_movements

META_FILE = "meta.json"
HTML_TEMPLATE = "creditReceiptTemplate.html"

load_dotenv()
KEY = os.getenv("KEY")


def load_metadata():
    with open(META_FILE, "r") as f:
        return json.load(f)


def convert_to_num_period(date_str):
    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }

    month = date_str[:3].lower()
    year = date_str[3:]

    return f"{month_map.get(month, '??')}/{year}"


def get_movement_by_reference(movements, id):
    for movement in movements:
        if movement['Reference'] == f'APTO{id}':
            return movement
    return None


def main(_period):
    metadata = load_metadata()
    admin = metadata["admin"]

    meta_file = os.path.abspath("meta.json")
    period_file = os.path.abspath("expenses.json")

    result = calculate_payments(meta_file, period_file, _period)

    balance_file_path = 'ADLG_ECTA.csv'
    balance_date = parse_csv(balance_file_path)
    num_period = convert_to_num_period(period)
    _, _, movements = calculate_balance_and_movements(balance_date, num_period)

    for apto in result['payments']:
        from_label = f'{apto['name']} -  Dpto. {apto['id']}'
        receipt_number = f'{_period.upper()}-{apto['id']}'

        movement = get_movement_by_reference(movements, apto['id'])

        encrypted_text = encrypt_text(receipt_number, KEY)
        qr_base64 = generate_qr_base64(encrypted_text)

        folder = f'credits/{_period}'

        voucher_img = os.path.abspath(f"{folder}/{apto['id']}.png")
        voucher_url = f"file://{voucher_img}"

        movement_date = movement['NfDate'] if movement is not None else datetime.today()
        movement_amount = movement['Credit'] if movement is not None else apto['total']

        data_to_render = {
            'from_label': from_label,
            'date': movement_date.strftime('%d/%m/%Y'),
            'receipt_number': receipt_number,
            'admin_full_name': admin["name"],
            'amount': f"{movement_amount:.2f}",
            'amount_words': amount_to_words(movement_amount),
            'concept': f'Mantenimiento {result['period_name']}',
            'payment_method': 'Transferencia bancaria',
            'imgs': {
                'signature_qr': qr_base64,
                'voucher_url': voucher_url
            }
        }

        with open(HTML_TEMPLATE, "r", encoding="utf-8") as file:
            html_template = file.read()

        template = Template(html_template)
        html_output = template.render(data_to_render)

        os.makedirs(folder, exist_ok=True)
        pdf_file = f"{folder}/{apto['id']}.pdf"
        HTML(string=html_output).write_pdf(pdf_file)


if __name__ == "__main__":
    period = 'may2025'
    main(period)
