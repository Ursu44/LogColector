import random
import uuid
import time
import json
import os
from datetime import datetime, timezone

ATTACK_STATE_FILE = "/shared/attack_state.json"

def _read_state() -> dict:
    try:
        with open(ATTACK_STATE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        state = {
            "in_attack":   False,
            "attack_end":  0.0,
            "next_attack": time.time() + random.randint(120, 300),
        }
        _write_state(state)
        return state

def _write_state(state: dict) -> None:
    try:
        os.makedirs("/shared", exist_ok=True)
        with open(ATTACK_STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception:
        pass

def get_phase() -> str:
    """
    Ciclu fix de 9 minute sincronizat cu ceasul sistemului:
      0-3 min: 'low'    → loguri benigne dominante
      3-6 min: 'medium' → activitate suspectă moderată
      6-9 min: 'high'   → attack wave masiv
    """
    cycle_seconds = 9 * 60  # 540 secunde
    position      = time.time() % cycle_seconds

    if position < 180:
        return "low"
    elif position < 360:
        return "medium"
    else:
        return "high"

def is_attack_wave() -> bool:
    """
    Compatibilitate cu generatoarele existente.
    Returnează True/False bazat pe faza curentă.
    """
    phase = get_phase()

    if phase == "low":
        return random.random() < 0.03    # 3% malițioase
    elif phase == "medium":
        return random.random() < 0.35   # 35% malițioase
    else:
        return random.random() < 0.92   # 92% malițioase


# ── Funcții comune tuturor generatoarelor ────────────────────────

def random_ip():
    private_ranges = [
        lambda: f"172.{random.randint(16,27)}.{random.randint(0,255)}.{random.randint(1,254)}",
        lambda: f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
    ]
    public_ranges = [
        lambda: f"31.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
        lambda: f"52.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    ]
    return random.choice(private_ranges + public_ranges)()


def random_user():
    users = [
        "admin", "root", "user1", "user2",
        "service", "backup", "test",
        "guest", "support"
    ]
    return random.choice(users)


def random_request_id():
    return f"req-{uuid.uuid4().hex[:12]}"


def timestamp_syslog():
    return datetime.now(timezone.utc).strftime("%b %d %H:%M:%S")


def timestamp_epoch():
    return f"{time.time():.3f}"


def timestamp_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def random_file_path():
    paths = [
        "/var/log/syslog",
        "/etc/hosts",
        "/usr/bin/python3",
        "/home/user1/.bashrc",
        "/opt/app/config.yaml",
        "/tmp/update.sh",
        "/tmp/.x",
        "/var/tmp/malware.bin",
        "/dev/shm/payload",
        "/root/.ssh/authorized_keys",
        "C:\\Windows\\System32\\notepad.exe",
        "C:\\Program Files\\App\\app.exe",
        "C:\\Users\\user1\\Documents\\report.docx",
        "C:\\Temp\\payload.exe",
        "C:\\Users\\Public\\svchost.exe",
        "C:\\Windows\\Temp\\dropper.exe",
        "C:\\Windows\\System32\\svchost.exe"
    ]
    return random.choice(paths)


def hostname():
    return random.choice(["server", "web01", "db01", "fw01", "ids01"])


def random_port():
    common_ports = [22, 80, 443, 3389, 3306, 5432]
    if random.random() < 0.7:
        return random.choice(common_ports)
    return random.randint(1024, 6553)


def internal_ip():
    return f"192.168.{random.randint(0,25)}.{random.randint(10,25)}"


def external_ip():
    return (
        f"{random.randint(20,120)}.{random.randint(0,25)}"
        f".{random.randint(0,25)}.{random.randint(1,24)}"
    )

def syslog_timestamp():
    """Alias pentru compatibilitate cu network_logs.py"""
    return datetime.now(timezone.utc).strftime("%b %d %H:%M:%S")
