import argparse
import time
from datetime import datetime
from app.scanner import scan_ports
from app.exporter import export_to_csv, export_to_html


DEFAULT_PORTS = [21, 22, 25, 53, 80, 110, 143, 443, 3306, 8080]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Basic network security scanner"
    )

    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="IP o dominio objetivo"
    )

    parser.add_argument(
        "--ports",
        type=int,
        nargs="+",
        help="Lista de puertos concretos a escanear"
    )

    parser.add_argument(
        "--range",
        dest="port_range",
        type=int,
        nargs=2,
        metavar=("START", "END"),
        help="Rango de puertos a escanear, por ejemplo: --range 1 1024"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Timeout por puerto en segundos"
    )

    parser.add_argument(
        "--output-name",
        type=str,
        default="scan_results",
        help="Nombre base de los archivos de salida"
    )

    return parser.parse_args()


def resolve_ports(args) -> list[int]:
    if args.ports:
        return sorted(set(args.ports))

    if args.port_range:
        start, end = args.port_range

        if start < 1 or end > 65535 or start > end:
            raise ValueError("El rango de puertos debe estar entre 1 y 65535 y START debe ser <= END.")

        return list(range(start, end + 1))

    return DEFAULT_PORTS


def main():
    args = parse_args()

    try:
        ports = resolve_ports(args)
    except ValueError as e:
        print(f"Error: {e}")
        return

    scan_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    start_time = time.perf_counter()
    results = scan_ports(args.target, ports, args.timeout)
    end_time = time.perf_counter()

    scan_duration = end_time - start_time

    open_ports = [item for item in results if item["status"] == "open"]
    closed_ports = [item for item in results if item["status"] == "closed"]

    for item in results:
        banner_text = f" | banner: {item['banner']}" if item["banner"] else ""
        print(
            f"Puerto {item['port']}: {item['status']} "
            f"({item['service']}){banner_text}"
        )

    csv_file = f"output/{args.output_name}.csv"
    html_file = f"output/{args.output_name}.html"

    export_to_csv(results, csv_file)
    export_to_html(
        results,
        html_file,
        args.target,
        scan_timestamp,
        scan_duration
    )

    print("\n--- Resumen ---")
    print(f"Objetivo: {args.target}")
    print(f"Fecha y hora: {scan_timestamp}")
    print(f"Duración del escaneo: {scan_duration:.2f} segundos")
    print(f"Puertos analizados: {len(results)}")
    print(f"Puertos abiertos: {len(open_ports)}")
    print(f"Puertos cerrados: {len(closed_ports)}")
    print(f"Informe CSV generado: {csv_file}")
    print(f"Informe HTML generado: {html_file}")

    if args.ports:
        print("Modo de escaneo: lista manual de puertos")
    elif args.port_range:
        print(f"Modo de escaneo: rango {args.port_range[0]}-{args.port_range[1]}")
    else:
        print("Modo de escaneo: puertos comunes por defecto")


if __name__ == "__main__":
    main()