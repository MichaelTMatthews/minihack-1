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
                            "not found in SKILL_TRANSFER_HOME, aborting.",
                        )
                        quit(1)

                print("All skills present, begin training on task.")

                if flags.model in ["foc", "hks"]:
                    flags.foc_options_path = skill_dirs
                    flags.foc_options_config_path = [
                        st_home + "/skill_config.yaml"
                        for _ in range(len(skill_dirs))
                    ]

                elif flags.model == "ks":
                    flags.teacher_path = skill_dirs
                    flags.teacher_config_path = [
                        st_home + "/skill_config.yaml"
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
