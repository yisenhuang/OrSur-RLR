# Copyright (c) 2022-2024, The ORBIT Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import math

from orbit.surgical.assets import ORBIT_ASSETS_DATA_DIR

# import omni.isaac.orbit.sim as sim_utils
# from omni.isaac.orbit.assets import AssetBaseCfg
# from omni.isaac.orbit.assets.articulation import ArticulationCfg
# from omni.isaac.orbit.managers import EventTermCfg as EventTerm
# from omni.isaac.orbit.managers import SceneEntityCfg
# from omni.isaac.orbit.utils import configclass

# Yisen: module name change
import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.assets import AssetBaseCfg
from omni.isaac.lab.assets.articulation import ArticulationCfg
from omni.isaac.lab.managers import EventTermCfg as EventTerm
from omni.isaac.lab.managers import SceneEntityCfg
from omni.isaac.lab.utils import configclass

import orbit.surgical.tasks.surgical.reach_dual.mdp as mdp
from orbit.surgical.tasks.surgical.reach_dual.reach_env_cfg import ReachEnvCfg

##
# Pre-defined configs
##
from orbit.surgical.assets.psm import PSM_CFG  # isort: skip


##
# Environment configuration
##


@configclass
class PSMReachEnvCfg(ReachEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        self.scene.table = AssetBaseCfg(
            prim_path="{ENV_REGEX_NS}/Table",
            spawn=sim_utils.UsdFileCfg(
                usd_path=f"{ORBIT_ASSETS_DATA_DIR}/Props/ORBIT_Surgical/Table/table.usd",
            ),
            init_state=AssetBaseCfg.InitialStateCfg(pos=(0.0, 0.0, -0.457)),
        )

        # switch robot to PSM
        self.scene.robot_1 = PSM_CFG.replace(
            prim_path="{ENV_REGEX_NS}/Robot_1",
            init_state=ArticulationCfg.InitialStateCfg(pos=(0.2, 0.0, 0.15), rot=(1.0, 0.0, 0.0, 0.0)),
        )
        self.scene.robot_2 = PSM_CFG.replace(
            prim_path="{ENV_REGEX_NS}/Robot_2",
            init_state=ArticulationCfg.InitialStateCfg(pos=(-0.2, 0.0, 0.15), rot=(1.0, 0.0, 0.0, 0.0)),
        )
        # override rewards
        self.rewards.end_effector_1_position_tracking.params["asset_cfg"].body_names = ["psm_tool_yaw_link"]
        self.rewards.end_effector_1_orientation_tracking.params["asset_cfg"].body_names = ["psm_tool_yaw_link"]
        self.rewards.end_effector_2_position_tracking.params["asset_cfg"].body_names = ["psm_tool_yaw_link"]
        self.rewards.end_effector_2_orientation_tracking.params["asset_cfg"].body_names = ["psm_tool_yaw_link"]
        # override actions
        self.actions.arm_action_1 = mdp.JointPositionActionCfg(
            asset_name="robot_1",
            joint_names=[
                "psm_yaw_joint",
                "psm_pitch_end_joint",
                "psm_main_insertion_joint",
                "psm_tool_roll_joint",
                "psm_tool_pitch_joint",
                "psm_tool_yaw_joint",
            ],
            scale=0.5,
            use_default_offset=True,
        )
        self.actions.arm_action_2 = mdp.JointPositionActionCfg(
            asset_name="robot_2",
            joint_names=[
                "psm_yaw_joint",
                "psm_pitch_end_joint",
                "psm_main_insertion_joint",
                "psm_tool_roll_joint",
                "psm_tool_pitch_joint",
                "psm_tool_yaw_joint",
            ],
            scale=0.5,
            use_default_offset=True,
        )
        # override command generator body
        # end-effector is along z-direction
        self.commands.ee_pose_1 = mdp.UniformPoseCommandCfg(
            asset_name="robot_1",
            body_name="psm_tool_yaw_link",
            resampling_time_range=(4.0, 4.0),
            debug_vis=True,
            ranges=mdp.UniformPoseCommandCfg.Ranges(
                pos_x=(-0.07, 0.07),
                pos_y=(-0.07, 0.07),
                pos_z=(-0.12, -0.08),
                roll=(-math.pi / 2, -math.pi / 2),
                pitch=(0.0, 0.0),
                yaw=(math.pi, math.pi),
            ),
        )

        self.commands.ee_pose_2 = mdp.UniformPoseCommandCfg(
            asset_name="robot_2",
            body_name="psm_tool_yaw_link",
            resampling_time_range=(4.0, 4.0),
            debug_vis=True,
            ranges=mdp.UniformPoseCommandCfg.Ranges(
                pos_x=(-0.07, 0.07),
                pos_y=(-0.07, 0.07),
                pos_z=(-0.12, -0.08),
                roll=(-math.pi / 2, -math.pi / 2),
                pitch=(0.0, 0.0),
                yaw=(math.pi, math.pi),
            ),
        )

        self.events.reset_robot_1_joints = EventTerm(
            func=mdp.reset_joints_by_scale,
            mode="reset",
            params={
                "asset_cfg": SceneEntityCfg("robot_1"),
                "position_range": (0.01, 0.1),
                "velocity_range": (0.0, 0.0),
            },
        )

        self.events.reset_robot_2_joints = EventTerm(
            func=mdp.reset_joints_by_scale,
            mode="reset",
            params={
                "asset_cfg": SceneEntityCfg("robot_2"),
                "position_range": (0.01, 0.1),
                "velocity_range": (0.0, 0.0),
            },
        )


@configclass
class PSMReachEnvCfg_PLAY(PSMReachEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
