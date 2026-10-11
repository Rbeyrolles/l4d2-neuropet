"""Development-only netconsole driver; the installed client VPK needs no helper."""
from pathlib import Path
import argparse
import json
import socket
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=21962)
    parser.add_argument("--duration", type=float, default=65)
    parser.add_argument("--map", default="c1m1_hotel")
    parser.add_argument("--prefix", default="neuropet_client_probe")
    parser.add_argument("--restart-animation", action="store_true", help="Diagnostic only: start LevelInit after the map is ready")
    parser.add_argument("--cheats-off", action="store_true", help="Turn cheats off before capturing client movement")
    parser.add_argument("--interval", type=float, default=3)
    parser.add_argument("--no-captures", action="store_true", help="Run without screenshots")
    args = parser.parse_args()
    log_dir = ROOT / "experiments/client-only"
    log_dir.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + 90
    connection = None
    while time.monotonic() < deadline:
        try:
            connection = socket.create_connection(("127.0.0.1", args.port), timeout=2)
            break
        except OSError:
            time.sleep(1)
    if connection is None:
        raise RuntimeError("Game netconsole did not become available")
    connection.settimeout(.1)
    started = time.monotonic()
    log = bytearray()
    commands = []

    def pump(seconds):
        until = time.monotonic() + seconds
        while time.monotonic() < until:
            try:
                data = connection.recv(65536)
                if not data:
                    return
                log.extend(data)
            except socket.timeout:
                pass

    def send(command):
        connection.sendall((command + "\n").encode("ascii"))
        commands.append({"seconds": round(time.monotonic() - started, 2), "command": command})

    try:
        # Wait until the main menu has mounted addons before loading ordinary coop.
        pump(15)
        send("echo [NEUROPET CLIENT LAB] ordinary coop, no mutation or IncludeScript")
        send("map " + args.map + " coop")
        pump(25)
        send("sv_cheats 1")
        send("director_stop")
        send("nb_stop 1")
        send("god 1")
        send("cl_showfps 0")
        send("net_graph 0")
        if not args.no_captures:
            send("jpeg_quality 95")
        if args.restart_animation:
            send("testhudanim LevelInit")
        if args.cheats_off:
            send("sv_cheats 0")
        send("hideconsole")
        for sample in range(int(args.duration / args.interval)):
            if not args.no_captures:
                send("jpeg " + args.prefix + f"_{sample:02d}")
            pump(args.interval)
        if args.cheats_off:
            send("sv_cheats 1")
        send('script printl("[NEUROPET CLIENT LAB] SERVER BRAIN PRESENT=" + ("NeuroPet" in getroottable()))')
        send("status")
        pump(1)
        send("quit")
        pump(1)
    finally:
        connection.close()
        (log_dir / (args.prefix + ".log")).write_bytes(log)
        (log_dir / (args.prefix + ".json")).write_text(json.dumps(commands, indent=2), encoding="utf-8")
    if b"[NEUROPET CLIENT LAB] SERVER BRAIN PRESENT=false" not in log:
        raise RuntimeError("Did not confirm that the server's NeuroPet brain was absent; inspect the saved log")
    print(f"Saved {len(commands)} commands and {len(log)} console bytes to {log_dir}")


if __name__ == "__main__":
    main()
