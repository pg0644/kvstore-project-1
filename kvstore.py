#!/usr/bin/env python3
"""
Project: Simple Persistent Key–Value Store (Project 1)
Language: Python 3.x

Commands Supported:
  SET <key> <value>
  GET <key>
  EXIT

- Stores all data in memory and in a file named data.db
- Uses append-only writes for persistence
- On startup, rebuilds data from the file
"""

import os
import sys

DATA_FILE = "data.db"

class KeyValueStore:
    def __init__(self):
        self.data = [] 
        self.load_data()

    def load_data(self):
        """Read data from file on startup."""
        if not os.path.exists(DATA_FILE):
            open(DATA_FILE, "a").close()
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 3 and parts[0] == "SET":
                    key, value = parts[1], parts[2]
                    self.set_in_memory(key, value)

    def set_in_memory(self, key, value):
        """Update or add a key-value pair in memory."""
        for pair in self.data:
            if pair[0] == key:
                pair[1] = value
                return
        self.data.append([key, value])

    def get_from_memory(self, key):
        """Return value for key if exists."""
        for pair in reversed(self.data):  # last write wins
            if pair[0] == key:
                return pair[1]
        return None

    def set(self, key, value):
        """Set value in memory and append to file."""
        self.set_in_memory(key, value)
        with open(DATA_FILE, "a") as f:
            f.write(f"SET {key} {value}\n")
            f.flush()
            os.fsync(f.fileno())

    def get(self, key):
        """Return the value or NULL."""
        value = self.get_from_memory(key)
        return value if value else "NULL"

def main():
    store = KeyValueStore()

    while True:
        try:
            command = input().strip()
        except EOFError:
            break

        if not command:
            continue

        parts = command.split()
        cmd = parts[0].upper()

        if cmd == "SET" and len(parts) == 3:
            key, value = parts[1], parts[2]
            store.set(key, value)
            print("OK")
        elif cmd == "GET" and len(parts) == 2:
            key = parts[1]
            print(store.get(key))
        elif cmd == "EXIT":
            break
        else:
            print("ERR: Invalid command")

if __name__ == "__main__":
    main()
