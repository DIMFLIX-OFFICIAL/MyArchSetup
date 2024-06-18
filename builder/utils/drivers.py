import subprocess
from typing import List


class Drivers:
    @staticmethod
    def get_gpu_vendor() -> str:
        try:
            output = subprocess.check_output("lspci | grep -E 'VGA|3D'", shell=True).decode()
            if "NVIDIA" in output:
                return "Nvidia"
            elif "AMD" in output:
                return "AMD"
            elif "Intel" in output:
                return "Intel"
        except subprocess.CalledProcessError as e:
            print(e.output)
        return "unknown"

    @staticmethod
    def get_cpu_vendor() -> str:
        try:
            output = subprocess.check_output("lscpu", shell=True).decode()
            if "GenuineIntel" in output:
                return "Intel"
            elif "AuthenticAMD" in output:
                return "AMD"
        except subprocess.CalledProcessError as e:
            print(e.output)

        return "unknown"

    @staticmethod
    def auto_detection() -> List[str]:
        cpu = Drivers.get_cpu_vendor()
        gpu = Drivers.get_gpu_vendor()
        drivers_for = [cpu, gpu]

        if "unknown" in drivers_for:
            drivers_for.remove("unknown")

        return drivers_for
