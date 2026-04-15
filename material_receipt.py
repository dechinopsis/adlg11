import json
import os

from datetime import datetime
from jinja2 import Template
from pdf2image import convert_from_path
from weasyprint import HTML

META_FILE = "meta.json"
HTML_TEMPLATE = "templates/materialReceiptTemplate.html"
OUTPUT_FOLDER = "matRecv"


def load_metadata():
    with open(META_FILE, "r") as f:
        return json.load(f)


def update_metadata(metadata):
    with open(META_FILE, "w") as f:
        json.dump(metadata, f, indent=4)


def get_receiver_name():
    while True:
        name = input("\n👤 Enter receiver's full name: ").strip()
        if name:
            return name.upper()
        print("❌ Name cannot be empty.")


def get_materials():
    print("\n📦 Enter materials (one per line, leave blank to finish):")
    materials = []
    while True:
        item = input(f"  Item {len(materials) + 1}: ").strip()
        if not item:
            if materials:
                break
            print("  ❌ At least one material is required.")
        else:
            materials.append(item)
    return materials


def generate_receipt():
    metadata = load_metadata()
    admin = metadata["admin"]

    enum = metadata["counters"]["matRecv"]
    receipt_number = f"MATRECV-{enum:03}"
    metadata["counters"]["matRecv"] += 1
    update_metadata(metadata)

    receiver_name = get_receiver_name()
    materials = get_materials()

    with open(HTML_TEMPLATE, "r", encoding="utf-8") as f:
        html_template = f.read()

    html_content = Template(html_template).render(
        date=datetime.today().strftime('%d/%m/%Y'),
        receipt_number=receipt_number,
        admin_full_name=admin["name"],
        admin_short_name=admin["shortName"],
        admin_id=admin["id"],
        receiver_name=receiver_name,
        materials=materials,
    )

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    pdf_file = f"{OUTPUT_FOLDER}/receipt_{receipt_number}.pdf"
    HTML(string=html_content).write_pdf(pdf_file)

    images = convert_from_path(pdf_file)
    png_file = f"{OUTPUT_FOLDER}/receipt_{receipt_number}.png"
    images[0].save(png_file, format="PNG")

    print(f"\n✅ Receipt successfully generated: {pdf_file} | {png_file}")


if __name__ == '__main__':
    generate_receipt()
