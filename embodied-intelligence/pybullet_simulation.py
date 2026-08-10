import os
import sys
import warnings
warnings.filterwarnings('ignore')
os.environ['PYBULLET_DISABLE_WARNINGS'] = '1'

import pybullet as p
import pybullet_data
import time
import numpy as np

print("=" * 60)
print("  PyBullet Robot Arm Simulation - IK Control")
print("=" * 60)
print()
print("Controls:")
print("  Mouse Left Drag  - Rotate camera")
print("  Mouse Right Drag - Pan camera")
print("  Mouse Wheel      - Zoom")
print("  H Key            - Reset to home position")
print("  Close window     - Exit")
print()
print("Starting simulation...")
print()

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.setPhysicsEngineParameter(fixedTimeStep=1.0/240.0, numSolverIterations=50)

planeId = p.loadURDF("plane.urdf")
startPos = [0, 0, 0]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])

robotId = p.loadURDF("kuka_iiwa/model.urdf", startPos, startOrientation, useFixedBase=True)
tableId = p.loadURDF("table/table.urdf", [0.5, 0, 0], p.getQuaternionFromEuler([0, 0, 0]))
cubeId = p.loadURDF("cube_small.urdf", [0.5, 0, 0.7])

numJoints = p.getNumJoints(robotId)
print(f"Loaded KUKA LBR iiwa with {numJoints} joints")

endEffectorIndex = 6

p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=50, cameraPitch=-35, cameraTargetPosition=[0.4, 0, 0.5])

target_x = p.addUserDebugParameter("Target X", 0.2, 0.7, 0.5)
target_y = p.addUserDebugParameter("Target Y", -0.3, 0.3, 0.0)
target_z = p.addUserDebugParameter("Target Z", 0.2, 0.8, 0.5)

print("Simulation running! Use sliders to control target position.")
print()

trail = []
max_trail = 80
home_joints = [0.0] * numJoints

def reset_home():
    for j in range(numJoints):
        p.resetJointState(robotId, j, home_joints[j])
    trail.clear()

try:
    while p.isConnected(physicsClient):
        tx = p.readUserDebugParameter(target_x)
        ty = p.readUserDebugParameter(target_y)
        tz = p.readUserDebugParameter(target_z)
        
        keys = p.getKeyboardEvents()
        if ord('h') in keys and keys[ord('h')] & p.KEY_WAS_TRIGGERED:
            reset_home()
        
        target_pos = [tx, ty, tz]
        
        jointPoses = p.calculateInverseKinematics(robotId, endEffectorIndex, target_pos, maxNumIterations=100)
        
        for i in range(min(numJoints, len(jointPoses))):
            p.setJointMotorControl2(
                bodyIndex=robotId,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                targetPosition=jointPoses[i],
                force=500,
                positionGain=0.05,
                velocityGain=0.3
            )
        
        ls = p.getLinkState(robotId, endEffectorIndex)
        ee_pos = ls[4]
        trail.append(list(ee_pos))
        if len(trail) > max_trail:
            trail.pop(0)
        
        for i in range(1, len(trail)):
            p.addUserDebugLine(trail[i-1], trail[i], [0, 0.5, 1], 1, lifeTime=0.1)
        
        p.addUserDebugLine([tx-0.05, ty, tz], [tx+0.05, ty, tz], [1, 0, 0], 2, lifeTime=0.1)
        p.addUserDebugLine([tx, ty-0.05, tz], [tx, ty+0.05, tz], [1, 0, 0], 2, lifeTime=0.1)
        p.addUserDebugLine([tx, ty, tz-0.05], [tx, ty, tz+0.05], [1, 0, 0], 2, lifeTime=0.1)
        
        p.stepSimulation()
        time.sleep(1.0 / 240.0)

except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
finally:
    try:
        p.disconnect(physicsClient)
    except:
        pass
    print("Simulation closed.")
