"""
工业化REST API服务器 - 机器人控制与监控
支持：健康检查、状态监控、运动控制、参数配置、模型管理
"""
import os
import sys
import time
import json
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from settings import get_all_config, SIMULATION_CONFIG, SAFETY_CONFIG
    SETTINGS_AVAILABLE = True
except:
    SETTINGS_AVAILABLE = False

try:
    from health_check import run_health_check
    HEALTH_AVAILABLE = True
except:
    HEALTH_AVAILABLE = False


# ============================================================================
# 数据模型
# ============================================================================
class JointCommand(BaseModel):
    joints: List[float] = Field(description="关节角度列表(弧度)")
    speed: Optional[float] = Field(default=1.0, description="速度比例(0.1-1.0)")


class CartesianCommand(BaseModel):
    x: float = Field(description="X坐标(米)")
    y: float = Field(description="Y坐标(米)")
    z: float = Field(description="Z坐标(米)")
    speed: Optional[float] = Field(default=1.0, description="速度比例")


class GripperCommand(BaseModel):
    action: str = Field(description="open/close")
    width: Optional[float] = Field(default=0.0, description="夹爪宽度(米)")
    force: Optional[float] = Field(default=50.0, description="夹持力(N)")


class SafetyConfig(BaseModel):
    torque_limit_ratio: Optional[float] = Field(default=0.7, ge=0.1, le=1.0)
    velocity_limit_ratio: Optional[float] = Field(default=0.7, ge=0.1, le=1.0)
    enable_collision_detection: Optional[bool] = Field(default=True)


# ============================================================================
# 系统状态
# ============================================================================
system_state = {
    "start_time": datetime.now().isoformat(),
    "mode": "idle",
    "connected": False,
    "safety_enabled": True,
    "estop_triggered": False,
    "current_joints": [0.0] * 7,
    "current_pose": {"x": 0.0, "y": 0.0, "z": 0.0},
    "joint_temperatures": [25.0] * 7,
    "operation_count": 0,
    "error_count": 0,
    "last_error": None,
}

command_history = []


# ============================================================================
# 生命周期管理
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 60)
    print("  机器人工业化API服务器启动中...")
    print("=" * 60)
    system_state["mode"] = "running"
    print(f"  ✅ 服务器就绪: {datetime.now().isoformat()}")
    print("=" * 60)
    yield
    print("  服务器关闭")
    system_state["mode"] = "shutdown"


app = FastAPI(
    title="机器人工业化控制API",
    description="具身智能系统 - 工业级机器人控制与监控平台",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# 1. 系统接口
# ============================================================================
@app.get("/", tags=["系统"])
async def root():
    return {
        "name": "具身智能工业化控制系统",
        "version": "2.0.0",
        "status": system_state["mode"],
        "uptime_seconds": (datetime.now() - datetime.fromisoformat(system_state["start_time"])).total_seconds(),
        "docs": "/docs",
    }


@app.get("/health", tags=["系统"])
async def health():
    result = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "system": system_state["mode"],
        "safety": system_state["safety_enabled"],
        "estop": not system_state["estop_triggered"],
    }
    if HEALTH_AVAILABLE:
        try:
            extra = run_health_check()
            if isinstance(extra, dict):
                result.update(extra)
        except:
            pass
    return result


@app.get("/config", tags=["系统"])
async def get_config():
    if SETTINGS_AVAILABLE:
        return get_all_config()
    return {"config": "default"}


@app.get("/status", tags=["系统"])
async def get_status():
    return {
        "timestamp": datetime.now().isoformat(),
        "mode": system_state["mode"],
        "connected": system_state["connected"],
        "estop": system_state["estop_triggered"],
        "safety_enabled": system_state["safety_enabled"],
        "joints": system_state["current_joints"],
        "pose": system_state["current_pose"],
        "temperatures": system_state["joint_temperatures"],
        "operation_count": system_state["operation_count"],
        "error_count": system_state["error_count"],
        "last_error": system_state["last_error"],
    }


# ============================================================================
# 2. 安全接口
# ============================================================================
@app.post("/safety/estop", tags=["安全"])
async def emergency_stop():
    """触发紧急停止"""
    system_state["estop_triggered"] = True
    system_state["mode"] = "estop"
    print("⚠️  紧急停止已触发!")
    return {"status": "estop_triggered", "message": "紧急停止已激活，请排查后复位"}


@app.post("/safety/reset", tags=["安全"])
async def reset_estop():
    """复位紧急停止"""
    system_state["estop_triggered"] = False
    system_state["mode"] = "idle"
    print("✅ 紧急停止已复位")
    return {"status": "reset", "message": "紧急停止已复位，系统就绪"}


