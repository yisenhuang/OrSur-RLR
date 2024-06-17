# Copyright (c) 2022-2024, The ORBIT Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import gymnasium as gym

from . import agents, ik_abs_env_cfg, ik_rel_env_cfg, joint_pos_env_cfg

##
# Register Gym environments.
##

##
# Joint Position Control
##

gym.register(
    id="Isaac-Reach-PSM-v0",
    # entry_point="omni.isaac.orbit.envs:RLTaskEnv", # Yisen module name change
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": joint_pos_env_cfg.PSMReachEnvCfg,
        "rsl_rl_cfg_entry_point": agents.rsl_rl_cfg.PSMReachPPORunnerCfg,
    },
)

gym.register(
    id="Isaac-Reach-PSM-Play-v0",
    # entry_point="omni.isaac.orbit.envs:RLTaskEnv", # Yisen module name change
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": joint_pos_env_cfg.PSMReachEnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": agents.rsl_rl_cfg.PSMReachPPORunnerCfg,
    },
)

##
# Inverse Kinematics - Absolute Pose Control
##

gym.register(
    id="Isaac-Reach-PSM-IK-Abs-v0",
    # entry_point="omni.isaac.orbit.envs:RLTaskEnv", # Yisen module name change
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": ik_abs_env_cfg.PSMReachEnvCfg,
        "rsl_rl_cfg_entry_point": agents.rsl_rl_cfg.PSMReachPPORunnerCfg,
    },
    disable_env_checker=True,
)

gym.register(
    id="Isaac-Reach-PSM-IK-Abs-Play-v0",
    # entry_point="omni.isaac.orbit.envs:RLTaskEnv", # Yisen module name change
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": ik_abs_env_cfg.PSMReachEnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": agents.rsl_rl_cfg.PSMReachPPORunnerCfg,
    },
    disable_env_checker=True,
)

##
# Inverse Kinematics - Relative Pose Control
##

gym.register(
    id="Isaac-Reach-PSM-IK-Rel-v0",
    # entry_point="omni.isaac.orbit.envs:RLTaskEnv", # Yisen module name change
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": ik_rel_env_cfg.PSMReachEnvCfg,
        "rsl_rl_cfg_entry_point": agents.rsl_rl_cfg.PSMReachPPORunnerCfg,
    },
    disable_env_checker=True,
)

gym.register(
    id="Isaac-Reach-PSM-IK-Rel-Play-v0",
    # entry_point="omni.isaac.orbit.envs:RLTaskEnv", # Yisen module name change
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": ik_rel_env_cfg.PSMReachEnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": agents.rsl_rl_cfg.PSMReachPPORunnerCfg,
    },
    disable_env_checker=True,
)
