from gym.envs import registration

from minihack.envs.skill_transfer import skills_all
from minihack.envs.skill_transfer.mini_skill_transfer import (
    MiniHackSkillTransfer,
)


class MiniHackMedusa(MiniHackSkillTransfer):
    """PickUp a wand in a random location"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_file = "skill_transfer/tasks/task_medusa.des"

        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-Medusa-v0",
    entry_point="minihack.envs.skill_transfer.task_medusa:" "MiniHackMedusa",
)
