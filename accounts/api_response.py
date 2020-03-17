from rest_framework.response import Response

from accounts.models import Ad
from accounts.serializers import AdSerializer


def get_all_response(request, offset, amount):
    result = Ad.objects.all()[offset:offset + amount]
    clean_data = []
    for row in result:
        clean_data.append(AdSerializer(row).data)
    return Response(clean_data)


def get_ping_response(request):
    return create_response(200, True, {}, {"Server run"})


def post_add_response(request):
    _addition = request.data.get('addition')
    try:
        person = Ad.objects.get(uuid=_addition.get('uuid'))
        addition = write_addition(person)

        if person.status:
            person.balance += _addition.get('change')
            person.save()
            return create_response(200, True, addition, {"Successfully"})
        else:
            return create_response(403, False, addition, {"Account is closed"})
    except Exception as e:
        return create_response(404, False, _addition, {"Not Found: {}".format(e)})


def post_substract_response(request):
    _addition = request.data.get('addition')
    try:
        person = Ad.objects.get(uuid=_addition.get('uuid'))
        addition = write_addition(person)
        if person.status:
            change = _addition.get('change')
            if person.balance - person.hold - change >= 0:
                person.hold += change
                person.save()

                return create_response(200, True, addition, {"Successfully"})
            else:
                return create_response(400, False, addition, {"Insufficient balance"})
        else:
            return create_response(403, False, addition, {"Account is closed"})
    except Exception as e:
        return create_response(404, False, _addition, {"Not Found: {}".format(e)})


def post_status_response(request):
    addition = request.data.get('addition')
    try:
        person = Ad.objects.get(uuid=addition.get('uuid'))
        addition = write_addition(person)

        return create_response(200, True, addition, {"Successfully"})

    except Exception as e:
        return create_response(404, False, addition, {"Not Found: {}".format(e)})


def create_response(http_status, operation_status, addition, description):
    return Response({
        "status": http_status,
        "result": operation_status,
        "addition": addition,
        "description": description
    })


def write_addition(person):
    addition = {
        "uuid": person.uuid,
        "name": person.name,
        "balance": person.balance,
        "hold": person.hold,
        "status": person.status
    }


    return addition