import re

from django.core.exceptions import ValidationError

REGEX_FOR_USERNAME = re.compile(r'^[\w.@+-]+')
REGEX_FOR_PASSWORD = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
)


def validate_username(name):
    """Checking the username field for compliance."""
    if name == 'me':
        raise ValidationError('The username "me" is not allowed!')
    if not REGEX_FOR_USERNAME.fullmatch(name):
        raise ValidationError(
            'You can only use letters, numbers, and @.+-_"')


def validate_password(password):
    """Checking the user password field for compliance."""
    if re.match(REGEX_FOR_PASSWORD, password) is None:
        raise ValidationError('The password must contain upper and lower case'
                              'letters, numbers, and special symbols.')
