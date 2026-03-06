from jinja2 import Template
from weasyprint import HTML

from commons.commons import parse_csv, calculate_balance_and_movements


def format_currency(amount):
    return f"{amount:,.2f}" if amount != 0 else ''


def generate_pdf_report(previous_balance, current_balance, movements, period):
    html_template = Template('''
    <!DOCTYPE html>
    <html>
    <head>
        {% block layout_style %}
        <style>
            @page {
                size: A4 portrait;
                margin: 0.8cm 1cm 0.8cm 1cm;
            }
        </style>
        {% endblock %}
        <style>
            body {
                font-family: 'Courier New', Courier, monospace;
                background-color: #fff;
                color: #000;
                padding: 8px;
                font-size: 12px;
                line-height: 1.3;
                margin: 0;
            }

            h2 {
                font-size: 15px;
                text-transform: uppercase;
                letter-spacing: 2px;
                border-bottom: 1px dashed #000;
                padding-bottom: 3px;
                margin: 6px 0 4px 0;
                text-align: center;
            }

            h4 {
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 1px;
                text-align: right;
                margin: 2px 0 8px 0;
            }

            h2::before { content: ">> "; }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 6px;
            }

            th, td {
                border: 1px solid #555;
                padding: 2px 4px;
                text-align: left;
                font-size: 11px;
            }

            th {
                background-color: #ddd;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .amount { text-align: right !important; white-space: nowrap; }

            .total-row td {
                border-top: 1px dashed #000;
                padding-top: 3px;
            }

            .total-row td:first-child,
            .total-row td:nth-child(2) {
                font-weight: bold;
                text-transform: uppercase;
            }
        </style>
    </head>
    <body>
        <h2>Estado de Cuenta Alto de la Gloria 11</h2>
        <h4>Periodo: {{ period }}</h4>
        <table>
            <tr>
                <th>Ordinal</th>
                <th>Concepto</th>
                <th>Fecha</th>
                <th class="amount">Debe</th>
                <th class="amount">Haber</th>
            </tr>
            {% if previous_balance != 0 %}
            <tr class="total-row">
                <td></td>
                <td>Saldo Mes Anterior</td>
                <td></td>
                <td></td>
                <td class="amount">{{ "{:,.2f}".format(previous_balance) }}</td>
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
                <td>Total Movimientos</td>
                <td></td>
                <td class="amount">{{ format_currency(movements|map(attribute='Debit')|sum) }}</td>
                <td class="amount">{{ format_currency(movements|map(attribute='Credit')|sum) }}</td>
            </tr>
            <tr class="total-row">
                <td></td>
                <td>Saldo Final</td>
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
    main('02/2026')
