from api.internal.dto.commissions import CommissionDTO
from api.internal.dto.payment_methods import PaymentMethodDTO
from api.internal.models.expenses import CommissionExpense

from datetime import date
from ninja import Schema
from typing import List


class TransferMoneyOut(Schema):
    id: int
    amount: float
    conversion_rate: float
    where_to: PaymentMethodDTO
    where_from: PaymentMethodDTO
    date: date


class TransferMoneyWithCommissionsOut(TransferMoneyOut):
    commissions: List[CommissionDTO]

    def __init__(self, transfer_money: TransferMoneyOut, commissions: List[CommissionExpense]):
        super().__init__(
            commissions=[CommissionDTO(commission.expense) for commission in commissions],
            **transfer_money.dict()
        )


class TransferMoneyListOut(Schema):
    count: int
    items: List[TransferMoneyWithCommissionsOut]
