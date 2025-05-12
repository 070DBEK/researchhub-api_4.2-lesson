from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound


class ObjectNotFound(NotFound):
    default_detail = _("Not found.")
    default_code = "NOT_FOUND"
