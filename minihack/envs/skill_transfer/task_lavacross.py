from gym.envs import registration

from minihack.envs.skill_transfer import skills_all
from minihack.envs.skill_transfer.mini_skill_transfer import (
    MiniHackSkillTransfer,
)


class MiniHackLCFreeze(MiniHackSkillTransfer):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 400)
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        super().__init__(
            *args,
            des_file="skill_transfer/tasks/task_lavacross_freeze.des",
            **kwargs,
        )


registration.register(
    id="MiniHack-LavaCrossFreeze-v0",
    entry_point="minihack.envs.skill_transfer.task_lavacross:"
    "MiniHackLCFreeze",
)
