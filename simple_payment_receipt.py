import json
import os

from datetime import datetime
from jinja2 import Template
from num2words import num2words
from weasyprint import HTML

from commons.commons import amount_to_words

META_FILE = "meta.json"
HTML_TEMPLATE = "receiptTemplate.html"


def load_metadata():
    """Load meta.json file."""
    with open(META_FILE, "r") as f:
        return json.load(f)


def update_metadata(metadata):
    """Update meta.json file."""
    with open(META_FILE, "w") as f:
        json.dump(metadata, f, indent=4)


def select_service(metadata):
    """Show a menu of available services and return the selected one."""
    services = metadata["services"]

    print("\n📌 Available Services:")
    service_keys = list(services.keys())

    for i, key in enumerate(service_keys, start=1):
        print(f"{i}. {services[key]['description']}")

    while True:
        try:
            choice = int(input("\n👉 Select a service (enter number): "))
            if 1 <= choice <= len(service_keys):
                return service_keys[choice - 1]  # Return the selected service key
            else:
                print("❌ Invalid choice. Please select a valid number.")
        except ValueError:
            print("❌ Please enter a valid number.")


def get_amount(service):
    """Get the amount, asking the user if not present."""
    if "usualAmount" in service:
        return service["usualAmount"]

    while True:
        try:
            amount = float(input("💰 Enter the amount to be paid: "))
            return round(amount, 2)
        except ValueError:
            print("❌ Invalid amount. Please enter a numeric value.")


def generate_receipt(service_key):
    """Generate a payment receipt in PDF format for a specific service."""
    metadata = load_metadata()
    service = metadata["services"][service_key]
    admin = metadata["admin"]

    # Generate receipt number
    receipt_number = f"{service_key.upper()}-{service['enum']:03}"
    metadata["services"][service_key]["enum"] += 1
    update_metadata(metadata)

    # Get amount
    amount = get_amount(service)
    amount_words = amount_to_words(amount)

    with open(HTML_TEMPLATE, "r", encoding="utf-8") as file:
        html_template = file.read()

    html_content = Template(html_template).render(
        date=datetime.today().strftime('%d/%m/%Y'),
        receipt_number=receipt_number,
        admin_full_name=admin["name"],
        admin_short_name=admin["shortName"],
        admin_id=admin["id"],
        responsible=service["responsible"],
        amount=f"{amount:.2f}",
        amount_words=amount_words,
        concept=service["description"],
        payment_method=service["moneySource"]
    )

    os.makedirs(service_key, exist_ok=True)
    pdf_file = f"{service_key}/receipt_{receipt_number}.pdf"
    HTML(string=html_content).write_pdf(pdf_file)

    print(f"\n✅ Receipt successfully generated: {pdf_file}")


def main():
    metadata = load_metadata()
    selected_service = select_service(metadata)
    generate_receipt(selected_service)


if __name__ == '__main__':
    main()
