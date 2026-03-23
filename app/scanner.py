import socket


COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
}


def grab_banner(target: str, port: int, timeout: float = 1.0) -> str:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))

        if port in [80, 8080]:
            sock.sendall(b"HEAD / HTTP/1.0\r\nHost: example\r\n\r\n")

        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()

        return banner[:200] if banner else ""
    except Exception:
        return ""


def scan_port(target: str, port: int, timeout: float = 1.0) -> dict:
    result = {
        "target": target,
        "port": port,
        "status": "closed",
        "service": COMMON_SERVICES.get(port, "unknown"),
        "banner": "",
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        connection_result = sock.connect_ex((target, port))
        if connection_result == 0:
            result["status"] = "open"
            result["banner"] = grab_banner(target, port, timeout)
    except socket.gaierror:
        result["status"] = "error_dns"
    except Exception:
        result["status"] = "error"
    finally:
        sock.close()

    return result


def scan_ports(target: str, ports: list[int], timeout: float = 1.0) -> list[dict]:
    results = []

    for port in ports:
        results.append(scan_port(target, port, timeout))

    return results