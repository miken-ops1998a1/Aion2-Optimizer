import os
import sys
import json
import time
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler


class Logger:
    """
    Логгер для Aion2 Optimizer.
    Пишет одновременно в UI (callback), консоль и файл.
    Поддерживает уровни: INFO, WARNING, ERROR, DEBUG.
    """

    def __init__(self, config_path=None, log_dir=None, level=logging.INFO):
        self.config = self._load_config(config_path)
        self.log_dir = self._resolve_log_dir(log_dir)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = os.path.join(
            self.log_dir, f"session_{self.session_id}.log"
        )

        # UI callback — сюда можно подписать Text-виджет из Tkinter
        self._ui_callback = None

        # Внутренний логгер
        self._logger = logging.getLogger("Aion2Optimizer")
        self._logger.setLevel(level)
        self._logger.propagate = False

        # Защита от дублирования хендлеров при повторной инициализации
        if not self._logger.handlers:
            self._setup_file_handler()
            self._setup_console_handler()

        # Метрики сессии
        self.stats = {
            "session_id": self.session_id,
            "started_at": datetime.now().isoformat(),
            "info": 0,
            "warning": 0,
            "error": 0,
            "debug": 0,
        }

    # ------------------------------------------------------------------ #
    # Инициализация
    # ------------------------------------------------------------------ #

    def _load_config(self, config_path):
        """Загружает config.json, если он есть — иначе дефолты."""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "config.json"
            )
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "monitoring": {
                    "log_to_file": True,
                    "log_path": "%APPDATA%\\Aion2Optimizer\\logs",
                },
                "app_name": "Aion2 Optimizer",
                "version": "1.0.0",
            }

    def _resolve_log_dir(self, log_dir):
        """Разворачивает переменные окружения и создаёт папку."""
        if log_dir is None:
            log_dir = self.config.get("monitoring", {}).get(
                "log_path", "%APPDATA%\\Aion2Optimizer\\logs"
            )

        # Разворачиваем %APPDATA% и т.п.
        log_dir = os.path.expandvars(log_dir)
        log_dir = os.path.expanduser(log_dir)

        # Если APPDATA не развернулся (не Windows) — падаем в локальную папку
        if "%" in log_dir:
            log_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "logs",
            )

        os.makedirs(log_dir, exist_ok=True)
        return log_dir

    def _setup_file_handler(self):
        """Rotating file handler — макс 5 МБ × 3 файла."""
        handler = RotatingFileHandler(
            self.session_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        self._logger.addHandler(handler)

    def _setup_console_handler(self):
        """Цветной вывод в консоль (если запущено из терминала)."""
        if sys.stdout is None:
            return

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        self._logger.addHandler(handler)

    # ------------------------------------------------------------------ #
    # UI-интеграция
    # ------------------------------------------------------------------ #

    def attach_ui(self, callback):
        """
        Привязывает UI-функцию. Callback получит уже готовую строку.

        Пример:
            logger.attach_ui(lambda msg: log_box.insert(tk.END, msg + "\\n"))
        """
        self._ui_callback = callback

    def detach_ui(self):
        self._ui_callback = None

    def _emit(self, formatted_msg):
        if self._ui_callback:
            try:
                self._ui_callback(formatted_msg)
            except Exception:
                pass  # не падаем, если UI умер

    # ------------------------------------------------------------------ #
    # Публичное API
    # ------------------------------------------------------------------ #

    def log(self, msg, level="info"):
        """
        Совместимо с вызовом self.log("текст") из Aion2Optimizer.py.
        По умолчанию уровень — INFO.
        """
        level = level.lower()
        icon = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "debug": "🐛",
            "success": "✅",
        }.get(level, "•")

        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {icon} {msg}"

        # В UI — всегда, независимо от уровня
        self._emit(formatted)

        # В файл/консоль — через logging
        if level == "error":
            self._logger.error(msg)
            self.stats["error"] += 1
        elif level == "warning":
            self._logger.warning(msg)
            self.stats["warning"] += 1
        elif level == "debug":
            self._logger.debug(msg)
            self.stats["debug"] += 1
        else:
            self._logger.info(msg)
            self.stats["info"] += 1

    def info(self, msg):
        self.log(msg, "info")

    def warning(self, msg):
        self.log(msg, "warning")

    def error(self, msg):
        self.log(msg, "error")

    def debug(self, msg):
        self.log(msg, "debug")

    def success(self, msg):
        self.log(msg, "success")

    def separator(self):
        self.log("-" * 50, "debug")

    def header(self, title):
        """Красивый заголовок секции."""
        line = "═" * 50
        self.log(line, "debug")
        self.log(f"  {title}", "info")
        self.log(line, "debug")

    # ------------------------------------------------------------------ #
    # Утилиты
    # ------------------------------------------------------------------ #

    def get_session_file(self):
        """Путь к текущему лог-файлу (для кнопки 'Open log' в UI)."""
        return self.session_file

    def get_log_dir(self):
        return self.log_dir

    def export_session_report(self):
        """
        Сохраняет JSON-отчёт о сессии рядом с логом.
        Полезно для баг-репортов на GitHub.
        """
        self.stats["ended_at"] = datetime.now().isoformat()
        report_path = os.path.join(
            self.log_dir, f"report_{self.session_id}.json"
        )
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, indent=4, ensure_ascii=False)
            return report_path
        except OSError as e:
            self.error(f"Не удалось сохранить отчёт: {e}")
            return None

    def cleanup_old_logs(self, keep_days=7):
        """Удаляет логи старше N дней."""
        now = time.time()
        cutoff = now - keep_days * 86400
        removed = 0
        try:
            for fname in os.listdir(self.log_dir):
                if not fname.endswith(".log"):
                    continue
                fpath = os.path.join(self.log_dir, fname)
                if os.path.getmtime(fpath) < cutoff:
                    os.remove(fpath)
                    removed += 1
        except OSError:
            pass
        if removed:
            self.debug(f"Удалено старых логов: {removed}")
        return removed