from gym.envs import registration

from minihack import RewardManager
from minihack.envs.skill_transfer import skills_all
from minihack.envs.skill_transfer.interleaved_curriculum import MiniHackIC
from minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer
from minihack.envs.skill_transfer.skills_all import RING_NAMES, WAND_NAMES, AMULET_NAMES


class MiniHackMimic(MiniHackSkillTransfer):
    """PickUp a wand in a random location"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_file = "skill_transfer/tasks/task_mimic.des"

        reward_manager = RewardManager()
        reward_manager.add_message_event(
            [
                "The dagger hits the large mimic",
                "The dagger misses",
                "amulet (being worn)",
            ],
            terminal_sufficient=True,
        )

        reward_manager.add_message_event(
            ["Wait!  That's a large mimic!"], terminal_sufficient=True, reward=-1
        )

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackMimicIC(MiniHackIC):
    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_files = [
            "skill_transfer/skills/skill_pick_up.des",
            "skill_transfer/skills/skill_throw.des",
            "skill_transfer/skills/skill_navigate_lava_to_amulet.des",
            "skill_transfer/skills/skill_put_on.des",
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

        reward_manager_t = RewardManager()
        reward_manager_t.add_message_event(
            ["You kill the large mimic", "You kill the orc"], terminal_sufficient=True
        )

        reward_manager_t.add_message_event(
            ["Wait!  That's a large mimic!"],
            terminal_required=False,
            reward=-1.5,
        )

        reward_manager_nlta = RewardManager()
        reward_manager_nlta.add_message_event(
            ["amulet"],
        )

        reward_manager_po = RewardManager()
        reward_manager_po.add_message_event(
            ["- a ring of levitation", "You are now wearing a towel around your head."]
        )

        reward_managers = [
            reward_manager_pu,
            reward_manager_t,
            reward_manager_nlta,
            reward_manager_po,
        ]

        super().__init__(
            *args, des_files=des_files, reward_managers=reward_managers, **kwargs
        )


registration.register(
    id="MiniHack-Mimic-v0",
    entry_point="minihack.envs.skill_transfer.task_mimic:" "MiniHackMimic",
)

registration.register(
    id="MiniHack-MimicIC-v0",
    entry_point="minihack.envs.skill_transfer.task_mimic:" "MiniHackMimicIC",
)
