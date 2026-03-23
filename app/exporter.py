import csv
from pathlib import Path


def export_to_csv(results: list[dict], filename: str) -> str:
    Path("output").mkdir(exist_ok=True)

    fieldnames = ["target", "port", "status", "service", "banner"]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    return filename


def export_to_html(
    results: list[dict],
    filename: str,
    target: str,
    scan_timestamp: str,
    scan_duration: float,
) -> str:
    Path("output").mkdir(exist_ok=True)

    total_ports = len(results)
    open_ports = len([item for item in results if item["status"] == "open"])
    closed_ports = len([item for item in results if item["status"] == "closed"])

    rows = ""
    for item in results:
        status_class = "open" if item["status"] == "open" else "closed"
        banner = item.get("banner", "") or "-"
        rows += f"""
        <tr>
            <td>{item['port']}</td>
            <td class="{status_class}">{item['status']}</td>
            <td>{item['service']}</td>
            <td>{banner}</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Security Scan Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f8fafc;
                color: #0f172a;
                margin: 0;
                padding: 32px;
            }}

            .container {{
                max-width: 1100px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
            }}

            h1 {{
                margin-top: 0;
                margin-bottom: 8px;
            }}

            .subtitle {{
                color: #475569;
                margin-bottom: 8px;
            }}

            .meta {{
                color: #334155;
                margin-bottom: 24px;
                line-height: 1.6;
            }}

            .summary-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 16px;
                margin: 24px 0 28px;
            }}

            .summary-card {{
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
                padding: 18px;
            }}

            .summary-label {{
                font-size: 13px;
                color: #475569;
                margin-bottom: 8px;
            }}

            .summary-value {{
                font-size: 28px;
                font-weight: bold;
            }}

            .summary-open .summary-value {{
                color: #15803d;
            }}

            .summary-closed .summary-value {{
                color: #b91c1c;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 16px;
            }}

            th, td {{
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
                text-align: left;
                vertical-align: top;
            }}

            th {{
                background: #f1f5f9;
            }}

            .open {{
                color: #15803d;
                font-weight: bold;
            }}

            .closed {{
                color: #b91c1c;
            }}

            @media (max-width: 768px) {{
                .summary-grid {{
                    grid-template-columns: 1fr 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Security Scan Report</h1>
            <p class="subtitle">Objetivo analizado: <strong>{target}</strong></p>
            <div class="meta">
                <div><strong>Fecha y hora:</strong> {scan_timestamp}</div>
                <div><strong>Duración del escaneo:</strong> {scan_duration:.2f} segundos</div>
            </div>

            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-label">Puertos analizados</div>
                    <div class="summary-value">{total_ports}</div>
                </div>
                <div class="summary-card summary-open">
                    <div class="summary-label">Puertos abiertos</div>
                    <div class="summary-value">{open_ports}</div>
                </div>
                <div class="summary-card summary-closed">
                    <div class="summary-label">Puertos cerrados</div>
                    <div class="summary-value">{closed_ports}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-label">Duración</div>
                    <div class="summary-value">{scan_duration:.2f}s</div>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Puerto</th>
                        <th>Estado</th>
                        <th>Servicio</th>
                        <th>Banner</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)

    return filename