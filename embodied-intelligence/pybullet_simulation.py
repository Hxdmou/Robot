
import pybullet as p
import pybullet_data
import time
import numpy as np
import sys

print("=" * 60)
print("  PyBullet Robot Arm Simulation")
print("=" * 60)
print()
print("Controls:")
print("  Mouse Left Drag  - Rotate camera")
print("  Mouse Right Drag - Pan camera")
print("  Mouse Wheel      - Zoom")
print("  Close window     - Exit")
print()
print("Starting simulation...")
print()

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

planeId = p.loadURDF("plane.urdf")
startPos = [0, 0, 0]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])

# Load KUKA LBR iiwa 7 DOF robot arm
robotId = p.loadURDF("kuka_iiwa/model.urdf", startPos, startOrientation, useFixedBase=True)

# Load a table
tableId = p.loadURDF("table/table.urdf", [0.5, 0, 0], p.getQuaternionFromEuler([0, 0, 0]))

# Load a cube to grasp
cubeId = p.loadURDF("cube_small.urdf", [0.5, 0, 0.7])

numJoints = p.getNumJoints(robotId)
print(f"Loaded robot with {numJoints} joints")

# Get end effector index
endEffectorIndex = 6

# Reset camera
p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=50, cameraPitch=-35, cameraTargetPosition=[0.4, 0, 0.5])

# Add debug parameters for target position
target_x = p.addUserDebugParameter("Target X", 0.2, 0.7, 0.5)
target_y = p.addUserDebugParameter("Target Y", -0.3, 0.3, 0.0)
target_z = p.addUserDebugParameter("Target Z", 0.2, 0.8, 0.5)

# Add reset button
reset_btn = p.addUserDebugParameter("Reset Pose", 1, 0, 0)
prev_reset = 0

print("Simulation running! Use sliders to control target position.")
print()

# Trail points
trail = []

try:
    while p.isConnected():
        # Read target position
        tx = p.readUserDebugParameter(target_x)
        ty = p.readUserDebugParameter(target_y)
        tz = p.readUserDebugParameter(target_z)
        
        # Read reset button
        current_reset = p.readUserDebugParameter(reset_btn)
        if current_reset != prev_reset:
            tx, ty, tz = 0.5, 0.0, 0.5
            prev_reset = current_reset
        
        target_pos = [tx, ty, tz]
        
        # Calculate IK
        jointPoses = p.calculateInverseKinematics(robotId, endEffectorIndex, target_pos)
        
        # Apply joint positions
        for i in range(min(numJoints, len(jointPoses))):
            p.setJointMotorControl2(robotId, i, p.POSITION_CONTROL, jointPoses[i], force=500)
        
        # Step simulation
        p.stepSimulation()
        
        # Get end effector position
        linkState = p.getLinkState(robotId, endEffectorIndex)
        endPos = linkState[0]
        
        # Draw trail
        trail.append(list(endPos))
        if len(trail) > 100:
            trail.pop(0)
        
        for i in range(len(trail) - 1):
            p.addUserDebugLine(trail[i], trail[i+1], [0, 0.5, 1], lineWidth=2, lifeTime=0.1)
        
        # Draw target marker
        p.addUserDebugLine([tx-0.05, ty, tz], [tx+0.05, ty, tz], [1, 0, 0], lineWidth=3, lifeTime=0.1)
        p.addUserDebugLine([tx, ty-0.05, tz], [tx, ty+0.05, tz], [1, 0, 0], lineWidth=3, lifeTime=0.1)
        p.addUserDebugLine([tx, ty, tz-0.05], [tx, ty, tz+0.05], [1, 0, 0], lineWidth=3, lifeTime=0.1)
        
        time.sleep(1.0 / 240.0)

except KeyboardInterrupt:
    pass
finally:
    p.disconnect()
    print("\nSimulation exited.")
