from gym.envs import registration

from minihack import RewardManager
from minihack.envs.skill_transfer import skills_all
from minihack.envs.skill_transfer.interleaved_curriculum import MiniHackIC
from minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer
from minihack.envs.skill_transfer.skills_all import RING_NAMES, WAND_NAMES, AMULET_NAMES


class MiniHackMedusa(MiniHackSkillTransfer):
    """PickUp a wand in a random location"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_file = "skill_transfer/tasks/task_medusa.des"

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackMedusaIC(MiniHackIC):
    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_files = [
            "skill_transfer/skills/skill_pick_up.des",
            "skill_transfer/skills/skill_put_on.des",
            "skill_transfer/skills/skill_navigate_blind.des",
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

        reward_manager_po = RewardManager()
        reward_manager_po.add_message_event(
            ["- a ring of levitation", "You are now wearing a towel around your head."]
        )

        reward_manager_b = None

        reward_managers = [reward_manager_pu, reward_manager_po, reward_manager_b]

        super().__init__(
            *args, des_files=des_files, reward_managers=reward_managers, **kwargs
        )


registration.register(
    id="MiniHack-Medusa-v0",
    entry_point="minihack.envs.skill_transfer.task_medusa:" "MiniHackMedusa",
)

registration.register(
    id="MiniHack-MedusaIC-v0",
    entry_point="minihack.envs.skill_transfer.task_medusa:" "MiniHackMedusaIC",
)
