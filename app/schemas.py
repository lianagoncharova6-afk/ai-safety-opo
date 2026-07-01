"""
Pydantic схемы для валидации входных/выходных данных.
"""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field


# ---------- Organization ----------
class OrganizationBase(BaseModel):
    name: str = Field(..., max_length=500)
    inn: str = Field(..., max_length=12)
    ogrn: Optional[str] = None
    legal_address: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationOut(OrganizationBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


# ---------- ObjectOkpo ----------
class ObjectOkpoBase(BaseModel):
    okpo_code: str = Field(..., max_length=10)
    name: str = Field(..., max_length=500)
    address: Optional[str] = None
    danger_class: str
    organization_id: int
    coordinates: Optional[str] = None
    h2s_content_percent: float = 0.0


class ObjectOkpoCreate(ObjectOkpoBase):
    pass


class ObjectOkpoOut(ObjectOkpoBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


# ---------- Employee ----------
class EmployeeBase(BaseModel):
    full_name: str = Field(..., max_length=300)
    position: Optional[str] = None
    qualification: Optional[str] = None
    safety_group: Optional[str] = None
    brief_date: Optional[date] = None
    brief_type: Optional[str] = None
    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeOut(EmployeeBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


# ---------- PPE ----------
class PpeBase(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=300)
    type: str = Field(..., max_length=100)
    description: Optional[str] = None
    standard: Optional[str] = None
    required_for: Optional[str] = None
    image_url: Optional[str] = None


class PpeCreate(PpeBase):
    pass


class PpeOut(PpeBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


# ---------- Equipment ----------
class EquipmentBase(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=300)
    type: str = Field(..., max_length=100)
    description: Optional[str] = None
    last_check_date: Optional[date] = None
    is_critical: bool = False


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentOut(EquipmentBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


# ---------- SafetySign ----------
class SafetySignBase(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=300)
    category: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    required_for: Optional[str] = None


class SafetySignCreate(SafetySignBase):
    pass


class SafetySignOut(SafetySignBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


# ---------- ActivityType ----------
class ActivityTypeBase(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=300)
    description: Optional[str] = None
    danger_category: Optional[str] = None
    requires_permit: bool = True


class ActivityTypeCreate(ActivityTypeBase):
    pass


class ActivityTypeOut(ActivityTypeBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


# ---------- WorkPermit ----------
class WorkPermitCreate(BaseModel):
    permit_number: str = Field(..., max_length=50)
    permit_type: str = Field(..., pattern=r"^(gas_hazard|fire|repair|combined)$")
    object_okpo_id: int
    activity_type_id: Optional[int] = None
    responsible_person_id: int
    work_manager_id: int
    work_description: str
    work_start_date: datetime
    work_end_date: datetime
    daily_extension: bool = False


class WorkPermitUpdate(BaseModel):
    status: Optional[str] = None
    work_description: Optional[str] = None
    daily_extension: Optional[bool] = None


class WorkPermitOut(BaseModel):
    id: int
    permit_number: str
    permit_type: str
    status: str
    object_okpo_id: int
    activity_type_id: Optional[int] = None
    responsible_person_id: int
    work_manager_id: int
    work_description: str
    work_start_date: datetime
    work_end_date: datetime
    daily_extension: bool
    created_at: datetime
    closed_at: Optional[datetime] = None
    model_config = {"from_attributes": True}


# ---------- Violation ----------
class ViolationCreate(BaseModel):
    permit_id: int
    violation_type: str
    severity: int = Field(default=1, ge=1, le=5)
    probability: int = Field(default=1, ge=1, le=5)
    detected_by_ai: bool = True
    camera_id: Optional[str] = None
    image_snapshot_url: Optional[str] = None


class ViolationOut(BaseModel):
    id: int
    permit_id: int
    violation_type: str
    severity: int
    probability: int
    risk_level: int
    detected_by_ai: bool
    camera_id: Optional[str] = None
    status: str
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    model_config = {"from_attributes": True}


# ---------- RiskMatrix ----------
class RiskMatrixOut(BaseModel):
    id: int
    permit_id: int
    hazard_description: str
    probability: int
    severity: int
    risk_score: int
    risk_category: str
    mitigation_measures: Optional[str] = None
    created_at: datetime
    model_config = {"from_attributes": True}


# ---------- ChecklistItem ----------
class ChecklistItemCreate(BaseModel):
    section: str = Field(..., max_length=200)
    item_number: str = Field(..., max_length=20)
    description: str
    normative_ref: Optional[str] = None
    is_required: bool = True


class ChecklistItemOut(ChecklistItemCreate):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


# ---------- GasMonitor ----------
class GasMonitorCreate(BaseModel):
    permit_id: int
    o2_level: Optional[float] = None
    h2s_level: Optional[float] = None
    ch4_level: Optional[float] = None
    co_level: Optional[float] = None
    temperature: Optional[float] = None
    is_alarm: bool = False
    notes: Optional[str] = None


class GasMonitorOut(GasMonitorCreate):
    id: int
    monitor_time: datetime
    model_config = {"from_attributes": True}


# ---------- Dashboard ----------
class DashboardStats(BaseModel):
    total_permits: int
    active_permits: int
    total_violations: int
    violations_by_type: dict
    violations_by_severity: dict
    risk_distribution: dict
