import json
import os

from dotenv import load_dotenv
from jinja2 import Template
from weasyprint import HTML

from commons.commons import calculate_payments, encrypt_text, generate_qr_base64

HTML_TEMPLATE = "monthly_report.html"
load_dotenv()
KEY = os.getenv("KEY")


def generate_report(report_data):
    yape_img = os.path.abspath("yape.png")
    yape_img_url = f"file://{yape_img}"

    plin_img = os.path.abspath("plin.png")
    plin_img_url = f"file://{plin_img}"

    with open(HTML_TEMPLATE, "r", encoding="utf-8") as file:
        html_template = file.read()

    encrypted_text = encrypt_text(result['period_id'], KEY)
    qr_base64 = generate_qr_base64(encrypted_text)

    report_data['imgs'] = {
        "yape_img_url": yape_img_url,
        "plin_img_url": plin_img_url,
        "qr_base64": qr_base64,
    }

    template = Template(html_template)
    html_output = template.render(report_data)

    folder = 'monthlyReports'
    os.makedirs(folder, exist_ok=True)
    pdf_file = f"{folder}/{report_data['period_id']}.pdf"
    HTML(string=html_output).write_pdf(pdf_file)

    print(f"\n✅ Receipt successfully generated: {pdf_file}")


if __name__ == "__main__":
    meta_file = os.path.abspath("meta.json")
    period_file = os.path.abspath("expenses.json")
    result = calculate_payments(meta_file, period_file, 'mar2026')
    print(json.dumps(result, indent=2, ensure_ascii=False))

    assert result['totals']['total_apt_expenses'] == result['totals']['total_expenses']
    assert result['totals']['total_apt_security'] == result['totals']['total_security']
    assert result['totals']['total_apt'] == result['totals']['total']

    generate_report(result)
