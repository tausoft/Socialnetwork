from django_registration.forms import RegistrationForm
from models import UserManager

class UserManagerForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = UserManager