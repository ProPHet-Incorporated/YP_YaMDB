from rest_framework.exceptions import ValidationError
import re


def validate_username(username):
    if username == 'me':
        raise ValidationError('Резервное системное имя.')

    # first option

    # if not re.match(r'^[\w.@+-]+$', username):
    #   raise ValidationError(f'{username} - cодержит запрещенные символы.')

    # second option

    allowed_symbols = r'^[\w.@+-]+$'
    if not re.match(rf'{allowed_symbols}', username):
        forbidden_symbols = []
        for char in username:
            if char not in allowed_symbols:
                forbidden_symbols.append(char)
        if forbidden_symbols:
            raise ValidationError(
                f'{username} - cодержит запрещенные символы: '
                f'{forbidden_symbols}'
            )
