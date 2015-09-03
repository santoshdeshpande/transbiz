from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        userModel = get_user_model()
        if username is None:
            username = kwargs.get(userModel.USERNAME_FIELD)
        try:
            user = userModel._default_manager.get_by_natural_key(username)
            if user.is_valid_login() and user.check_password(password):
                print "User ok: %s" % user
                return user
            print "Login Ok: %d" % user.is_valid_login()
        except userModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            userModel().set_password(password)


class MobileAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        userModel = get_user_model()
        if username is None:
            username = kwargs.get("email")
        try:
            user = userModel._default_manager.get(mobile_no__exact=username)
            if user.is_valid_login() and user.check_password(password):
                return user
        except userModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            userModel().set_password(password)
