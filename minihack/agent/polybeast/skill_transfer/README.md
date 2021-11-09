<h1>How to run a Skill Transfer experiment</h1>
First, create a directory to store pretrained skills in and set the environment variable SKILL_TRANSFER_HOME to point to this directory.
This directory must also include a file called skill_config.yaml.  A default setting for this file can be found in the same directory as this readme.

Next, run an experiment by calling skill_transfer_polyhydra.py in the same way you would call polyhydra.py, for instance
```
python -m minihack.agent.polybeast.skill_transfer_polyhydra model=foc env=mini_simple_seq total_steps=1e8
```

If the relevant skills for the environment are not present in SKILL_TRANSFER_HOME, they will be trained and stored there before the main experiment is run.
The skill transfer specific models are
<ul>
  <li>foc: Options Framework</li>
  <li>ks: Kickstarting</li>
  <li>hks: Hierarchical Kickstarting</li>
</ul>

The tasks created for skill transfer are
<ul>
  <li>mini_simple_seq: Battle</li>
  <li>mini_simple_union: Over or Around</li>
  <li>mini_simple_intersection: Prepare for Battle</li>
  <li>mini_simple_random: Target Practice</li>
  <li>mini_lc_freeze: Frozen Lava Cross</li>
  <li>mini_medusa: Medusa</li>
  <li>mini_mimic: Identify Mimic</li>
  <li>mini_seamonsters: Sea Monsters</li>
</ul>

So, for example, to run hierarchical kickstarting on the Target Practice environment, one would call
```
python -m minihack.agent.polybeast.skill_transfer_polyhydra model=hks env=mini_simple_random
```
With all other parameters being able to be set in the same way as with polyhydra.py
