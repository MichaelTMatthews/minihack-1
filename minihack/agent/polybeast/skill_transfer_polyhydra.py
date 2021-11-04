import hydra
from omegaconf import DictConfig
import os
import json
import shutil

from minihack.agent.polybeast import polyhydra


@hydra.main(config_name="config")
def main(flags: DictConfig):
    st_home = os.environ.get("SKILL_TRANSFER_HOME")

    if st_home is None:
        print("Environment variable SKILL_TRANSFER_HOME is not set.")
        print(
            "Set this variable to the directory where "
            "trained skill networks should be stored."
        )
        print("Exiting...")
        return

    if flags.model in ["foc", "ks", "hks"]:
        with open(
            "../../../minihack/dat/skill_transfer/tasks/tasks.json"
        ) as tasks_json:
            tasks = json.load(tasks_json)

            if flags.env in tasks.keys():
                skills = tasks[flags.env]

                skill_dirs = [
                    (st_home + "/" + skill + ".tar") for skill in skills
                ]

                for i, skill in enumerate(skills):
                    skill_dir = skill_dirs[i]

                    if not os.path.isfile(skill_dir):
                        print(
                            "Required skill",
                            skill,
                            "not found in SKILL_TRANSFER_HOME, training "
                            "an agent for this skill first.",
                        )

                        skill_flags = flags.copy()
                        skill_flags.env = skill
                        skill_flags.use_lstm = False
                        skill_flags.total_steps = 1e3
                        skill_flags.wandb = False
                        skill_flags.model = "baseline"

                        polyhydra.main(skill_flags)

                        print("Finished training skill", skill)
                        print("Copying network to SKILL_TRANSFER_HOME")

                        shutil.copyfile("checkpoint.tar", skill_dir)

                        print("Network copied, deleting saves.")

                        for filename in os.listdir("."):
                            file_path = os.path.join(".", filename)
                            try:
                                if os.path.isfile(file_path) or os.path.islink(
                                    file_path
                                ):
                                    os.unlink(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                            except Exception as e:
                                print(
                                    "Failed to delete %s. Reason: %s"
                                    % (file_path, e)
                                )

                print("All skills present, begin training on task.")

                if flags.model == "foc":
                    flags.foc_options_path = skill_dirs
                    flags.foc_options_config_path = [
                        st_home + "/option_config.yaml"
                        for _ in range(len(skill_dirs))
                    ]

            else:
                print("Task not found in tasks.json")
                print("Training without skills...")
    else:
        print("Model", flags.model, "does not use skills")
        print("Training without skills...")

    polyhydra.main(flags)


if __name__ == "__main__":
    main()
