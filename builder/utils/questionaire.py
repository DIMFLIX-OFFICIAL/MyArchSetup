import subprocess
import inquirer
from inquirer import Checkbox as QuestionCheckbox, List as QuestionList
from inquirer.themes import GreenPassion
from typing import List, Union, Dict
from dataclasses import dataclass

from .banner import banner
from .drivers import Drivers


@dataclass
class Answer:
    enable_multilib: bool
    update_arch_database: bool
    install_custom_depends: bool
    install_drivers: bool

    intel_driver: bool
    nvidia_driver: bool
    amd_driver: bool


class Questionaire:
    answers_type = Dict[str, Union[str, List[str]]]

    @staticmethod
    def get_answers() -> Answer:
        drivers = Drivers.auto_detection()

        answers: Questionaire.answers_type = {}
        quests: List[Union[QuestionCheckbox, QuestionList]] = [
            QuestionList(
                name='enable_multilib',
                message="1) Should I enable the multilib repository?",
                choices=["Yes", "No"],
                default="Yes",
                carousel=True
            ),
            QuestionList(
                name='update_arch_database',
                message="2) Update Arch DataBase?",
                choices=["Yes", "No"],
                default="Yes",
                carousel=True
            ),
            QuestionList(
                name='install_custom_depends',
                message="3) Install custom dependencies?",
                choices=["Yes", "No"],
                carousel=True
            ),
            QuestionCheckbox(
                name='install_drivers',
                message="4) What drivers do you want to install?",
                choices=["Nvidia", "Intel", "AMD"],
                default=drivers,
                carousel=True
            ),
        ]

        for question in quests:
            subprocess.run("clear", shell=True)
            print(banner)
            answer = inquirer.prompt([question], theme=GreenPassion())
            answers.update(answer)

        return Answer(
            enable_multilib=answers['enable_multilib'] == 'Yes',
            update_arch_database=answers['update_arch_database'] == 'Yes',
            install_custom_depends=answers['install_custom_depends'] == 'Yes',
            install_drivers=len(answers['install_drivers']) > 0,
            intel_driver='Intel' in answers['install_drivers'],
            nvidia_driver='Nvidia' in answers['install_drivers'],
            amd_driver='AMD' in answers['install_drivers'],
        )
