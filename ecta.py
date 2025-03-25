from jinja2 import Template
from weasyprint import HTML

from commons.commons import parse_csv, calculate_balance_and_movements


def format_currency(amount):
    return f"{amount:,.2f}" if amount != 0 else ''


def generate_pdf_report(previous_balance, current_balance, movements, period):
    html_template = Template('''
    <html>
    <head>
        {% block layout_style %}
        <style>
            @page {
                size: A4 portrait;
                margin: 1cm;
            }
        </style>
        {% endblock %}
        <style>
            body { font-family: Arial, sans-serif; margin: 10px; }
            h1, h2, h3, h4 { text-align: center; }
            h4 { text-align: right; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 4px; }
            th { background-color: #f2f2f2; text-align: left; }
            td { text-align: left; }
            .amount { text-align: right; }
            .total-row td { border-top: 1px solid #000; border-bottom: 1px solid #000; }
            .total-row td:first-child, .total-row td:nth-child(2) { font-weight: bold; text-transform: uppercase; }
        </style>
    </head>
    <body>
        <h2>Reporte de Estado de Cuenta Alto de la Gloria 11</h2>
        <h4>Periodo: {{ period }}</h4>
        <table>
            <tr>
                <th>Ordinal</th>
                <th>Concept</th>
                <th>Date</th>
                <th class="amount">Debit</th>
                <th class="amount">Credit</th>
            </tr>
            {% if previous_balance != 0 %}
            <tr class="total-row">
                <td></td>
                <td>Saldo Mes Anterior</td>
                <td></td>
                <td></td>
                <td class="amount">{{ "{:,}".format(previous_balance) }}</td>
            </tr>
            {% endif %}
            {% for mov in movements %}
            <tr>
                <td>{{ mov.Ordinal }}</td>
                <td>{{ mov.Concept }}</td>
                <td>{{ mov.Date }}</td>
                <td class="amount">{{ format_currency(mov.Debit) }}</td>
                <td class="amount">{{ format_currency(mov.Credit) }}</td>
            </tr>
            {% endfor %}
            <tr class="total-row">
                <td></td>
                <td>TOTAL MOVIMIENTOS</td>
                <td></td>
                <td class="amount">{{ format_currency(movements|map(attribute='Debit')|sum) }}</td>
                <td class="amount">{{ format_currency(movements|map(attribute='Credit')|sum) }}</td>
            </tr>
            <tr class="total-row">
                <td></td>
                <td>SALDO FINAL</td>
                <td></td>
                <td></td>
                <td class="amount">{{ format_currency(current_balance) }}</td>
            </tr>
        </table>
    </body>
    </html>
    ''')

    html_content = html_template.render(
        period=period,
        previous_balance=previous_balance,
        current_balance=current_balance,
        movements=movements,
        format_currency=format_currency
    )
    pperiod = (period.replace('/', '_'))
    HTML(string=html_content).write_pdf(f"monthlyReports/ecta_{pperiod}.pdf")


def main(period):
    file_path = 'ADLG_ECTA.csv'
    data = parse_csv(file_path)
    previous_balance, current_balance, movements = calculate_balance_and_movements(data, period)

    print(f"Balance until the previous month: {previous_balance:.2f}")
    print(f"Current balance: {current_balance:.2f}")

    generate_pdf_report(previous_balance, current_balance, movements, period)


if __name__ == "__main__":
    main('03/2025')
