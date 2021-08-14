from api.internal.dto.commissions import AddCommissionDTO
from api.internal.service.transfer_money import TransferMoneyService
from api.internal.service.commission import CommissionService
from api.internal.transport.rest.transfer_money.requests import TransferMoneyIn
from api.internal.dto.transfer_money import AddTransferMoneyDTO
from api.internal.transport.rest.transfer_money.responses import TransferMoneyWithCommissionsOut, TransferMoneyOut, \
    TransferMoneyListOut
from api.pkg.requests import PaginationIn

from ninja import Query


class TransferMoneyHandler:
    def __init__(self, transfer_money_service: TransferMoneyService, commission_service: CommissionService):
        self.transfer_money_service = transfer_money_service
        self.commission_service = commission_service

    def get_transfer_money_list(self, request, pagination_data: PaginationIn = Query(...)) -> TransferMoneyListOut:
        count, transfers_money = self.transfer_money_service.get_transfer_money_list(**pagination_data.dict())

        return TransferMoneyListOut(
            count=count,
            items=[
                TransferMoneyWithCommissionsOut(
                    transfer_money=TransferMoneyOut.from_orm(transfer_money),
                    commissions=self.commission_service.get_commissions(source_transfer_money=transfer_money)
                ) for transfer_money in transfers_money
            ]
        )

    def add_transfer_money_list(self, request, transfer_money_data: TransferMoneyIn) -> TransferMoneyWithCommissionsOut:
        transfer_money_data = transfer_money_data.dict()
        commissions_data = transfer_money_data.pop('commissions')

        transfer_money = self.transfer_money_service.add_transfer_money(AddTransferMoneyDTO(**transfer_money_data))

        commissions = self.commission_service.add_commissions(
            source_date=transfer_money.date,
            source_transfer_money=self.transfer_money_service.get_transfer_money_by_id(transfer_money.id),
            commissions_data=[AddCommissionDTO(**commission) for commission in commissions_data],
        )

        return TransferMoneyWithCommissionsOut(
            transfer_money=TransferMoneyOut.from_orm(transfer_money),
            commissions=commissions
        )
