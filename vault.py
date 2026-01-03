import os
import shutil
import argparse
import json
import time


VAULT_ROOT = os.path.join(os.getcwd(), "Vault")
CONFIG_FILE = os.path.join(VAULT_ROOT, "config.json")

DEFAULT_CONFIG = {
    "year": "2026",
    "semester": "Sem1",
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads")
}


def load_config():
    if not os.path.exists(VAULT_ROOT):
        os.makedirs(VAULT_ROOT)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f)
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f)

def active_path():
    cfg = load_config()
    return os.path.join(VAULT_ROOT, cfg["year"], cfg["semester"])

def ensure_subject(subject):
    path = os.path.join(active_path(), subject)
    os.makedirs(path, exist_ok=True)
    return path


def setsem(year, sem):
    cfg = load_config()
    cfg["year"] = year
    cfg["semester"] = sem
    save_config(cfg)
    print(f"Active semester set to {year}/{sem}")

def add(file_path, subject, newname=None):
    if not os.path.isfile(file_path):
        print("File not found.")
        return
    dest_folder = ensure_subject(subject)
    name = newname if newname else os.path.basename(file_path)
    shutil.copy(file_path, os.path.join(dest_folder, name))
    print(f"Added {name} to {subject}")

def rename(subject, old, new):
    folder = ensure_subject(subject)
    oldp = os.path.join(folder, old)
    if os.path.isfile(oldp):
        os.rename(oldp, os.path.join(folder, new))
        print("Renamed.")
    else:
        print("File not found.")

def semend():
    base = active_path()
    for subject in os.listdir(base):
        sp = os.path.join(base, subject)
        if os.path.isdir(sp):
            for f in os.listdir(sp):
                os.remove(os.path.join(sp, f))
    print("Semester wiped (Keep folder untouched).")


parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="cmd")

s = sub.add_parser("setsem")
s.add_argument("year")
s.add_argument("sem")

a = sub.add_parser("add")
a.add_argument("file")
a.add_argument("subject")
a.add_argument("--name")

r = sub.add_parser("rename")
r.add_argument("subject")
r.add_argument("old")
r.add_argument("new")

sub.add_parser("semend")

args = parser.parse_args()

if args.cmd == "setsem":
    setsem(args.year, args.sem)
elif args.cmd == "add":
    add(args.file, args.subject, args.name)
elif args.cmd == "rename":
    rename(args.subject, args.old, args.new)
elif args.cmd == "semend":
    semend()
else:
    print("Commands: setsem | add | rename | semend")
