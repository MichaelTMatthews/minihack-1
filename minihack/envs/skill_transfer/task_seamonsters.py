from gym.envs import registration

from minihack import RewardManager
from minihack.envs.skill_transfer import skills_all
from minihack.envs.skill_transfer.interleaved_curriculum import MiniHackIC
from minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer
from minihack.envs.skill_transfer.skills_all import RING_NAMES, WAND_NAMES, AMULET_NAMES
from minihack.reward_manager import AlwaysEvent


class MiniHackSeaMonsters(MiniHackSkillTransfer):
    """PickUp a wand in a random location"""

    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_file = "skill_transfer/tasks/task_seamonsters.des"

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackSeaMonstersIC(MiniHackIC):
    def __init__(self, *args, **kwargs):
        # Limit Action Space
        kwargs["actions"] = kwargs.pop("actions", skills_all.COMMANDS)

        des_files = [
            "skill_transfer/skills/skill_pick_up.des",
            "skill_transfer/skills/skill_take_off.des",
            "skill_transfer/skills/skill_wear.des",
            "skill_transfer/skills/skill_navigate_water.des",
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

        reward_manager_to = RewardManager()
        reward_manager_to.add_message_event(["You finish taking off your suit."])
        reward_manager_to.add_event(AlwaysEvent(-0.05, True, False, False))

        reward_manager_w = RewardManager()
        reward_manager_w.add_message_event(["You are now wearing a robe"])
        reward_manager_w.add_event(AlwaysEvent(-0.05, True, False, False))

        reward_manager_nw = RewardManager()
        reward_manager_nw.add_message_event(
            ["You try to crawl"],
            reward=-0.1,
            terminal_sufficient=False,
            repeatable=True,
        )
        reward_manager_nw.add_message_event(
            ["fdshfdsbyufewj"], reward=0, terminal_required=True
        )

        reward_managers = [
            reward_manager_pu,
            reward_manager_to,
            reward_manager_w,
            reward_manager_nw,
        ]

        super().__init__(
            *args, des_files=des_files, reward_managers=reward_managers, **kwargs
        )


registration.register(
    id="MiniHack-SeaMonsters-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_seamonsters:"
    "MiniHackSeaMonsters",
)

registration.register(
    id="MiniHack-SeaMonstersIC-v0",
    entry_point="nle.minihack.envs.skill_transfer.task_seamonsters:"
    "MiniHackSeaMonstersIC",
)
