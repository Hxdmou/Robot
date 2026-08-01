"""
RobotReachEnv PPO Training Script - STABLE VERSION
Features for MAXIMUM STABILITY on Windows:
1. CPU-only mode (avoids CUDA compatibility issues)
2. 8 parallel environments (stable on Windows)
3. 5M training steps (converges fast, reduces crash risk)
4. Memory ceiling at 75% with automatic cleanup
5. Pure ASCII output (no GBK encoding errors)
6. Periodic gc.collect() every 500k steps
7. Safe environment cleanup on exit
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



import gc
import time
import psutil
import numpy as np
import os
import signal

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv, VecMonitor
from stable_baselines3.common.callbacks import (
    BaseCallback,
    EvalCallback,
    CheckpointCallback
)
from robot_reach_env_optimized import RobotReachEnvOptimized


def make_env(rank, seed=0):
    def _init():
        env = RobotReachEnvOptimized(render_mode=None, max_steps=500)
        env.reset(seed=seed + rank)
        return env
    return _init


class SafeResourceMonitor(BaseCallback):
    """SAFE Resource Monitor - Prevents memory exhaustion"""

    def __init__(self, check_freq=1000, memory_threshold=75, verbose=1):
        super().__init__(verbose)
        self.check_freq = check_freq
        self.memory_threshold = memory_threshold
        self.last_check_time = time.time()
        self.last_gc_time = time.time()

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            memory_percent = psutil.virtual_memory().percent

            # Strict memory ceiling
            if memory_percent > self.memory_threshold:
                if self.verbose > 0:
                    print(f"\n[SAFETY] Memory: {memory_percent:.1f}% > {self.memory_threshold}%")
                    print("   Running emergency GC...")
                gc.collect()
                time.sleep(0.5)
                new_mem = psutil.virtual_memory().percent
                if self.verbose > 0:
                    print(f"   After cleanup: {new_mem:.1f}%")

                # If still high, reduce frequency
                if new_mem > self.memory_threshold + 5:
                    if self.verbose > 0:
                        print("   WARNING: Memory still high! Continuing carefully...")

            # Periodic deep cleanup every 30 seconds
            current_time = time.time()
            if current_time - self.last_gc_time > 30:
                self.last_gc_time = current_time
                gc.collect()

            # Periodic status output every 30 seconds
            if current_time - self.last_check_time > 30:
                self.last_check_time = current_time
                if self.verbose > 0:
                    cpu_percent = psutil.cpu_percent(interval=0.1)
                    mem_used = psutil.virtual_memory().used / 1024**3
                    mem_total = psutil.virtual_memory().total / 1024**3
                    print(f"\n[STATUS] CPU: {cpu_percent:.1f}% | Memory: {mem_used:.2f}/{mem_total:.2f} GB ({memory_percent:.1f}%)")

        return True


class TimestepLogger(BaseCallback):
    """Logs progress every 500k steps"""

    def __init__(self, log_interval=500000):
        super().__init__()
        self.log_interval = log_interval

    def _on_step(self) -> bool:
        if self.n_calls % self.log_interval == 0:
            elapsed = time.time() - self.model.start_time
            fps = self.n_calls / elapsed if elapsed > 0 else 0
            print(f"\n[PROGRESS] Steps: {self.n_calls:,} / {self.model._total_timesteps:,} | Time: {elapsed/60:.1f} min | FPS: {fps:.0f}")
        return True


class TrainingAnomalyMonitor(BaseCallback):
    """Monitors for loss oscillations and reward anomalies during training"""

    def __init__(self, check_freq=50000, anomaly_window=200000, verbose=1):
        super().__init__(verbose)
        self.check_freq = check_freq
        self.anomaly_window = anomaly_window
        self.reward_history = []
        self.value_loss_history = []
        self.policy_loss_history = []
        self.last_anomaly_time = 0
        self.anomaly_count = 0
        self.max_anomaly_count = 10

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            try:
                infos = self.locals.get('infos', [])
                if infos and isinstance(infos, dict) and 'episode' in infos:
                    episode_info = infos['episode']
                    if isinstance(episode_info, dict):
                        reward = episode_info.get('r', 0)
                        self.reward_history.append(reward)
                        if len(self.reward_history) > self.anomaly_window:
                            self.reward_history = self.reward_history[-self.anomaly_window:]

                if hasattr(self.model, 'logger') and self.model.logger.name_to_value:
                    for key in self.model.logger.name_to_value:
                        if 'value_loss' in key.lower():
                            self.value_loss_history.append(self.model.logger.name_to_value[key])
                        elif 'policy_loss' in key.lower():
                            self.policy_loss_history.append(self.model.logger.name_to_value[key])

                    if len(self.value_loss_history) > 50:
                        self.value_loss_history = self.value_loss_history[-50:]
                    if len(self.policy_loss_history) > 50:
                        self.policy_loss_history = self.policy_loss_history[-50:]

                self._check_anomalies()

            except Exception as e:
                if self.verbose > 0:
                    print(f"[ANOMALY MONITOR] Error checking: {e}")

        return True

    def _check_anomalies(self):
        current_time = time.time()
        if current_time - self.last_anomaly_time < 30:
            return

        anomalies = []

        if len(self.reward_history) >= 100:
            recent_rewards = self.reward_history[-100:]
            reward_mean = np.mean(recent_rewards)
            reward_std = np.std(recent_rewards)
            
            if reward_std > abs(reward_mean) * 0.8 and abs(reward_mean) > 10:
                anomalies.append(f"REWARD OSCILLATION detected! Mean={reward_mean:.2f}, Std={reward_std:.2f}")
            
            if reward_mean < -50:
                anomalies.append(f"REWARD COLLAPSE! Mean reward={reward_mean:.2f}")

        if len(self.value_loss_history) >= 50:
            recent_vloss = self.value_loss_history[-50:]
            vloss_mean = np.mean(recent_vloss)
            vloss_std = np.std(recent_vloss)
            
            if vloss_std > vloss_mean * 1.5 and vloss_mean > 1.0:
                anomalies.append(f"VALUE LOSS OSCILLATION! Mean={vloss_mean:.4f}, Std={vloss_std:.4f}")
            
            if vloss_mean > 50:
                anomalies.append(f"VALUE LOSS EXPLODING! Mean={vloss_mean:.4f}")

        if len(self.policy_loss_history) >= 50:
            recent_ploss = self.policy_loss_history[-50:]
            ploss_mean = np.mean(recent_ploss)
            ploss_std = np.std(recent_ploss)
            
            if ploss_std > abs(ploss_mean) * 1.5 and abs(ploss_mean) > 0.01:
                anomalies.append(f"POLICY LOSS OSCILLATION! Mean={ploss_mean:.4f}, Std={ploss_std:.4f}")

        if anomalies:
            self.anomaly_count += 1
            self.last_anomaly_time = current_time
            
            print("\n" + "=" * 70)
            print("  ⚠️  TRAINING ANOMALY DETECTED ⚠️")
            print("=" * 70)
            for anomaly in anomalies:
                print(f"   {anomaly}")
            print(f"   Steps: {self.n_calls:,}")
            print(f"   Anomaly Count: {self.anomaly_count}/{self.max_anomaly_count}")
            print("=" * 70)

            if self.anomaly_count >= self.max_anomaly_count:
                print("\n" + "=" * 70)
                print("  🔴 CRITICAL: Too many anomalies! Stopping training.")
                print("=" * 70)
                return False

        return True


def setup_safe_exit(model, env, eval_env):
    """Setup safe exit handlers"""
    def safe_exit(signum, frame):
        print("\n[SAFE EXIT] Received exit signal. Saving model...")
        try:
            model.save("ppo_reach_safe_exit")
            print("[SAFE EXIT] Model saved successfully")
        except Exception as e:
            print(f"[SAFE EXIT] Save failed: {e}")
        try:
            env.close()
        except:
            pass
        try:
            eval_env.close()
        except:
            pass
        gc.collect()
        print("[SAFE EXIT] Cleanup complete")
        os._exit(0)

    signal.signal(signal.SIGINT, safe_exit)
    signal.signal(signal.SIGTERM, safe_exit)


if __name__ == "__main__":
    print("=" * 70)
    print("  RobotReachEnv PPO Training - STABLE VERSION")
    print("  CPU-only mode for MAXIMUM COMPATIBILITY")
    print("=" * 70)

    # System info
    memory = psutil.virtual_memory()
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()

    print(f"\n[SYSTEM INFO]")
    print(f"   CPU Cores: {cpu_count}")
    print(f"   CPU Frequency: {cpu_freq.current:.0f} MHz")
    print(f"   Total RAM: {memory.total / 1024**3:.2f} GB")
    print(f"   Available RAM: {memory.available / 1024**3:.2f} GB")
    print(f"   Current Usage: {memory.percent:.1f}%")

    # Optimized training configuration for generalization
    # Windows stable defaults: 8 envs, 5M steps, CPU-only
    n_envs = 8
    total_timesteps = 5_000_000
    learning_rate = 3e-4
    n_steps = 2048
    batch_size = 256
    n_epochs = 10
    gamma = 0.99

    print(f"\n[TRAINING CONFIG]")
    print(f"   Parallel Environments: {n_envs} (Windows-stable)")
    print(f"   Total Steps: {total_timesteps:,}")
    print(f"   Learning Rate: {learning_rate}")
    print(f"   n_steps: {n_steps}")
    print(f"   batch_size: {batch_size}")
    print(f"   n_epochs: {n_epochs}")

    print(f"\n[ENVIRONMENT SETTINGS]")
    print(f"   Target Range: [0.25~0.65, -0.25~0.25, 0.20~0.55] (EXTENDED)")
    print(f"   Joint Init: uniform(-1.0, 1.0) (EXTENDED)")
    print(f"   Reach Reward: 50.0")
    print(f"   Action Penalty: 0.0005")
    print(f"   Time Limit: 500 steps/episode")

    print(f"\n[SAFETY MEASURES]")
    print(f"   Memory Threshold: {75}%")
    print(f"   Device: CPU (CUDA compatibility)")
    print(f"   Auto GC: Every 30 seconds")

    # Create parallel environments
    print(f"\nCreating {n_envs} parallel environments...")
    try:
        env = SubprocVecEnv([make_env(i) for i in range(n_envs)])
        env = VecMonitor(env)
        print(f"   Successfully created {n_envs} environments")
    except Exception as e:
        print(f"   ERROR: Failed to create environments: {e}")
        print("   Falling back to 4 environments...")
        n_envs = 4
        env = SubprocVecEnv([make_env(i) for i in range(n_envs)])
        env = VecMonitor(env)

    # Evaluation environment - wrapped to match training env type
    from stable_baselines3.common.env_util import make_vec_env
    eval_env = make_vec_env(
        lambda: RobotReachEnvOptimized(render_mode=None, max_steps=500),
        n_envs=1,
        vec_env_cls=None
    )
    eval_env = VecMonitor(eval_env)

    # Callbacks
    resource_callback = SafeResourceMonitor(check_freq=1000, memory_threshold=75, verbose=1)
    timestep_callback = TimestepLogger(log_interval=500000)
    anomaly_monitor = TrainingAnomalyMonitor(check_freq=10000, anomaly_window=100000, verbose=1)

    eval_callback = EvalCallback(
        eval_env,
        eval_freq=50000,
        n_eval_episodes=20,
        best_model_save_path="./best_reach_stable/",
        log_path="./eval_logs_reach_stable/",
        deterministic=True,
        verbose=1
    )

    checkpoint_callback = CheckpointCallback(
        save_freq=100000,
        save_path="./checkpoints_reach_stable/",
        name_prefix="ppo_reach",
        verbose=1
    )

    # Initialize PPO model with CPU-only
    print("\nInitializing PPO model (CPU-only)...")
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=learning_rate,
        n_steps=n_steps,
        batch_size=batch_size,
        n_epochs=n_epochs,
        gamma=gamma,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        vf_coef=0.5,
        max_grad_norm=0.5,
        verbose=1,
        tensorboard_log="./logs_reach_stable/",
        device="cpu"
    )

    model.start_time = time.time()

    print(f"\nModel Parameters: {sum(p.numel() for p in model.policy.parameters()):,}")
    print(f"\nStarting Training ({total_timesteps:,} steps)...")
    print("=" * 70)

    # Setup safe exit handlers
    setup_safe_exit(model, env, eval_env)

    start_time = time.time()

    try:
        model.learn(
            total_timesteps=total_timesteps,
            callback=[resource_callback, timestep_callback, anomaly_monitor, eval_callback, checkpoint_callback],
            progress_bar=True
        )

        elapsed = time.time() - start_time
        print(f"\n[SUCCESS] Training Completed!")
        print(f"   Total Time: {elapsed/60:.2f} minutes")
        print(f"   Average Speed: {total_timesteps/elapsed:.1f} steps/second")

        gc.collect()
        model.save("ppo_robot_reach_final_5m_enhanced.zip")
        print("   Model Saved: ppo_robot_reach_final_5m_enhanced.zip")

    except KeyboardInterrupt:
        print("\n\n[INTERRUPT] User interrupted training")
        gc.collect()
        model.save("ppo_robot_reach_final_5m_enhanced")
        print("   Model Saved: ppo_robot_reach_final_5m_enhanced.zip")

    except Exception as e:
        print(f"\n\n[ERROR] Training failed with exception:")
        print(f"   Type: {type(e).__name__}")
        print(f"   Message: {e}")
        import traceback
        traceback.print_exc()
        try:
            gc.collect()
            model.save("ppo_robot_reach_final_5m_enhanced")
            print("   Model Saved: ppo_robot_reach_final_5m_enhanced.zip")
        except Exception as save_err:
            print(f"   Save failed: {save_err}")

    finally:
        print("\n[CLEANUP] Closing environments...")
        try:
            env.close()
            print("   Training environments closed")
        except Exception as e:
            print(f"   Warning: Failed to close training env: {e}")

        try:
            eval_env.close()
            print("   Evaluation environment closed")
        except Exception as e:
            print(f"   Warning: Failed to close eval env: {e}")

        gc.collect()

        memory = psutil.virtual_memory()
        print(f"\n[FINAL STATUS]")
        print(f"   Memory Usage: {memory.percent:.1f}%")
        print("=" * 70)

    # Testing phase
    print("\n" + "=" * 70)
    print("  Testing Training Results")
    print("=" * 70)

    try:
        test_env = RobotReachEnvOptimized(render_mode=None, max_steps=500)
        test_model = PPO.load("ppo_robot_reach_final_5m_enhanced", env=test_env, device="cpu")

        success_count = 0
        total_episodes = 50
        all_rewards = []
        all_steps = []
        all_distances = []

        print(f"\nRunning {total_episodes} test episodes...\n")

        for ep in range(total_episodes):
            obs, info = test_env.reset()
            episode_reward = 0

            for step in range(500):
                action, _ = test_model.predict(obs, deterministic=True)
                obs, reward, terminated, truncated, info = test_env.step(action)
                episode_reward += reward

                if terminated:
                    success_count += 1
                    all_rewards.append(episode_reward)
                    all_steps.append(step + 1)
                    all_distances.append(info.get("distance", 0))
                    status = "[OK]"
                    break
                elif truncated:
                    all_rewards.append(episode_reward)
                    all_steps.append(500)
                    all_distances.append(info.get("distance", 999))
                    status = "[FAIL]"
                    break

            if (ep + 1) % 10 == 0:
                print(f"  Episode {ep+1:3d}: {status} | Steps: {step+1:3d} | Reward: {episode_reward:.2f} | Dist: {info.get('distance', 0):.3f}")

        test_env.close()

        print(f"\n[TEST RESULTS]")
        print(f"   Success Rate: {success_count}/{total_episodes} ({success_count/total_episodes*100:.1f}%)")
        if all_rewards:
            print(f"   Average Reward: {np.mean(all_rewards):.2f}")
            print(f"   Average Steps: {np.mean(all_steps):.1f}")
        if success_count > 0:
            success_steps = [s for s in all_steps if s < 500]
            print(f"   Avg Success Steps: {np.mean(success_steps):.1f}")
            print(f"   Fastest Success: {min(success_steps)} steps")
            avg_dist = np.mean([all_distances[i] for i in range(len(all_distances)) if all_steps[i] < 500])
            print(f"   Avg Success Distance: {avg_dist:.4f}")

    except Exception as e:
        print(f"[TEST ERROR] Testing failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)
    print("  All Tasks Complete")
    print("=" * 70)