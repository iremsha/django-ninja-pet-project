from datetime import date

from api.internal.dto.equipment import BorrowEquipmentData
from api.internal.service.equipment import EquipmentService
from api.internal.transport.rest.equipment.responses import EquipmentOut, BorrowEquipmentIn, EquipmentListOut


class EquipmentHandler:
    def __init__(self, equipment_service: EquipmentService):
        self.equipment_service = equipment_service

    def get_equipment_list(self, request) -> EquipmentListOut:
        equipment_list = self.equipment_service.get_equipment_employee_list(request.user)
        return EquipmentListOut(equipment=equipment_list)

    def get_equipment_by_id(self, request, id: int) -> EquipmentOut:
        return EquipmentOut.from_orm(self.equipment_service.get_equipment_by_id(id))

    def return_equipment(self, request, id: int, return_date: date) -> EquipmentOut:
        return EquipmentOut.from_orm(self.equipment_service.return_equipment(request.user, id, return_date))

    def borrow_equipment(self, request, id: int, borrow_data: BorrowEquipmentIn) -> EquipmentOut:
        return EquipmentOut.from_orm(
            self.equipment_service.borrow_equipment(request.user, id, BorrowEquipmentData(**borrow_data.dict()))
        )

    def extension_borrow_equipment(self, request, id: int, estimated_return_date: date) -> EquipmentOut:
        return EquipmentOut.from_orm(
            self.equipment_service.extension_borrow_equipment(request.user, id, estimated_return_date)
        )
