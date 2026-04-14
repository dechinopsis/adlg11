import csv
import json
import os
from datetime import datetime

EXPENSES_FOLDER = 'monthlyExpenses'
CREDITS_FOLDER  = 'credits'
CSV_PATH        = 'ADLG_ECTA.csv'
OUTPUT_PATH     = 'evidence-manifest.json'

MONTH_ABBR = {
    '01': 'jan', '02': 'feb', '03': 'mar', '04': 'apr',
    '05': 'may', '06': 'jun', '07': 'jul', '08': 'aug',
    '09': 'sep', '10': 'oct', '11': 'nov', '12': 'dec'
}


def period_folder(month, year):
    return MONTH_ABBR[month] + year


def find_files(folder, prefix):
    """Return all files in folder whose name starts with prefix."""
    if not os.path.isdir(folder):
        return []
    return [
        os.path.join(folder, f).replace('\\', '/')
        for f in sorted(os.listdir(folder))
        if f.startswith(prefix) and os.path.isfile(os.path.join(folder, f))
    ]


def build_manifest():
    manifest = {}

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [h.strip().lstrip('\ufeff') for h in reader.fieldnames]
        rows = list(reader)

    for row in rows:
        ordinal   = row['Ordinal'].strip()
        reference = row['Reference'].strip()
        date_str  = row['Date'].strip()

        try:
            date = datetime.strptime(date_str, '%d/%m/%y')
        except ValueError:
            continue

        month  = date.strftime('%m')
        year   = date.strftime('%Y')
        folder = period_folder(month, year)
        period_id = folder  # e.g. "jan2026"

        files = []

        if reference:
            if reference.startswith('APTO'):
                apt_id = reference[4:]  # e.g. "302"
                image_exts = {'.png', '.jpg', '.jpeg', '.webp'}
                files = [
                    f for f in find_files(os.path.join(CREDITS_FOLDER, folder), apt_id)
                    if os.path.splitext(f)[1].lower() in image_exts
                ]
            else:
                path = os.path.join(EXPENSES_FOLDER, folder, f'{reference}.pdf')
                if os.path.exists(path):
                    files = [path.replace('\\', '/')]
        else:
            files = find_files(os.path.join(EXPENSES_FOLDER, folder), ordinal)

        if files:
            if period_id not in manifest:
                manifest[period_id] = {}
            manifest[period_id][ordinal] = files

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f'Manifest written to {OUTPUT_PATH}')
    total = sum(len(v) for p in manifest.values() for v in p.values())
    print(f'Periods: {len(manifest)} — Total file entries: {total}')


if __name__ == '__main__':
    build_manifest()
