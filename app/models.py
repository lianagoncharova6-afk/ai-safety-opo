"""
SQLAlchemy модели — 17 таблиц.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    DateTime,
    Date,
    ForeignKey,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from app.database import Base


class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    inn = Column(String(12), nullable=False, unique=True)
    ogrn = Column(String(13))
    legal_address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    objects = relationship("ObjectOkpo", back_populates="organization", cascade="all, delete")


class ObjectOkpo(Base):
    __tablename__ = "object_okpo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    okpo_code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(500), nullable=False)
    address = Column(Text)
    danger_class = Column(String(4), nullable=False)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    coordinates = Column(String(50))
    h2s_content_percent = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="objects")
    permits = relationship("WorkPermit", back_populates="object_okpo", cascade="all, delete")

    __table_args__ = (
        CheckConstraint("danger_class IN ('I', 'II', 'III', 'IV')", name="ck_obj_danger_class"),
    )


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(300), nullable=False)
    position = Column(String(200))
    qualification = Column(String(200))
    safety_group = Column(String(10))
    brief_date = Column(Date)
    brief_type = Column(String(100))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Ppe(Base):
    __tablename__ = "ppe"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(300), nullable=False)
    type = Column(String(100), nullable=False)
    description = Column(Text)
    standard = Column(String(200))
    required_for = Column(Text)
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)


class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(300), nullable=False)
    type = Column(String(100), nullable=False)
    description = Column(Text)
    last_check_date = Column(Date)
    is_critical = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SafetySign(Base):
    __tablename__ = "safety_sign"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(300), nullable=False)
    category = Column(String(100))
    image_url = Column(String(500))
    description = Column(Text)
    required_for = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class ActivityType(Base):
    __tablename__ = "activity_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(300), nullable=False)
    description = Column(Text)
    danger_category = Column(String(100))
    requires_permit = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    permits = relationship("WorkPermit", back_populates="activity_type")


class WorkPermit(Base):
    __tablename__ = "work_permit"
    id = Column(Integer, primary_key=True, autoincrement=True)
    permit_number = Column(String(50), nullable=False, unique=True)
    permit_type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="draft", index=True)
    object_okpo_id = Column(Integer, ForeignKey("object_okpo.id"), nullable=False)
    activity_type_id = Column(Integer, ForeignKey("activity_type.id"))
    responsible_person_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    work_manager_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    work_description = Column(Text, nullable=False)
    work_start_date = Column(DateTime, nullable=False)
    work_end_date = Column(DateTime, nullable=False)
    daily_extension = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime)

    object_okpo = relationship("ObjectOkpo", back_populates="permits")
    activity_type = relationship("ActivityType", back_populates="permits")
    responsible_person = relationship("Employee", foreign_keys=[responsible_person_id])
    work_manager = relationship("Employee", foreign_keys=[work_manager_id])
    crew = relationship("PermitCrew", back_populates="permit", cascade="all, delete")
    ppe_list = relationship("PermitPpe", back_populates="permit", cascade="all, delete")
    equipment_list = relationship("PermitEquipment", back_populates="permit", cascade="all, delete")
    violations = relationship("Violation", back_populates="permit", cascade="all, delete")
    gas_monitors = relationship("GasMonitor", back_populates="permit", cascade="all, delete")
    risk_entries = relationship("RiskMatrix", back_populates="permit", cascade="all, delete")
    checklists = relationship("PermitChecklist", back_populates="permit", cascade="all, delete")

    __table_args__ = (
        CheckConstraint(
            "permit_type IN ('gas_hazard', 'fire', 'repair', 'combined')",
            name="ck_permit_type",
        ),
        CheckConstraint(
            "status IN ('draft', 'active', 'suspended', 'closed')",
            name="ck_permit_status",
        ),
        Index("idx_work_permit_dates", "work_start_date", "work_end_date"),
    )


class PermitCrew(Base):
    __tablename__ = "permit_crew"
    id = Column(Integer, primary_key=True, autoincrement=True)
    permit_id = Column(Integer, ForeignKey("work_permit.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    role = Column(String(100))
    brief_date = Column(Date)
    signature = Column(Boolean, default=False)

    permit = relationship("WorkPermit", back_populates="crew")
    employee = relationship("Employee")


class PermitPpe(Base):
    __tablename__ = "permit_ppe"
    id = Column(Integer, primary_key=True, autoincrement=True)
    permit_id = Column(Integer, ForeignKey("work_permit.id"), nullable=False)
    ppe_id = Column(Integer, ForeignKey("ppe.id"), nullable=False)
    quantity = Column(Integer, default=1)
    check_result = Column(Boolean)

    permit = relationship("WorkPermit", back_populates="ppe_list")
    ppe = relationship("Ppe")


class PermitEquipment(Base):
    __tablename__ = "permit_equipment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    permit_id = Column(Integer, ForeignKey("work_permit.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    check_result = Column(Boolean)
    notes = Column(Text)

    permit = relationship("WorkPermit", back_populates="equipment_list")
    equipment = relationship("Equipment")


class Violation(Base):
    __tablename__ = "violation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    permit_id = Column(Integer, ForeignKey("work_permit.id"), nullable=False, index=True)
    violation_type = Column(String(50), nullable=False, index=True)
    severity = Column(Integer, nullable=False, default=1)
    probability = Column(Integer, nullable=False, default=1)
    risk_level = Column(Integer, nullable=False, default=1)
    detected_by_ai = Column(Boolean, default=True)
    camera_id = Column(String(50))
    image_snapshot_url = Column(String(500))
    status = Column(String(20), default="new")
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    resolution_notes = Column(Text)

    permit = relationship("WorkPermit", back_populates="violations")

    __table_args__ = (
        CheckConstraint("severity BETWEEN 1 AND 5", name="ck_viol_severity"),
        CheckConstraint("probability BETWEEN 1 AND 5", name="ck_viol_probability"),
        CheckConstraint("risk_level BETWEEN 1 AND 25", name="ck_viol_risk"),
        CheckConstraint(
            "status IN ('new', 'acknowledged', 'resolved', 'false_alarm')",
            name="ck_viol_status",
        ),
        Index("idx_violation_permit", "permit_id", "detected_at"),
    )


class GasMonitor(Base):
    __tablename__ = "gas_monitor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    permit_id = Column(Integer, ForeignKey("work_permit.id"), nullable=False, index=True)
    monitor_time = Column(DateTime, default=datetime.utcnow)
    o2_level = Column(Float)
    h2s_level = Column(Float)
    ch4_level = Column(Float)
    co_level = Column(Float)
    temperature = Column(Float)
    is_alarm = Column(Boolean, default=False)
    notes = Column(Text)

    permit = relationship("WorkPermit", back_populates="gas_monitors")

    __table_args__ = (Index("idx_gas_monitor_permit", "permit_id", "monitor_time"),)


class RiskMatrix(Base):
    __tablename__ = "risk_matrix"
    id = Column(Integer, primary_key=True, autoincrement=True)
    permit_id = Column(Integer, ForeignKey("work_permit.id"), nullable=False, index=True)
    hazard_description = Column(Text, nullable=False)
    probability = Column(Integer, nullable=False)
    severity = Column(Integer, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_category = Column(String(20), nullable=False)
    mitigation_measures = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    permit = relationship("WorkPermit", back_populates="risk_entries")

    __table_args__ = (
        CheckConstraint("probability BETWEEN 1 AND 5", name="ck_rm_probability"),
        CheckConstraint("severity BETWEEN 1 AND 5", name="ck_rm_severity"),
        CheckConstraint("risk_score BETWEEN 1 AND 25", name="ck_rm_score"),
        CheckConstraint(
            "risk_category IN ('low', 'medium', 'high', 'critical')",
            name="ck_rm_category",
        ),
    )


class ChecklistItem(Base):
    __tablename__ = "checklist_item"
    id = Column(Integer, primary_key=True, autoincrement=True)
    section = Column(String(200), nullable=False)
    item_number = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    normative_ref = Column(String(300))
    is_required = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class PermitChecklist(Base):
    __tablename__ = "permit_checklist"
    id = Column(Integer, primary_key=True, autoincrement=True)
    permit_id = Column(Integer, ForeignKey("work_permit.id"), nullable=False, index=True)
    checklist_item_id = Column(Integer, ForeignKey("checklist_item.id"), nullable=False)
    is_compliant = Column(Boolean)
    notes = Column(Text)
    checked_by = Column(String(200))
    checked_at = Column(DateTime)

    permit = relationship("WorkPermit", back_populates="checklists")
    checklist_item = relationship("ChecklistItem")


class ExportLog(Base):
    __tablename__ = "export_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    export_type = Column(String(100), nullable=False)
    file_path = Column(String(500))
    created_by = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