@app.get("/safety/config", tags=["安全"])
async def get_safety_config():
    if SETTINGS_AVAILABLE:
        return {
            "torque_limit_ratio": SAFETY_CONFIG.get("torque_limit_ratio", 0.7),
            "velocity_limit_ratio": SAFETY_CONFIG.get("velocity_limit_ratio", 0.7),
            "collision_detection": True,
        }
    return {"torque_limit_ratio": 0.7, "velocity_limit_ratio": 0.7}


@app.put("/safety/config", tags=["安全"])
async def set_safety_config(config: SafetyConfig):
    if system_state["estop_triggered"]:
        raise HTTPException(status_code=400, detail="紧急停止状态下无法修改配置")
    system_state["safety_enabled"] = config.enable_collision_detection
    return {
        "status": "updated",
        "config": config.dict(),
    }


# ============================================================================
# 3. 运动控制接口
# ============================================================================
def _check_safety():
    if system_state["estop_triggered"]:
        raise HTTPException(status_code=400, detail="紧急停止已触发，拒绝运动")


@app.post("/motion/joint", tags=["运动控制"])
async def move_joint(cmd: JointCommand):
    _check_safety()
    if len(cmd.joints) < 6:
        raise HTTPException(status_code=400, detail="关节数量不足")
    system_state["current_joints"] = cmd.joints
    system_state["operation_count"] += 1
    command_history.append({
        "time": datetime.now().isoformat(),
        "type": "joint",
        "command": cmd.dict(),
    })
    return {"status": "accepted", "joints": cmd.joints, "speed": cmd.speed}


@app.post("/motion/cartesian", tags=["运动控制"])
async def move_cartesian(cmd: CartesianCommand):
    _check_safety()
    system_state["current_pose"] = {"x": cmd.x, "y": cmd.y, "z": cmd.z}
    system_state["operation_count"] += 1
    command_history.append({
        "time": datetime.now().isoformat(),
        "type": "cartesian",
        "command": cmd.dict(),
    })
    return {"status": "accepted", "pose": cmd.dict()}


@app.post("/motion/home", tags=["运动控制"])
async def go_home():
    _check_safety()
    home = [0.0, -1.57, 0.0, -1.57, 0.0, 0.0, 0.0]
    system_state["current_joints"] = home
    system_state["operation_count"] += 1
    return {"status": "moving_home", "joints": home}


@app.post("/motion/stop", tags=["运动控制"])
async def stop_motion():
    system_state["mode"] = "idle"
    return {"status": "stopped"}


# ============================================================================
# 4. 夹爪控制接口
# ============================================================================
@app.post("/gripper", tags=["夹爪控制"])
async def gripper_control(cmd: GripperCommand):
    _check_safety()
    if cmd.action not in ["open", "close"]:
        raise HTTPException(status_code=400, detail="动作必须是open或close")
    return {
        "status": "accepted",
        "action": cmd.action,
        "width": cmd.width,
        "force": cmd.force,
    }


# ============================================================================
# 5. 模型接口
# ============================================================================
@app.get("/models", tags=["模型管理"])
async def list_models():
    models_dir = os.path.dirname(os.path.abspath(__file__))
    models = []
    for f in os.listdir(models_dir):
        if f.startswith("ppo_") and f.endswith(".zip"):
            path = os.path.join(models_dir, f)
            models.append({
                "name": f.replace(".zip", ""),
                "size_kb": round(os.path.getsize(path) / 1024, 1),
                "modified": datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
            })
    return {"models": models, "count": len(models)}


@app.get("/models/{name}/validate", tags=["模型管理"])
async def validate_model(name: str):
    try:
        from stable_baselines3 import PPO
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
        model = PPO.load(path, device="cpu")
        return {
            "valid": True,
            "name": name,
            "observation_space": str(model.observation_space),
            "action_space": str(model.action_space),
        }
    except Exception as e:
        return {"valid": False, "name": name, "error": str(e)}


# ============================================================================
# 6. 日志接口
# ============================================================================
@app.get("/logs/commands", tags=["日志"])
async def get_command_log(limit: int = 100):
    return {
        "total": len(command_history),
        "commands": command_history[-limit:],
    }


@app.get("/logs/errors", tags=["日志"])
async def get_error_log():
    return {
        "error_count": system_state["error_count"],
        "last_error": system_state["last_error"],
    }


# ============================================================================
# 启动入口
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("ROBOT_API_PORT", "8000"))
    print(f"🚀 启动机器人API服务器: http://localhost:{port}")
    print(f"📖 API文档: http://localhost:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)
