import os
import json
import csv
import shutil
import zipfile
from datetime import datetime, timedelta
from typing import Optional, Iterator, Dict
from pathlib import Path
from network.client import NetworkClient  

class Logger:
    def __init__(self, config_path: str, client: Optional[NetworkClient] = None):
        # Wczytaj konfigurację JSON
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)

        self.log_dir = cfg.get("log_dir", "./logs")
        self.archive_dir = os.path.join(self.log_dir, "archive")
        self.filename_pattern = cfg.get("filename_pattern", "sensors_%Y%m%d.csv")
        self.buffer_size = cfg.get("buffer_size", 200)
        self.rotate_every_hours = cfg.get("rotate_every_hours", 24)
        self.max_size_mb = cfg.get("max_size_mb", 10)
        self.rotate_after_lines = cfg.get("rotate_after_lines", None)
        self.retention_days = cfg.get("retention_days", 30)

        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)

        self.buffer = []
        self.current_file = None
        self.current_writer = None
        self.current_filename = None
        self.current_file_start_time = None
        self.lines_written = 0
        self.client = client

    def start(self) -> None:
        now = datetime.now()
        filename = now.strftime(self.filename_pattern)
        self.current_filename = os.path.join(self.log_dir, filename)
        self.current_file_start_time = now
        file_exists = os.path.isfile(self.current_filename)
        self.current_file = open(self.current_filename, mode='a', newline='', encoding='utf-8')
        self.current_writer = csv.writer(self.current_file)
        if not file_exists:
            # Zapisz nagłówek
            self.current_writer.writerow(["timestamp", "sensor_id","sensor_name", "value", "unit"])
            self.lines_written = 1
        else:
            # Licz linię w pliku (bez nagłówka)
            self.lines_written = sum(1 for _ in open(self.current_filename, 'r', encoding='utf-8')) - 1

        self._send_event("start", {
            "filename": self.current_filename,
            "buffer_size": self.buffer_size
        })

    def stop(self) -> None:
        self._flush_buffer()
        if self.current_file:
            self.current_file.close()
            self.current_file = None

        self._send_event("stop", {
            "filename": self.current_filename,
            "buffer_size": self.buffer_size
        })

    def log_reading(self, timestamp: datetime,sensor_id: str,sensor_name: str, value: float, unit: str) -> None:
        row = [timestamp.isoformat(), sensor_id,sensor_name, value, unit]
        self.buffer.append(row)
        self._send_event(
            "log_reading", {
            "timestamp": timestamp.isoformat(),
            "sensor_id": sensor_id,
            "sensor_name": sensor_name,
            "value": value,
            "unit": unit,
            "filename": self.current_filename,
            "buffer_size": self.buffer_size
        })
        if not self.current_file:
            return
        if len(self.buffer) >= self.buffer_size:
            self._flush_buffer()
        if self._should_rotate():
            self._rotate()

    def read_logs(
        self,
        start: datetime,
        end: datetime,
        sensor_id: Optional[str] = None
    ) -> Iterator[Dict]:
        # Przeszukaj pliki csv w log_dir
        for filename in os.listdir(self.log_dir):
            if not filename.endswith(".csv"):
                continue
            full_path = os.path.join(self.log_dir, filename)
            yield from self._read_file(full_path, start, end, sensor_id)

        # Przeszukaj archiwa zip w archive_dir
        for filename in os.listdir(self.archive_dir):
            if not filename.endswith(".zip"):
                continue
            full_path = os.path.join(self.archive_dir, filename)
            yield from self._read_zip(full_path, start, end, sensor_id)

    # --- Prywatne metody ---

    def _flush_buffer(self):
        if not self.buffer:
            return
        for row in self.buffer:
            self.current_writer.writerow(row)
        self.lines_written += len(self.buffer)
        self.current_file.flush()
        self.buffer.clear()
        self._send_event("flush", {"rows": len(self.buffer)})

    def _should_rotate(self) -> bool:
        # Rotacja co rotate_every_hours
        elapsed = datetime.now() - self.current_file_start_time
        if elapsed > timedelta(hours=self.rotate_every_hours):
            return True

        # Rotacja po rozmiarze
        self.current_file.flush()
        size_mb = os.path.getsize(self.current_filename) / (1024 * 1024)
        if size_mb >= self.max_size_mb:
            return True

        # Rotacja po liczbie wierszy
        if self.rotate_after_lines and self.lines_written >= self.rotate_after_lines:
            return True

        return False

    def _rotate(self):
        self.stop()
        self._archive()
        self._clean_old_archives()
        self.start()
        self._send_event("rotate", {"filename": self.current_filename})

    def _archive(self):
        # Przenieś i spakuj aktualny plik do archive/
        base_name = os.path.basename(self.current_filename)
        archive_path = os.path.join(self.archive_dir, base_name)
        name = archive_path[0:-4]
        i=1
        while True:
            if not os.path.isfile(name + ".csv.zip"):
                break
            if i==1:
                name += str("-" + str(i))
            else:
                i_len = len(str(i))
                name = name[:-i_len]
                name+=str(i)
            i+=1

        zip_path = name + ".csv.zip"
        shutil.move(self.current_filename, archive_path)
        
        # Kompresja zip
        with zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(archive_path, arcname=base_name)
        os.remove(archive_path)
        self._send_event("archive", {"zip_path": zip_path})

    def _clean_old_archives(self):
        now = datetime.now()
        cutoff = now - timedelta(days=self.retention_days)
        removed = []
        for filename in os.listdir(self.archive_dir):
            if not filename.endswith(".zip"):
                continue
            full_path = os.path.join(self.archive_dir, filename)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(full_path))
            if file_mtime < cutoff:
                os.remove(full_path)
                removed.append(filename)
        self._send_event("cleanup", {"removed_files": removed})

    def _read_file(self, filepath: str, start: datetime, end: datetime, sensor_id: Optional[str]) -> Iterator[Dict]:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    ts = datetime.fromisoformat(row["timestamp"])
                    if ts < start or ts > end:
                        continue
                    if sensor_id is not None and row["sensor_id"] != sensor_id:
                        continue
                    yield {
                        "timestamp": ts,
                        "sensor_id": row["sensor_id"],
                        "value": float(row["value"]),
                        "unit": row["unit"]
                    }
                except Exception:
                    continue

    def _read_zip(self, zip_path: str, start: datetime, end: datetime, sensor_id: Optional[str]) -> Iterator[Dict]:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            for name in zipf.namelist():
                if not name.endswith(".csv"):
                    continue
                with zipf.open(name) as f:
                    text = f.read().decode('utf-8').splitlines()
                    reader = csv.DictReader(text)
                    for row in reader:
                        try:
                            ts = datetime.fromisoformat(row["timestamp"])
                            if ts < start or ts > end:
                                continue
                            if sensor_id is not None and row["sensor_id"] != sensor_id:
                                continue
                            yield {
                                "timestamp": ts,
                                "sensor_id": row["sensor_id"],
                                "value": float(row["value"]),
                                "unit": row["unit"]
                            }
                        except Exception:
                            continue

    def _send_event(self, event: str, details: Optional[dict] = None):
        if self.client is None:
            return
        message = {
            "type": "logger_event",
            "event": event,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        try:
            self.client.send(message)
        except Exception as e:
            print(f"[Logger] Błąd wysyłania eventu '{event}': {e}")
