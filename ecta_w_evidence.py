import csv
import os
from datetime import datetime
from jinja2 import Template
from weasyprint import HTML
import base64
from pdf2image import convert_from_path
from io import BytesIO


def pdf_to_base64_image(pdf_path):
    images = convert_from_path(pdf_path)
    if images:
        buffered = BytesIO()
        images[0].save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    return None


def main(period):
    # Directorios base
    expenses_folder = 'monthlyExpenses'
    credits_folder = 'credits'

    movements = []
    with open('ADLG_ECTA.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la cabecera
        for row in reader:
            movements.append(
                (row[0], row[1], row[2], row[3], float(row[4]) if row[4] else None, float(row[5]) if row[5] else None))

    # Convertir periodo a formato datetime
    period_date = datetime.strptime(period, "%m/%Y")
    period_folder = period_date.strftime("%b%Y").lower()
    period_formatted = period_date.strftime("%m/%Y")

    # Filtrar movimientos con comprobantes existentes y fecha correspondiente al periodo
    filtered_movements = []

    for ordinal, concept, date, reference, debit, credit in movements:
        try:
            movement_date = datetime.strptime(date, "%d/%m/%y")
            if movement_date.month == period_date.month and movement_date.year == period_date.year:
                folder = period_folder
                attachments = []

                if reference:
                    if reference.startswith("APTO"):
                        folder = os.path.join(credits_folder, folder)
                        filename = f"{reference[4:]}.png"
                    else:
                        folder = os.path.join(expenses_folder, folder)
                        filename = f"{reference}.pdf"

                    filepath = os.path.join(folder, filename)
                    if os.path.exists(filepath):
                        if filename.endswith('.pdf'):
                            encoded_file = pdf_to_base64_image(filepath)
                        else:
                            with open(filepath, 'rb') as file:
                                encoded_file = base64.b64encode(file.read()).decode('utf-8')
                        if encoded_file:
                            attachments.append({'data': encoded_file, 'filename': filename})
                else:
                    folder = os.path.join(expenses_folder, folder)
                    for file in os.listdir(folder):
                        if file.startswith(ordinal):
                            filepath = os.path.join(folder, file)
                            if file.endswith('.pdf'):
                                encoded_file = pdf_to_base64_image(filepath)
                            else:
                                with open(filepath, 'rb') as f:
                                    encoded_file = base64.b64encode(f.read()).decode('utf-8')
                            if encoded_file:
                                attachments.append({'data': encoded_file, 'filename': file})

                if attachments:
                    filtered_movements.append((ordinal, concept, date, reference, debit, credit, attachments))
        except ValueError:
            continue

    # Contar el número total de páginas
    total_pages = sum(len(movement[6]) for movement in filtered_movements)

    # Crear una lista de números de página
    page_counter = 1
    page_data = []
    for movement in filtered_movements:
        for attachment in movement[6]:
            page_data.append((movement, attachment, page_counter, total_pages))
            page_counter += 1

    # Plantilla HTML para el reporte
    html_template = Template('''
<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Movimientos</title>
    <style>
        @page {
            size: A4 portrait;
            margin: 0.5cm;
        }
        body { font-family: Arial, sans-serif; }
        .page { page-break-after: always; margin: 10px; position: relative; }
        .info-table { width: 100%; border-collapse: collapse; margin-bottom: 5px; }
        .info-table th, .info-table td { border: 1px solid #ddd; padding: 4px; text-align: center; }
        .info-table th { background: #f1f1f1; }
        .attachment { text-align: center; margin-top: 10px; }
        .report-header { font-size: 12px; text-align: right; margin-bottom: 5px; }
        .responsive-img { width: auto; height: auto; max-width: 100%; max-height: 400px; object-fit: contain; }
        .pdf-img { width: auto; height: auto; max-width: 100%; max-height: 900px; object-fit: contain; }
    </style>
</head>
<body>
{% for movement, attachment, page_number, total_pages in page_data %}
    <div class="page">
        <div class="report-header">Reporte de movimientos Alto de la Gloria 11 periodo {{ period_formatted }} - Página {{ page_number }} de {{ total_pages }}</div>
        <table class="info-table">
            <tr>
                <th>Ordinal</th>
                <th>Concepto</th>
                <th>Fecha</th>
                <th>Importe</th>
            </tr>
            <tr>
                <td>{{ movement[0] }}</td>
                <td>{{ movement[1] }}</td>
                <td>{{ movement[2] }}</td>
                <td>{{ '{:,.2f}'.format(movement[5] if movement[5] else (-movement[4] if movement[4] else 0)) }}</td>
            </tr>
        </table>
        <div class="attachment">
            <img src="data:image/png;base64,{{ attachment['data'] }}" alt="{{ attachment['filename'] }}" class="{{ 'pdf-img' if attachment['filename'].endswith('.pdf') else 'responsive-img' }}"/>
        </div>
    </div>
{% endfor %}
</body>
</html>
''')

    html_content = html_template.render(page_data=page_data, period_formatted=period_formatted)

    pperiod = (period_formatted.replace('/', '_'))
    HTML(string=html_content).write_pdf(f'monthlyReports/ecta_w_evidence_{pperiod}.pdf')
    print(f'Reporte generado')


if __name__ == "__main__":
    main('08/2025')