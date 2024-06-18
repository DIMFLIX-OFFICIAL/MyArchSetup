import subprocess
from typing import NoReturn, List

from loguru import logger

from packages import BASE, CUSTOM
from utils.questionaire import Questionaire, Answer


class Configure:
	log_file = "build_debug.log"

	def __init__(self) -> None:
		##==> Настройка логирования
		#######################################
		logger.add(
			sink=self.log_file,
			format="{time} | {level} | {message}",
			level="DEBUG",
			encoding="utf-8"
		)

		##==> Запуск анкетирования
		#######################################
		logger.info("[*] The program has been launched successfully. We are starting the survey.")
		answers: Answer = Questionaire.get_answers()

		##==> Выполняем установку
		#######################################
		if answers.update_arch_database:
			self.update_database()

		self.install_packages(custom=answers.install_custom_depends)

	@staticmethod
	def update_database() -> None:
		logger.info("[*] I'm starting to update the package database.")
		subprocess.run(["sudo", "pacman", "-Sy"], check=True)
		logger.success("[+] The package database update was successful!")

	@staticmethod
	def install_aur_manager() -> None:
		logger.info("[*] I'm starting to install the yay package manager")
		subprocess.run(["sudo", "pacman", "-S", "--needed", "git"], check=True)
		subprocess.run(["git", "-C", "/tmp", "clone", "https://aur.archlinux.org/yay.git"], check=True)
		subprocess.run(["makepkg", "-si"], cwd="/tmp/yay", check=True)
		logger.success("[+] Package \"yay\" has been successfully installed!")

	def install_packages(self, custom: bool) -> None:
		self.install_aur_manager()
		succ: NoReturn = lambda pkg: logger.success(f"[+] Package \"{package}\" has been successfully installed!")
		packages_pacman: List[str] = BASE["pacman"] + CUSTOM["pacman"] if custom else BASE["pacman"]
		packages_aur: List[str] = BASE["aur"] + CUSTOM["aur"] if custom else BASE["aur"]

		for package in packages_pacman:
			subprocess.run(["sudo", "pacman", "-S", "--noconfirm", package], check=True)
			succ(package)

		for package in packages_aur:
			subprocess.run(["yay", "-S", "--noconfirm", package], check=True)
			succ(package)


if __name__ == "__main__":
	conf = Configure()
