<h1>How to run a Skill Transfer experiment</h1>
First, create a directory to store pretrained skills in and set the environment variable SKILL_TRANSFER_HOME to point to this directory.
This directory must also include a file called skill_config.yaml.  A default setting for this file can be found in the same directory as this readme.

Next, this directory must be populated with pretrained skill experts.  These are obtained by running polyhydra.py on a skill-specific environment, then copying the final network weights to the SKILL_TRANSFER_HOME directory.

<h2>Full Skill Expert Training Walkthrough</h2>

In this example we train the <i>fight</i> skill.

First, the agent is trained with the following command

```
python -m minihack.agent.polybeast.polyhydra model=baseline env=mini_skill_fight use_lstm=false total_steps=1e7
```

Once the agent is trained, the final weights are found in
```
minihack-1/outputs/<DATE>/<TIME>/checkpoint.tar
```

This tar file is then copied to SKILL_TRANSFER_HOME and renamed to the exact name of the skill environment.
So, in this example, it is renamed to mini_skill_fight.tar

<h2>Training other skills</h2>
Repeat this for all skills.  Almost all skills can be trained within 1e7 timesteps with the exceptions being mini_skill_pick_up and mini_skill_throw, which can both take up to 2e7 timesteps to train.

Remember all skills need to be trained with use_lstm=false

The full list of skills to be trained is
<ul>
<li>mini_skill_apply_frost_horn
<li>mini_skill_eat
<li>mini_skill_fight
<li>mini_skill_nav_blind
<li>mini_skill_nav_lava
<li>mini_skill_nav_lava_to_amulet
<li>mini_skill_nav_over_lava
<li>mini_skill_nav_water
<li>mini_skill_pick_up
<li>mini_skill_put_on
<li>mini_skill_take_off
<li>mini_skill_throw
<li>mini_skill_unlock
<li>mini_skill_wear
<li>mini_skill_wield
<li>mini_skill_zap_cold
<li>mini_skill_zap_death
</ul>

<h2>Training on Tasks</h2>

If the relevant skills for the environment are not present in SKILL_TRANSFER_HOME an error will be shown indicating which skill is missing.
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


<h2>Repeating experiments from diss</h2>

Train each of {foc, ks, hks} on each of the 8 skill transfer tasks for 1e8 timesteps.
Train {baseline} on each of 8 skill transfer tasks for 1.5e8 timesteps.
