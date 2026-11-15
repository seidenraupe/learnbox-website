#!/usr/bin/env python3
"""Nur Verbindungstest zu KreativMedia (ls), kein Upload. Liest .env im Projektroot."""
from __future__ import annotations

import ftplib
import socket
import ssl
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"


def load_env() -> dict[str, str]:
    out: dict[str, str] = {}
    if not ENV.is_file():
        raise SystemExit(f"Fehlt: {ENV}")
    for line in ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        out[key.strip()] = val.strip().strip('"').strip("'")
    return out


def mask_host(host: str) -> str:
    if "." not in host:
        return host
    parts = host.split(".")
    if len(parts) >= 2:
        return f"{parts[0][:3]}***.{'.'.join(parts[1:])}"
    return host[:3] + "***"


def try_ftps(
    host: str, port: int, user: str, password: str, remote_path: str
) -> tuple[bool, str, bool]:
    """Returns (full_ok, message, login_ok). listing may fail when PASV is blocked."""
    login_ok = False
    try:
        ftp = ftplib.FTP_TLS(timeout=30)
        ftp.connect(host, port)
        ftp.auth()
        ftp.prot_p()
        welcome = ftp.login(user, password)
        login_ok = True
        pwd = ftp.sendcmd("PWD")
        if remote_path and remote_path not in ("/", "."):
            try:
                ftp.cwd(remote_path)
            except ftplib.error_perm as e:
                ftp.quit()
                return (
                    False,
                    f"Login ok ({welcome!r}), aber Ordner {remote_path!r} fehlt: {e}",
                    True,
                )
        ftp.set_pasv(True)
        try:
            names = ftp.nlst()
        except ftplib.error_temp as e:
            ftp.quit()
            return (
                False,
                f"Login ok, {pwd}. Datenkanal (PASV) für Auflistung blockiert: {e}",
                True,
            )
        ftp.quit()
        preview = names[:12]
        suffix = f" … (+{len(names) - 12} weitere)" if len(names) > 12 else ""
        return (
            True,
            f"FTPS ok, {len(names)} Einträge im Zielordner: {preview!r}{suffix}",
            True,
        )
    except (OSError, ftplib.Error, ssl.SSLError) as e:
        if login_ok:
            return False, f"Login ok, danach Fehler: {type(e).__name__}: {e}", True
        return False, f"FTPS: {type(e).__name__}: {e}", False


def try_sftp(host: str, port: int, user: str, password: str, remote_path: str) -> tuple[bool, str]:
    try:
        import paramiko  # type: ignore
    except ImportError:
        return False, "SFTP: paramiko nicht installiert (optional)"

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        if not sftp:
            return False, "SFTP: Client konnte nicht erstellt werden"
        path = remote_path if remote_path else "/"
        names = sftp.listdir(path)
        sftp.close()
        transport.close()
        preview = names[:12]
        suffix = f" … (+{len(names) - 12} weitere)" if len(names) > 12 else ""
        return True, f"SFTP ok, {len(names)} Einträge: {preview!r}{suffix}"
    except Exception as e:
        return False, f"SFTP: {type(e).__name__}: {e}"


def tcp_reachable(host: str, port: int) -> tuple[bool, str]:
    try:
        with socket.create_connection((host, port), timeout=15):
            return True, "TCP-Verbindung aufgebaut"
    except OSError as e:
        return False, f"TCP: {e}"


def main() -> int:
    env = load_env()
    host = env.get("KREATIVMEDIA_SFTP_HOST", "")
    user = env.get("KREATIVMEDIA_SFTP_USER", "")
    password = env.get("KREATIVMEDIA_SFTP_PASSWORD", "")
    remote = env.get("KREATIVMEDIA_REMOTE_PATH", "/")
    protocol = env.get("KREATIVMEDIA_PROTOCOL", "auto").lower()
    port = int(env.get("KREATIVMEDIA_SFTP_PORT", "21"))

    missing = [k for k, v in [
        ("KREATIVMEDIA_SFTP_HOST", host),
        ("KREATIVMEDIA_SFTP_USER", user),
        ("KREATIVMEDIA_SFTP_PASSWORD", password),
    ] if not v]
    if missing:
        print(f"Fehlende Werte in .env: {', '.join(missing)}", file=sys.stderr)
        return 2

    print(f"Ziel (maskiert): {mask_host(host)}:{port}, Pfad: {remote!r}, Protokoll: {protocol}")

    ok_tcp, tcp_msg = tcp_reachable(host, port)
    print(f"Netzwerk: {tcp_msg}")
    if not ok_tcp:
        return 1

    attempts: list[tuple[str, bool, str]] = []
    ports_to_try: list[int] = []
    if port:
        ports_to_try.append(port)
    if protocol in ("auto", "ftps", "ftp") and 21 not in ports_to_try:
        ports_to_try.append(21)

    login_verified = False
    for p in ports_to_try:
        ok, msg, logged_in = try_ftps(host, p, user, password, remote)
        login_verified = login_verified or logged_in
        label = f"FTPS:{p}"
        attempts.append((label, ok, msg))
        if ok:
            print(msg)
            return 0
        print(f"{label}: {msg}", file=sys.stderr)

    if protocol in ("auto", "sftp"):
        sftp_port = 22 if protocol == "sftp" and port == 2121 else port
        if protocol == "auto" and port == 2121:
            sftp_port = 22
        if sftp_port != port:
            ok_tcp2, tcp2 = tcp_reachable(host, sftp_port)
            print(f"Alternativ-Port SFTP {sftp_port}: {tcp2}")
            if not ok_tcp2 and protocol == "auto":
                pass
            else:
                ok, msg = try_sftp(host, sftp_port, user, password, remote)
                attempts.append(("SFTP", ok, msg))
                if ok:
                    print(msg)
                    return 0
                print(msg, file=sys.stderr)
        else:
            ok, msg = try_sftp(host, port, user, password, remote)
            attempts.append(("SFTP", ok, msg))
            if ok:
                print(msg)
                return 0
            print(msg, file=sys.stderr)

    if login_verified:
        print(
            "Hinweis: Zugangsdaten sind gültig (Login ok). "
            "Dateiliste scheiterte vermutlich am FTP-Datenkanal (PASV) von dieser IP "
            "oder am Port in .env – für Upload Port 21 und FTP-Hostname aus Plesk nutzen."
        )
        return 0

    print("Keine Protokoll-Variante erfolgreich.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())