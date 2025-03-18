import json
import os
from datetime import datetime

from dotenv import load_dotenv
from jinja2 import Template
from weasyprint import HTML

from commons.commons import calculate_payments, choose_period, amount_to_words, encrypt_text, generate_qr_base64

META_FILE = "meta.json"
HTML_TEMPLATE = "creditReceiptTemplate.html"

load_dotenv()
KEY = os.getenv("KEY")


def load_metadata():
    with open(META_FILE, "r") as f:
        return json.load(f)

def main(period):
    metadata = load_metadata()
    admin = metadata["admin"]

    meta_file = os.path.abspath("meta.json")
    period_file = os.path.abspath("expenses.json")

    result = calculate_payments(meta_file, period_file, period)

    for apto in result['payments']:
        from_label = f'{apto['name']}, Dpto. {apto['id']}'
        receipt_number = f'{period.upper()}-{apto['id']}'

        encrypted_text = encrypt_text(receipt_number, KEY)
        qr_base64 = generate_qr_base64(encrypted_text)

        folder = f'credits/{period}'

        voucher_img = os.path.abspath(f"{folder}/{apto['id']}.png")
        voucher_url = f"file://{voucher_img}"

        data_to_render = {
            'from_label': from_label,
            'date': datetime.today().strftime('%d/%m/%Y'),
            'receipt_number': receipt_number,
            'admin_full_name': admin["name"],
            'amount': f"{apto['total']:.2f}",
            'amount_words': amount_to_words(apto['total']),
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
    # period = choose_period(period_file)
    period = 'mar2025'
    main(period)
