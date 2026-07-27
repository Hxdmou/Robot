"""
模型版本管理工具
功能：
  1. 模型导出（SB3 → 标准化格式）
  2. 模型版本注册与管理
  3. 模型加载（指定版本或最新版）
  4. 模型回滚（到上一个稳定版本）
  5. 模型元数据记录（训练参数、准确率、训练时间等）

使用方法：
  # 注册一个新模型版本
  python model_manager.py --register path/to/model.zip --name v1.0 --notes "初始版本"

  # 列出所有模型版本
  python model_manager.py --list

  # 加载指定版本
  python model_manager.py --load v1.0

  # 回滚到上一版本
  python model_manager.py --rollback

  # 设置默认部署版本
  python model_manager.py --set-default v1.0
"""

import os
import sys
import json
import shutil
import argparse
import time
from datetime import datetime
from typing import Optional, Dict, Any, List


class ModelVersion:
    """模型版本数据结构"""

    def __init__(self, version_id: str, name: str, model_path: str,
                 created_at: str = None, metrics: Dict[str, Any] = None,
                 notes: str = "", is_default: bool = False):
        self.version_id = version_id
        self.name = name
        self.model_path = model_path
        self.created_at = created_at or datetime.now().isoformat()
        self.metrics = metrics or {}
        self.notes = notes
        self.is_default = is_default

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version_id": self.version_id,
            "name": self.name,
            "model_path": self.model_path,
            "created_at": self.created_at,
            "metrics": self.metrics,
            "notes": self.notes,
            "is_default": self.is_default,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelVersion":
        return cls(
            version_id=data["version_id"],
            name=data["name"],
            model_path=data["model_path"],
            created_at=data.get("created_at"),
            metrics=data.get("metrics", {}),
            notes=data.get("notes", ""),
            is_default=data.get("is_default", False),
        )


