from rest_framework.exceptions import APIException


class InvalidProfessionSelection(APIException):
    status_code = 400
    default_detail = 'An invalid profession has been selected based on an entity race'
    default_code = 'bad_profession'


class InvalidName(APIException):
    status_code = 400
    default_detail = 'A player-provided name was rejected'
    default_code = 'bad_entityname'


