import psutil
import subprocess
import win32process
import win32api
import win32con

class ProcessOptimizer:
    def __init__(self):
        self.saved_priority = {}

    def optimize(self, log):
        log("--- Process Optimization ---")
        self._set_high_performance_power(log)
        self._kill_background(log)
        self._set_aion_priority(log)

    def _set_high_performance_power(self, log):
        log("Power plan: High Performance")
        subprocess.run(
            "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
            shell=True, capture_output=True
        )
        log("  ✅ Power plan set")

    def _kill_background(self, log):
        targets = ["chrome.exe", "firefox.exe", "msedge.exe",
                   "discord.exe", "spotify.exe", "OneDrive.exe",
                   "Teams.exe", "SteamWebHelper.exe"]
        killed = 0
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() in [t.lower() for t in targets]:
                try:
                    proc.kill()
                    killed += 1
                except Exception:
                    pass
        if killed:
            log(f"  Killed {killed} background processes")
        else:
            log("  No background processes to kill")

    def _set_aion_priority(self, log):
        # Находим процесс AION 2
        found = False
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] and 'aion' in proc.info['name'].lower():
                try:
                    p = psutil.Process(proc.info['pid'])
                    p.nice(psutil.HIGH_PRIORITY_CLASS)
                    self.saved_priority[proc.info['pid']] = psutil.NORMAL_PRIORITY_CLASS
                    log(f"  ✅ AION 2 process priority: HIGH (PID: {proc.info['pid']})")
                    found = True
                except Exception as e:
                    log(f"  ⚠️ Could not set priority: {e}")
        if not found:
            log("  ℹ️ AION 2 not running. Run optimizer before launching game.")

    def restore(self, log):
        log("Process: restoring defaults...")
        subprocess.run(
            "powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e",
            shell=True, capture_output=True
        )
        log("  ✅ Power plan restored to Balanced")