from minihack import MiniHackSkill


class MiniHackSkillTransfer(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            reward_win=1,
            reward_lose=-1,
            **kwargs,
        )

    def _reward_fn(self, last_observation, action, observation, end_status):
        """Use reward_manager to collect reward calculated in _is_episode_end,
        or revert to standard sparse reward."""
        if self.reward_manager is not None:
            reward = self.reward_manager.collect_reward()

            # Also include negative penalty for death
            if (
                end_status == self.StepStatus.DEATH
                or end_status == self.StepStatus.ABORTED
            ):
                reward += self.reward_lose
        else:
            if end_status == self.StepStatus.TASK_SUCCESSFUL:
                reward = self.reward_win
            elif end_status == self.StepStatus.RUNNING:
                reward = 0
            else:  # death or aborted
                reward = self.reward_lose
        return reward + self._get_time_penalty(last_observation, observation)
