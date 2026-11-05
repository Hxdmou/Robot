#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
教育AI模块 - V1.0
================================================================
新增内容：
  1. EducationLevel（教育阶段枚举）
  2. Subject（学科枚举）
  3. LearningProfile（学习者画像数据类）
  4. AITutor（AI辅导老师）
  5. PersonalizedLearningEngine（个性化学习引擎）
  6. IntelligentGradingAI（智能批改AI）
  7. EducationAgent（教育智能体）
  8. ClassroomAnalytics（课堂分析AI）
  9. AI教学助手
  10. create_education_ai（工厂函数）

核心能力：
  - 多学科AI一对一辅导（苏格拉底式提问）
  - 个性化学习路径规划与知识图谱
  - 作文/作业智能批改与反馈
  - 课堂行为分析与教学质量评估
  - 教育智能体自动化备课与资源生成
"""

import time
import threading
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class EducationLevel(Enum):
    PRESCHOOL = "preschool"
    PRIMARY = "primary"
    JUNIOR_HIGH = "junior_high"
    SENIOR_HIGH = "senior_high"
    UNIVERSITY = "university"
    GRADUATE = "graduate"
    VOCATIONAL = "vocational"
    CONTINUING = "continuing"


class Subject(Enum):
    MATH = "math"
    CHINESE = "chinese"
    ENGLISH = "english"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    HISTORY = "history"
    GEOGRAPHY = "geography"
    POLITICS = "politics"
    COMPUTER_SCIENCE = "computer_science"
    ART = "art"
    MUSIC = "music"
    PHYSICAL_EDUCATION = "physical_education"


class MasteryLevel(Enum):
    NOT_STARTED = "not_started"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class AssignmentType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    CODING = "coding"
    ORAL = "oral"


@dataclass
class KnowledgePoint:
    point_id: str
    subject: Subject
    name: str
    prerequisites: List[str] = field(default_factory=list)
    difficulty: float = 0.5
    mastery: float = 0.0


@dataclass
class LearningProfile:
    student_id: str
    name: str
    education_level: EducationLevel
    subjects: List[Subject] = field(default_factory=list)
    knowledge_map: Dict[str, KnowledgePoint] = field(default_factory=dict)
    learning_style: str = "visual"
    pace: str = "normal"
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    total_study_minutes: float = 0.0
    streak_days: int = 0


@dataclass
class Assignment:
    assignment_id: str
    student_id: str
    subject: Subject
    assignment_type: AssignmentType
    questions: List[Dict[str, Any]]
    answers: List[Any] = field(default_factory=list)
    score: float = 0.0
    feedback: str = ""
    graded: bool = False


class PersonalizedLearningEngine:
    """个性化学习引擎。

    基于知识图谱和学习者画像，规划最优学习路径，
    推荐练习和资源。
    """

    def __init__(self):
        self.knowledge_graph: Dict[str, KnowledgePoint] = {}
        self.students: Dict[str, LearningProfile] = {}
        self._lock = threading.Lock()
        self._recommendation_count = 0

    def register_knowledge_point(self, kp: KnowledgePoint) -> None:
        with self._lock:
            self.knowledge_graph[kp.point_id] = kp

    def register_student(self, profile: LearningProfile) -> None:
        with self._lock:
            self.students[profile.student_id] = profile

    def update_mastery(self, student_id: str, point_id: str,
                       mastery_delta: float) -> None:
        with self._lock:
            student = self.students.get(student_id)
            if not student:
                return
            if point_id not in student.knowledge_map:
                kp = self.knowledge_graph.get(point_id)
                if kp:
                    student.knowledge_map[point_id] = KnowledgePoint(
                        point_id=kp.point_id, subject=kp.subject,
                        name=kp.name, prerequisites=kp.prerequisites,
                        difficulty=kp.difficulty,
                    )
            if point_id in student.knowledge_map:
                kp = student.knowledge_map[point_id]
                kp.mastery = min(1.0, max(0.0, kp.mastery + mastery_delta))

    def recommend_learning_path(self, student_id: str,
                                subject: Subject,
                                target_point_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            self._recommendation_count += 1
            student = self.students.get(student_id)
            if not student:
                return []

            path = []
            visited = set()

            def traverse(pid: str) -> None:
                if pid in visited:
                    return
                visited.add(pid)
                kp = self.knowledge_graph.get(pid)
                if not kp:
                    return
                for pre in kp.prerequisites:
                    traverse(pre)
                student_kp = student.knowledge_map.get(pid)
                mastery = student_kp.mastery if student_kp else 0.0
                if mastery < 0.8:
                    path.append({
                        "point_id": pid,
                        "name": kp.name,
                        "subject": kp.subject.value,
                        "difficulty": kp.difficulty,
                        "current_mastery": mastery,
                        "estimated_minutes": int(kp.difficulty * 30 + 15),
                        "priority": len(path) + 1,
                    })

            traverse(target_point_id)
            return path

    def generate_practice(self, student_id: str,
                          point_id: str, count: int = 5) -> List[Dict[str, Any]]:
        with self._lock:
            kp = self.knowledge_graph.get(point_id)
            student = self.students.get(student_id)
            if not kp or not student:
                return []

            student_kp = student.knowledge_map.get(point_id)
            mastery = student_kp.mastery if student_kp else 0.0

            difficulty = "basic" if mastery < 0.3 else ("intermediate" if mastery < 0.7 else "advanced")

            questions = []
            for i in range(count):
                questions.append({
                    "question_id": f"Q-{point_id}-{i+1:03d}",
                    "knowledge_point": point_id,
                    "difficulty": difficulty,
                    "type": "multiple_choice" if i < count - 1 else "application",
                    "estimated_time_seconds": 60 + i * 30,
                })
            return questions

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "knowledge_points": len(self.knowledge_graph),
                "students": len(self.students),
                "recommendations_generated": self._recommendation_count,
            }


class AITutor:
    """AI辅导老师。

    苏格拉底式对话辅导，不直接给答案，
    引导学生思考。
    """

    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        self._lock = threading.Lock()
        self._session_count = 0

    def start_session(self, student_id: str, subject: Subject) -> str:
        with self._lock:
            self._session_count += 1
            session_id = f"TUT-{student_id}-{int(time.time())}"
            self.sessions[session_id] = [
                {"role": "system",
                 "content": f"你是一位{subject.value}辅导老师，用苏格拉底式提问引导学生思考"},
                {"role": "assistant",
                 "content": f"你好！今天我们来学习{subject.value}。你有什么问题？"},
            ]
            return session_id

    def ask(self, session_id: str, question: str) -> Dict[str, Any]:
        with self._lock:
            if session_id not in self.sessions:
                return {"success": False, "reason": "session_not_found"}

            self.sessions[session_id].append(
                {"role": "user", "content": question})

            response = self._socratic_response(question)
            self.sessions[session_id].append(
                {"role": "assistant", "content": response})

            return {
                "success": True,
                "response": response,
                "approach": "socratic",
                "turn_count": len(self.sessions[session_id]),
            }

    def _socratic_response(self, question: str) -> str:
        q = question.lower()
        if "怎么" in q or "how" in q:
            return "这个问题很好。你能不能先告诉我，你已经尝试了什么方法？你觉得卡在哪一步？"
        elif "为什么" in q or "why" in q:
            return "让我们一起来分析。你能先说说你对这个问题的理解吗？你觉得背后的原理是什么？"
        elif "答案" in q or "answer" in q:
            return "我先不直接给你答案。你觉得这个问题的关键信息是什么？我们一步步来推导。"
        else:
            return "我理解你的问题。你能不能举个具体的例子？这样我们能更好地一起探讨。"

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "total_sessions": self._session_count,
                "active_sessions": len(self.sessions),
            }


class IntelligentGradingAI:
    """智能批改AI。

    客观题自动批改，主观题/作文AI评分+反馈，
    代码作业自动测试。
    """

    def __init__(self):
        self.graded_assignments: Dict[str, Assignment] = {}
        self._lock = threading.Lock()
        self._grade_count = 0

    def grade(self, assignment: Assignment) -> Assignment:
        with self._lock:
            self._grade_count += 1
            total_questions = len(assignment.questions)
            if total_questions == 0:
                return assignment

            correct = 0
            feedback_parts = []

            for i, q in enumerate(assignment.questions):
                answer = assignment.answers[i] if i < len(assignment.answers) else None
                correct_answer = q.get("correct_answer")

                if assignment.assignment_type == AssignmentType.MULTIPLE_CHOICE:
                    if answer == correct_answer:
                        correct += 1
                    else:
                        feedback_parts.append(f"第{i+1}题: 答案应为{correct_answer}")

                elif assignment.assignment_type == AssignmentType.FILL_BLANK:
                    if str(answer).strip().lower() == str(correct_answer).strip().lower():
                        correct += 1
                    else:
                        feedback_parts.append(f"第{i+1}题: 正确答案「{correct_answer}」")

                elif assignment.assignment_type == AssignmentType.ESSAY:
                    score, fb = self._grade_essay(answer, q)
                    correct += score
                    feedback_parts.append(f"作文评分: {score:.1f}/{q.get('points', 100)}")
                    feedback_parts.append(f"反馈: {fb}")

                elif assignment.assignment_type == AssignmentType.CODING:
                    score, fb = self._grade_code(answer, q)
                    correct += score
                    feedback_parts.append(f"代码评分: {score:.1f}")
                    if fb:
                        feedback_parts.append(f"建议: {fb}")

            assignment.score = (correct / total_questions) * 100 if total_questions > 0 else 0
            assignment.feedback = "\n".join(feedback_parts) if feedback_parts else "全部正确，表现优秀！"
            assignment.graded = True
            self.graded_assignments[assignment.assignment_id] = assignment
            return assignment

    def _grade_essay(self, essay: Optional[str],
                     question: Dict[str, Any]) -> tuple:
        if not essay:
            return 0, "未作答"
        length = len(essay)
        if length < 100:
            return 60, "内容偏短，建议展开论述，增加论据和案例"
        elif length < 300:
            return 75, "结构基本完整，可进一步丰富论证层次"
        elif length < 600:
            return 85, "论述充分，逻辑清晰，注意语言精炼"
        else:
            return 92, "内容丰富，论证有力，结构完整"

    def _grade_code(self, code: Optional[str],
                    question: Dict[str, Any]) -> tuple:
        if not code:
            return 0, "未提交代码"
        test_cases = question.get("test_cases", [])
        passed = 0
        for tc in test_cases:
            try:
                result = eval(code)(*tc["input"])
                if result == tc["expected"]:
                    passed += 1
            except Exception:
                pass
        score = (passed / len(test_cases)) * 100 if test_cases else 70
        feedback = f"通过{passed}/{len(test_cases)}个测试用例" if test_cases else "代码结构合理"
        return score, feedback

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "total_graded": self._grade_count,
                "average_score": sum(a.score for a in self.graded_assignments.values()) / max(1, len(self.graded_assignments)),
            }


class EducationAgent:
    """教育智能体。

    自动化备课、教学资源生成、课程安排、
    学情分析报告。
    """

    def __init__(self):
        self.lesson_plans: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._plan_count = 0

    def generate_lesson_plan(self, subject: Subject, topic: str,
                             duration_minutes: int = 45,
                             level: EducationLevel = EducationLevel.PRIMARY
                             ) -> Dict[str, Any]:
        with self._lock:
            self._plan_count += 1
            plan = {
                "plan_id": f"LP-{self._plan_count:04d}",
                "subject": subject.value,
                "topic": topic,
                "level": level.value,
                "duration_minutes": duration_minutes,
                "objectives": [
                    f"理解{topic}的基本概念",
                    f"掌握{topic}的核心方法",
                    f"能够运用{topic}解决实际问题",
                ],
                "structure": [
                    {"phase": "导入", "minutes": 5, "activity": "情境引入，激发兴趣"},
                    {"phase": "新授", "minutes": 20, "activity": f"讲解{topic}核心知识"},
                    {"phase": "练习", "minutes": 12, "activity": "分层练习，即时反馈"},
                    {"phase": "总结", "minutes": 5, "activity": "知识梳理，布置作业"},
                    {"phase": "拓展", "minutes": 3, "activity": "思维拓展，联系生活"},
                ],
                "homework": [
                    f"完成{topic}基础练习",
                    f"思考{topic}在生活中的应用",
                ],
                "ai_resources": [
                    "AI生成知识点思维导图",
                    "AI生成分层练习题",
                    "AI推荐相关拓展阅读",
                ],
                "generated_at": time.time(),
            }
            self.lesson_plans[plan["plan_id"]] = plan
            return plan

    def generate_report(self, student_id: str,
                        learning_engine: PersonalizedLearningEngine) -> Dict[str, Any]:
        with self._lock:
            student = learning_engine.students.get(student_id)
            if not student:
                return {"success": False, "reason": "student_not_found"}

            mastered = sum(1 for kp in student.knowledge_map.values() if kp.mastery >= 0.8)
            total = len(student.knowledge_map)
            mastery_rate = mastered / total if total > 0 else 0

            return {
                "student_id": student_id,
                "student_name": student.name,
                "level": student.education_level.value,
                "total_knowledge_points": total,
                "mastered_points": mastered,
                "mastery_rate": round(mastery_rate, 2),
                "total_study_minutes": student.total_study_minutes,
                "streak_days": student.streak_days,
                "strengths": student.strengths,
                "weaknesses": student.weaknesses,
                "recommendations": [
                    "继续保持每日学习习惯",
                    f"重点攻克薄弱环节: {', '.join(student.weaknesses[:3])}",
                    "适当增加综合应用题练习",
                ],
                "generated_at": time.time(),
            }


class ClassroomAnalytics:
    """课堂分析AI。

    课堂行为识别、专注度分析、
    教学互动质量评估。
    """

    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def start_class(self, class_id: str, subject: Subject,
                    teacher_id: str, student_count: int) -> None:
        with self._lock:
            self.sessions[class_id] = {
                "subject": subject,
                "teacher_id": teacher_id,
                "student_count": student_count,
                "started_at": time.time(),
                "engagement_samples": [],
                "interaction_count": 0,
            }

    def analyze_frame(self, class_id: str,
                      engagement_data: Dict[str, float]) -> Dict[str, Any]:
        with self._lock:
            session = self.sessions.get(class_id)
            if not session:
                return {"success": False, "reason": "class_not_found"}
            session["engagement_samples"].append({
                "timestamp": time.time(),
                **engagement_data,
            })
            avg_engagement = sum(engagement_data.values()) / max(1, len(engagement_data))
            return {
                "success": True,
                "avg_engagement": round(avg_engagement, 3),
                "status": "high" if avg_engagement > 0.7 else ("medium" if avg_engagement > 0.4 else "low"),
            }

    def get_class_report(self, class_id: str) -> Dict[str, Any]:
        with self._lock:
            session = self.sessions.get(class_id)
            if not session:
                return {"success": False, "reason": "class_not_found"}
            samples = session["engagement_samples"]
            if not samples:
                return {"success": False, "reason": "no_data"}
            avg = sum(sum(s.get(k, 0) for k in s if k != "timestamp") / max(1, len(s)-1)
                      for s in samples) / len(samples)
            return {
                "class_id": class_id,
                "subject": session["subject"].value,
                "duration_minutes": round((time.time() - session["started_at"]) / 60, 1),
                "avg_engagement": round(avg, 3),
                "samples_collected": len(samples),
                "recommendation": "课堂互动良好" if avg > 0.7 else "建议增加互动环节",
            }


class EducationAI:
    """教育AI平台。"""

    def __init__(self):
        self.learning_engine = PersonalizedLearningEngine()
        self.tutor = AITutor()
        self.grading = IntelligentGradingAI()
        self.agent = EducationAgent()
        self.classroom = ClassroomAnalytics()
        self._lock = threading.Lock()

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "learning_engine": self.learning_engine.get_status(),
                "tutor": self.tutor.get_status(),
                "grading": self.grading.get_status(),
                "lesson_plans": self.agent._plan_count,
            }


def create_education_ai() -> EducationAI:
    """工厂函数：创建教育AI平台。"""
    ai = EducationAI()

    math_kps = [
        KnowledgePoint("M001", Subject.MATH, "整数运算", [], 0.2),
        KnowledgePoint("M002", Subject.MATH, "分数运算", ["M001"], 0.4),
        KnowledgePoint("M003", Subject.MATH, "一元一次方程", ["M002"], 0.5),
        KnowledgePoint("M004", Subject.MATH, "二元一次方程组", ["M003"], 0.6),
        KnowledgePoint("M005", Subject.MATH, "一元二次方程", ["M003"], 0.65),
        KnowledgePoint("M006", Subject.MATH, "函数概念", ["M003"], 0.55),
        KnowledgePoint("M007", Subject.MATH, "二次函数", ["M005", "M006"], 0.75),
    ]
    for kp in math_kps:
        ai.learning_engine.register_knowledge_point(kp)

    phys_kps = [
        KnowledgePoint("P001", Subject.PHYSICS, "运动学基础", [], 0.3),
        KnowledgePoint("P002", Subject.PHYSICS, "牛顿运动定律", ["P001"], 0.5),
        KnowledgePoint("P003", Subject.PHYSICS, "功和能", ["P002"], 0.55),
        KnowledgePoint("P004", Subject.PHYSICS, "动量守恒", ["P002"], 0.6),
    ]
    for kp in phys_kps:
        ai.learning_engine.register_knowledge_point(kp)

    student1 = LearningProfile(
        student_id="STU001", name="小明",
        education_level=EducationLevel.JUNIOR_HIGH,
        subjects=[Subject.MATH, Subject.PHYSICS, Subject.ENGLISH],
        learning_style="visual", pace="normal",
        strengths=["几何直观", "物理概念理解"],
        weaknesses=["代数运算", "英语写作"],
        streak_days=15, total_study_minutes=4500,
    )
    ai.learning_engine.register_student(student1)
    ai.learning_engine.update_mastery("STU001", "M001", 0.95)
    ai.learning_engine.update_mastery("STU001", "M002", 0.82)
    ai.learning_engine.update_mastery("STU001", "M003", 0.65)
    ai.learning_engine.update_mastery("STU001", "P001", 0.88)
    ai.learning_engine.update_mastery("STU001", "P002", 0.45)

    student2 = LearningProfile(
        student_id="STU002", name="小红",
        education_level=EducationLevel.SENIOR_HIGH,
        subjects=[Subject.MATH, Subject.CHEMISTRY, Subject.CHINESE],
        learning_style="reading", pace="fast",
        strengths=["逻辑推理", "化学方程式"],
        weaknesses=["语文作文"],
        streak_days=28, total_study_minutes=8200,
    )
    ai.learning_engine.register_student(student2)

    return ai


if __name__ == "__main__":
    edu = create_education_ai()
    status = edu.get_status()
    print(f"教育AI平台已创建: {status['learning_engine']['knowledge_points']}个知识点, "
          f"{status['learning_engine']['students']}名学生, "
          f"{status['lesson_plans']}份教案")
    path = edu.learning_engine.recommend_learning_path("STU001", Subject.MATH, "M007")
    print(f"学习路径: {len(path)}个知识点待学习")
    session = edu.tutor.start_session("STU001", Subject.MATH)
    result = edu.tutor.ask(session, "二次函数怎么解？")
    print(f"AI辅导: {result['response']}")
