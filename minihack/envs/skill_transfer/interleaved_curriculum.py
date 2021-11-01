from random import random

import numpy as np

from minihack.envs.skill_transfer.mini_skill_transfer import MiniHackSkillTransfer


class MiniHackIC(MiniHackSkillTransfer):
    """The base class for interleaved curriculum.  Pass it a list of des files
    and on each environment reset a random one will be selected."""

    def __init__(self, *args, des_files, reward_managers, **kwargs):
        self.des_files = des_files
        self.reward_managers = reward_managers

        des_file, reward_manager = self.sample_level()

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )

    def sample_level(self):
        lvl = np.random.randint(len(self.des_files))
        return self.des_files[lvl], self.reward_managers[lvl]

    def reset(self, *args, **kwargs):
        des_file, reward_manager = self.sample_level()
        self.update(des_file)

        if self.reward_manager is not None:
            self.reward_manager.reset()
        self.reward_manager = reward_manager
        if self.reward_manager is not None:
            self.reward_manager.reset()

        if self._level_seeds is not None:
            seed = random.choice(self._level_seeds)
            self.seed(seed, seed, reseed=False)
        return super().reset(*args, **kwargs)