class ModelManager:
    """模型版本管理器"""

    def __init__(self, storage_dir: str = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.storage_dir = storage_dir or os.path.join(base_dir, "model_registry")
        self.models_dir = os.path.join(self.storage_dir, "models")
        self.index_file = os.path.join(self.storage_dir, "model_index.json")

        os.makedirs(self.models_dir, exist_ok=True)

        self._versions: Dict[str, ModelVersion] = {}
        self._default_version: Optional[str] = None
        self._load_index()

    def _load_index(self):
        """从磁盘加载模型索引"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._versions = {
                    v["version_id"]: ModelVersion.from_dict(v)
                    for v in data.get("versions", [])
                }
                self._default_version = data.get("default_version")
            except Exception as e:
                print(f"[MODEL] 警告: 加载索引失败: {e}")
                self._versions = {}
                self._default_version = None

    def _save_index(self):
        """保存模型索引到磁盘"""
        data = {
            "versions": [v.to_dict() for v in self._versions.values()],
            "default_version": self._default_version,
            "last_updated": datetime.now().isoformat(),
        }
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def register_model(self, model_path: str, name: str = None,
                       notes: str = "", metrics: Dict[str, Any] = None) -> ModelVersion:
        """注册一个新模型版本

        Args:
            model_path: 原始模型文件路径（.zip或目录）
            name: 版本名称（如 v1.0, v2.0-stable）
            notes: 版本说明
            metrics: 模型性能指标字典

        Returns:
            注册后的 ModelVersion 对象
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件不存在: {model_path}")

        version_id = f"v{len(self._versions) + 1:03d}_{int(time.time())}"
        name = name or version_id

        dst_path = os.path.join(self.models_dir, f"{version_id}.zip")

        if os.path.isdir(model_path):
            shutil.make_archive(dst_path.replace(".zip", ""), "zip", model_path)
        elif model_path.endswith(".zip"):
            shutil.copy2(model_path, dst_path)
        else:
            raise ValueError(f"不支持的模型格式: {model_path}")

        version = ModelVersion(
            version_id=version_id,
            name=name,
            model_path=dst_path,
            metrics=metrics or {},
            notes=notes,
            is_default=len(self._versions) == 0,
        )

        self._versions[version_id] = version
        if version.is_default:
            self._default_version = version_id

        self._save_index()
        print(f"[MODEL] ✅ 已注册版本: {name} ({version_id})")
        return version

    def get_version(self, version_id: str = None) -> Optional[ModelVersion]:
        """获取指定版本的模型

        Args:
            version_id: 版本ID或名称，None表示获取默认版本

        Returns:
            ModelVersion 对象或 None
        """
        if version_id is None:
            version_id = self._default_version

        if version_id is None:
            return None

        if version_id in self._versions:
            return self._versions[version_id]

        for v in self._versions.values():
            if v.name == version_id:
                return v

        return None

    def load_model(self, version_id: str = None, device: str = "cpu"):
        """加载指定版本的模型

        Args:
            version_id: 版本ID或名称，None表示默认版本
            device: 加载设备 (cpu/cuda)

        Returns:
            (model, version_info) 元组
        """
        from stable_baselines3 import PPO

        version = self.get_version(version_id)
        if version is None:
            raise ValueError(f"未找到模型版本: {version_id}")

        model = PPO.load(version.model_path, device=device)
        print(f"[MODEL] ✅ 已加载模型: {version.name} ({version.version_id})")
        return model, version.to_dict()

    def list_versions(self) -> List[ModelVersion]:
        """列出所有已注册的模型版本"""
        return sorted(self._versions.values(), key=lambda v: v.created_at, reverse=True)

    def set_default(self, version_id: str):
        """设置默认部署版本"""
        if version_id not in self._versions:
            for v in self._versions.values():
                if v.name == version_id:
                    version_id = v.version_id
                    break

        if version_id not in self._versions:
            raise ValueError(f"未找到版本: {version_id}")

        for v in self._versions.values():
            v.is_default = (v.version_id == version_id)

        self._default_version = version_id
        self._save_index()
        print(f"[MODEL] ✅ 默认版本已设置为: {self._versions[version_id].name}")

    def rollback(self) -> Optional[ModelVersion]:
        """回滚到上一个稳定版本

        Returns:
            回滚后的版本，None表示没有可回滚的版本
        """
        versions = self.list_versions()
        if len(versions) < 2:
            print("[MODEL] ⚠️ 没有可回滚的版本")
            return None

        prev = versions[1]  # 第二个最新版本
        self.set_default(prev.version_id)
        print(f"[MODEL] ✅ 已回滚到: {prev.name}")
        return prev

    def delete_version(self, version_id: str):
        """删除指定版本（不能删除默认版本）"""
        if version_id == self._default_version:
            raise ValueError("不能删除默认版本，请先设置其他版本为默认")

        if version_id not in self._versions:
            for v in self._versions.values():
                if v.name == version_id:
                    version_id = v.version_id
                    break

        if version_id not in self._versions:
            raise ValueError(f"未找到版本: {version_id}")

        version = self._versions[version_id]
        if os.path.exists(version.model_path):
            os.remove(version.model_path)

        del self._versions[version_id]
        self._save_index()
        print(f"[MODEL] ✅ 已删除版本: {version.name}")

    def print_versions_table(self):
        """以表格形式打印所有版本"""
        versions = self.list_versions()

        print("=" * 90)
        print(f"{'默认':<4} {'版本名称':<20} {'版本ID':<25} {'创建时间':<25} {'指标':<15}")
        print("-" * 90)

        for v in versions:
            default_mark = "★" if v.is_default else " "
            created = v.created_at[:19].replace("T", " ")
            metrics_str = ", ".join(f"{k}={v:.2f}" for k, v in list(v.metrics.items())[:2])
            print(f"{default_mark:<4} {v.name:<20} {v.version_id:<25} {created:<25} {metrics_str:<15}")
            if v.notes:
                print(f"     说明: {v.notes}")

        print("=" * 90)
        print(f"共 {len(versions)} 个版本，默认: {self._versions[self._default_version].name if self._default_version else '无'}")


def find_model_file(path: str = None) -> Optional[str]:
    """查找模型文件"""
    if path and os.path.exists(path):
        return path

    search_paths = [
        path or "ppo_robot_reach_curriculum.zip",
        os.path.join(os.path.dirname(__file__), "ppo_robot_reach_curriculum.zip"),
        r"f:\个人作品\具身智能\embodied-intelligence\ppo_robot_reach_curriculum.zip",
        r"f:\个人作品\具身智能\ppo_robot_reach_curriculum.zip",
    ]

    for p in search_paths:
        if os.path.exists(p):
            return p

    return None


def main():
    parser = argparse.ArgumentParser(description="模型版本管理工具")
    parser.add_argument("--register", help="注册模型: 指定模型文件路径")
    parser.add_argument("--name", help="版本名称 (如 v1.0)")
    parser.add_argument("--notes", default="", help="版本说明")
    parser.add_argument("--list", action="store_true", help="列出所有版本")
    parser.add_argument("--load", help="加载并验证指定版本")
    parser.add_argument("--set-default", help="设置默认部署版本")
    parser.add_argument("--rollback", action="store_true", help="回滚到上一版本")
    parser.add_argument("--delete", help="删除指定版本")
    parser.add_argument("--storage", help="模型仓库目录")

    args = parser.parse_args()

    manager = ModelManager(args.storage)

    if args.list:
        manager.print_versions_table()

    elif args.register:
        model_path = find_model_file(args.register)
        if not model_path:
            print(f"❌ 未找到模型文件: {args.register}")
            sys.exit(1)
        manager.register_model(model_path, args.name, args.notes)
        manager.print_versions_table()

    elif args.load:
        try:
            model, info = manager.load_model(args.load)
            print(f"✅ 模型加载成功: {info['name']}")
            print(f"   观测空间: {model.observation_space}")
            print(f"   动作空间: {model.action_space}")
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            sys.exit(1)

    elif args.set_default:
        manager.set_default(args.set_default)
        manager.print_versions_table()

    elif args.rollback:
        manager.rollback()
        manager.print_versions_table()

    elif args.delete:
        manager.delete_version(args.delete)
        manager.print_versions_table()

    else:
        parser.print_help()
        print("\n当前仓库状态:")
        manager.print_versions_table()


if __name__ == "__main__":
    main()
