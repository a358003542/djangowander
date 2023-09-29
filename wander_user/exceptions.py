from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User already exist.'
    default_code = 'user_already_exist'
