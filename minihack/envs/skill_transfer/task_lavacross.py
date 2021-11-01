from gym.envs import registration

from minihack import RewardManager
from minihack.envs.skill_transfer import skills_all
from minihack.envs.skill_transfer.interleaved_curriculum import MiniHackIC
from minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer
from minihack.envs.skill_transfer.skills_all import RING_NAMES, WAND_NAMES, AMULET_NAMES


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


class MiniHackLCFreezeIC(MiniHackIC):
    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_files = [
            "skill_transfer/skills/skill_pick_up.des",
            "skill_transfer/skills/skill_zap_cold.des",
            "skill_transfer/skills/skill_apply_frost_horn.des",
        ]

        reward_manager_pu = RewardManager()
        reward_manager_pu.add_message_event(
            [
                "f - a silver saber",
                "f - a leather cloak",
                *RING_NAMES,
                "f - a key",
                *WAND_NAMES,
                "f - a dagger",
                "f - a horn",
                "f - a towel",
                "f - a green dragon scale mail",
                "$ - a gold piece",
                *AMULET_NAMES,
            ]
        )

        reward_manager_zc = RewardManager()
        reward_manager_zc.add_message_event(["The lava cools and solidifies."])

        reward_manager_afh = RewardManager()
        reward_manager_afh.add_message_event(["The lava cools and solidifies."])

        reward_managers = [reward_manager_pu, reward_manager_zc, reward_manager_afh]

        super().__init__(
            *args, des_files=des_files, reward_managers=reward_managers, **kwargs
        )


registration.register(
    id="MiniHack-LavaCrossFreeze-v0",
    entry_point="minihack.envs.skill_transfer.task_lavacross:" "MiniHackLCFreeze",
)

registration.register(
    id="MiniHack-LavaCrossFreezeIC-v0",
    entry_point="minihack.envs.skill_transfer.task_lavacross:" "MiniHackLCFreezeIC",
)
