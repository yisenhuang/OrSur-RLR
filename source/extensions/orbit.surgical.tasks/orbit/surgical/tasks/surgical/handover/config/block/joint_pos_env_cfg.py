# Copyright (c) 2022-2024, The ORBIT Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from orbit.surgical.assets import ORBIT_ASSETS_DATA_DIR

# from omni.isaac.orbit.assets import RigidObjectCfg
# from omni.isaac.orbit.assets.articulation import ArticulationCfg
# from omni.isaac.orbit.sensors import FrameTransformerCfg
# from omni.isaac.orbit.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
# from omni.isaac.orbit.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
# from omni.isaac.orbit.sim.spawners.from_files.from_files_cfg import UsdFileCfg
# from omni.isaac.orbit.utils import configclass

# Yisen: module name change
from omni.isaac.lab.assets import RigidObjectCfg
from omni.isaac.lab.assets.articulation import ArticulationCfg
from omni.isaac.lab.sensors import FrameTransformerCfg
from omni.isaac.lab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from omni.isaac.lab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from omni.isaac.lab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from omni.isaac.lab.utils import configclass

from orbit.surgical.tasks.surgical.handover import mdp
from orbit.surgical.tasks.surgical.handover.handover_env_cfg import HandoverEnvCfg

##
# Pre-defined configs
##
# from omni.isaac.orbit.markers.config import FRAME_MARKER_CFG  # isort: skip

from omni.isaac.lab.markers.config import FRAME_MARKER_CFG  # isort: skip
from orbit.surgical.assets.psm import PSM_CFG  # isort: skip


@configclass
class BlockHandoverEnvCfg(HandoverEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set PSM as robot
        self.scene.robot_1 = PSM_CFG.replace(
            prim_path="{ENV_REGEX_NS}/Robot_1",
            init_state=ArticulationCfg.InitialStateCfg(pos=(0.2, 0.0, 0.15), rot=(1.0, 0.0, 0.0, 0.0)),
        )
        self.scene.robot_2 = PSM_CFG.replace(
            prim_path="{ENV_REGEX_NS}/Robot_2",
            init_state=ArticulationCfg.InitialStateCfg(pos=(-0.2, 0.0, 0.15), rot=(1.0, 0.0, 0.0, 0.0)),
        )

        # Set actions for the specific robot type (PSM)
        self.actions.body_1_joint_pos = mdp.JointPositionActionCfg(
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
        self.actions.body_2_joint_pos = mdp.JointPositionActionCfg(
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
        self.actions.finger_1_joint_pos = mdp.BinaryJointPositionActionCfg(
            asset_name="robot_1",
            joint_names=["psm_tool_gripper.*_joint"],
            open_command_expr={"psm_tool_gripper1_joint": -0.5, "psm_tool_gripper2_joint": 0.5},
            close_command_expr={"psm_tool_gripper1_joint": -0.07, "psm_tool_gripper2_joint": 0.07},
        )
        self.actions.finger_2_joint_pos = mdp.BinaryJointPositionActionCfg(
            asset_name="robot_2",
            joint_names=["psm_tool_gripper.*_joint"],
            open_command_expr={"psm_tool_gripper1_joint": -0.5, "psm_tool_gripper2_joint": 0.5},
            close_command_expr={"psm_tool_gripper1_joint": -0.07, "psm_tool_gripper2_joint": 0.07},
        )
        # Set the body name for the end effector
        self.commands.ee_pose_1.body_name = "psm_tool_yaw_link"
        self.commands.ee_pose_2.body_name = "psm_tool_yaw_link"

        # Set Peg Block as object
        self.scene.object = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Object",
            init_state=RigidObjectCfg.InitialStateCfg(pos=(-0.2, 0.0, 0.05), rot=(1, 0, 0, 0)),
            spawn=UsdFileCfg(
                usd_path=f"{ORBIT_ASSETS_DATA_DIR}/Props/ORBIT_Surgical/Surgical_block/block.usd",
                scale=(0.011, 0.011, 0.011),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=16,
                    solver_velocity_iteration_count=16,
                    max_angular_velocity=0.1,
                    max_linear_velocity=0.1,
                    max_depenetration_velocity=1.0,
                    disable_gravity=False,
                ),
            ),
        )

        # Listens to the required transforms
        marker_cfg = FRAME_MARKER_CFG.copy()
        marker_cfg.markers["frame"].scale = (0.02, 0.02, 0.02)
        marker_cfg.prim_path = "/Visuals/FrameTransformer"
        self.scene.ee_frame_1 = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot_1/psm_remote_center_link",
            debug_vis=False,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot_1/psm_tool_yaw_link",
                    name="end_effector",
                    offset=OffsetCfg(pos=[0.0, 0.009, 0.0], rot=[0.7071068, -0.7071068, 0, 0]),
                ),
            ],
        )
        self.scene.ee_frame_2 = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot_2/psm_remote_center_link",
            debug_vis=False,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot_2/psm_tool_yaw_link",
                    name="end_effector",
                    offset=OffsetCfg(pos=[0.0, 0.009, 0.0], rot=[0.7071068, -0.7071068, 0, 0]),
                ),
            ],
        )


@configclass
class BlockHandoverEnvCfg_PLAY(BlockHandoverEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
