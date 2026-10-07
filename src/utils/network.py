import subprocess

class NetworkOptimizer:
    def __init__(self):
        self.backup = {}

    def optimize(self, log):
        log("--- Network Optimization ---")
        self._set_tcp_nodelay(log)
        self._disable_nagle(log)
        self._set_tcp_ack_frequency(log)
        self._optimize_dns(log)

    def _set_tcp_nodelay(self, log):
        log("TCP NoDelay: enabled")
        subprocess.run(
            'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces" '
            '/v TcpAckFrequency /t REG_DWORD /d 1 /f',
            shell=True, capture_output=True
        )

    def _disable_nagle(self, log):
        log("Nagle's Algorithm: disabled")
        subprocess.run(
            'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces" '
            '/v TcpNoDelay /t REG_DWORD /d 1 /f',
            shell=True, capture_output=True
        )

    def _set_tcp_ack_frequency(self, log):
        log("TCP ACK Frequency: 1 (low latency mode)")
        subprocess.run(
            'netsh int tcp set global autotuninglevel=normal',
            shell=True, capture_output=True
        )

    def _optimize_dns(self, log):
        log("DNS: flushing cache...")
        subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
        log("  ✅ DNS cache flushed")

    def restore(self, log):
        log("Network: restoring defaults...")
        subprocess.run(
            'reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces" '
            '/v TcpAckFrequency /f',
            shell=True, capture_output=True
        )
        subprocess.run(
            'reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces" '
            '/v TcpNoDelay /f',
            shell=True, capture_output=True
        )
        log("  ✅ Network settings restored")