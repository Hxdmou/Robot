"""
碰撞检测模块（轻量级）
安全原则：低资源占用、实时检测、安全停止
"""
# ============================================================================
# 免责声明与AI使用规范
# ============================================================================
# 本文件仅供技术研究与学习交流使用，不得用于任何非法用途。
#
# AI使用规范：
#   1. 使用本文件相关内容时须遵守所在地法律法规及伦理准则
#   2. 不得用于侵犯他人合法权益、危害网络安全、破坏公共秩序的活动
#   3. 涉及自动化决策的场景须确保人工复核机制与可解释性
#   4. 处理个人信息时须符合数据保护相关法规要求
#
# 风险提示：
#   本文件内容按"现状"提供，不保证绝对准确无误。
#   使用者须自行评估风险，因使用本文件导致的任何损失由使用者承担。
# ============================================================================



import time
import threading
import pybullet as p


class CollisionDetector:
    def __init__(self, config=None):
        config = config or {}
        self.enabled = config.get("enabled", True)
        self.safety_distance = config.get("safety_distance", 0.01)
        self.warning_distance = config.get("warning_distance", 0.02)
        self.check_interval = config.get("check_interval", 0.01)
        self.max_contacts = config.get("max_contacts", 100)
        
        self.collision_history = []
        self.max_history = 100
        self.running = False
        self._lock = threading.Lock()
        
        self.last_collision_time = 0
        self.collision_count = 0
        self.safety_stop_triggered = False

    def check_collision(self, robot_id, obstacle_ids=None):
        if not self.enabled:
            return False, []

        contacts = []
        
        if obstacle_ids:
            for obstacle_id in obstacle_ids:
                result = p.getContactPoints(robot_id, obstacle_id, -1, -1, self.max_contacts)
                contacts.extend(result)
        else:
            result = p.getContactPoints(robot_id, -1, -1, -1, self.max_contacts)
            contacts.extend(result)

        collision_detected = len(contacts) > 0
        
        if collision_detected:
            self._record_collision(contacts)
        
        return collision_detected, contacts

    def check_distance(self, robot_id, target_pos, joint_indices=None):
        if not self.enabled:
            return False, 0.0

        min_distance = float('inf')
        
        if joint_indices:
            for j_idx in joint_indices:
                link_state = p.getLinkState(robot_id, j_idx)
                link_pos = link_state[0]
                dist = self._calc_distance(link_pos, target_pos)
                min_distance = min(min_distance, dist)
        else:
            num_joints = p.getNumJoints(robot_id)
            for j_idx in range(num_joints):
                link_state = p.getLinkState(robot_id, j_idx)
                link_pos = link_state[0]
                dist = self._calc_distance(link_pos, target_pos)
                min_distance = min(min_distance, dist)

        too_close = min_distance < self.safety_distance
        warning = min_distance < self.warning_distance

        return too_close, warning, min_distance

    def _calc_distance(self, pos1, pos2):
        return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 + (pos1[2]-pos2[2])**2)**0.5

    def _record_collision(self, contacts):
        timestamp = time.time()
        self.last_collision_time = timestamp
        self.collision_count += 1
        
        collision_info = {
            "timestamp": timestamp,
            "contact_count": len(contacts),
            "links": []
        }
        
        for contact in contacts[:5]:
            collision_info["links"].append({
                "link_a": contact[3],
                "link_b": contact[4],
                "distance": contact[8],
                "normal_force": contact[9]
            })
        
        with self._lock:
            self.collision_history.append(collision_info)
            if len(self.collision_history) > self.max_history:
                self.collision_history.pop(0)

    def start_monitoring(self, robot_id, obstacle_ids=None):
        self.robot_id = robot_id
        self.obstacle_ids = obstacle_ids
        self.running = True
        print(f"[COLLISION] 碰撞检测已启用")

    def update(self):
        if not self.running or not self.enabled:
            return

        try:
            collision, contacts = self.check_collision(self.robot_id, self.obstacle_ids)
            if collision:
                self._handle_collision(collision, contacts)
        except Exception as e:
            pass

    def _handle_collision(self, collision, contacts):
        if contacts:
            max_force = max(contact[9] for contact in contacts)
            
            if max_force > 10.0:
                print(f"[COLLISION] ⚠️ 碰撞警告 - 接触力: {max_force:.2f}N")
                
            if max_force > 50.0:
                print(f"[COLLISION] ❌ 强碰撞 - 接触力: {max_force:.2f}N")
                self.safety_stop_triggered = True

    def stop_monitoring(self):
        self.running = False

    def is_safety_stop_triggered(self):
        return self.safety_stop_triggered

    def reset_safety_stop(self):
        self.safety_stop_triggered = False

    def get_collision_stats(self):
        with self._lock:
            recent_collisions = [c for c in self.collision_history 
                               if time.time() - c["timestamp"] < 60]
            
            return {
                "total_collisions": self.collision_count,
                "recent_collisions": len(recent_collisions),
                "last_collision_time": self.last_collision_time,
                "safety_stop_triggered": self.safety_stop_triggered
            }

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_enabled(self):
        return self.enabled


class ForceFeedback:
    def __init__(self, config=None):
        config = config or {}
        self.enabled = config.get("enabled", True)
        self.force_threshold = config.get("force_threshold", 10.0)
        self.max_force = config.get("max_force", 100.0)
        
        self.applied_forces = []
        self.max_history = 50
        self._lock = threading.Lock()

    def apply_force(self, robot_id, ee_index, force):
        if not self.enabled:
            return

        clamped_force = [max(-self.max_force, min(self.max_force, f)) for f in force]
        
        p.applyExternalForce(
            objectUniqueId=robot_id,
            linkIndex=ee_index,
            forceObj=clamped_force,
            posObj=[0, 0, 0],
            flags=p.WORLD_FRAME
        )

        with self._lock:
            self.applied_forces.append({
                "timestamp": time.time(),
                "force": clamped_force
            })
            if len(self.applied_forces) > self.max_history:
                self.applied_forces.pop(0)

    def get_force_at_contact(self, robot_id, obstacle_id):
        contacts = p.getContactPoints(robot_id, obstacle_id, -1, -1, 10)
        
        if contacts:
            total_force = sum(contact[9] for contact in contacts)
            avg_force = total_force / len(contacts)
            return avg_force, len(contacts)
        
        return 0.0, 0

    def get_force_stats(self):
        with self._lock:
            if not self.applied_forces:
                return {"avg_force": 0, "max_force": 0}
            
            magnitudes = [sum(f["force"][i]**2 for i in range(3))**0.5 
                         for f in self.applied_forces]
            
            return {
                "avg_force": sum(magnitudes) / len(magnitudes),
                "max_force": max(magnitudes),
                "force_count": len(self.applied_forces)
            }

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
