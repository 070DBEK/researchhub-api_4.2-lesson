"""
Custom validators for the ResearchHub API.
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_orcid_id(value):
    """
    Validate ORCID ID format.
    """
    pattern = r'^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Invalid ORCID ID format. Expected format: 0000-0000-0000-0000'),
            code='invalid_orcid'
        )


def validate_doi(value):
    """
    Validate DOI format.
    """
    pattern = r'^10\.\d{4,}\/[-._;()\/:a-zA-Z0-9]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Invalid DOI format. Expected format: 10.xxxx/xxxxx'),
            code='invalid_doi'
        )


def validate_file_size(value):
    """
    Validate file size (max 50MB).
    """
    max_size = 50 * 1024 * 1024  # 50MB
    if value.size > max_size:
        raise ValidationError(
            _('File size cannot exceed 50MB.'),
            code='file_too_large'
        )


def validate_image_file(value):
    """
    Validate image file type.
    """
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if value.content_type not in allowed_types:
        raise ValidationError(
            _('Only JPEG, PNG, GIF, and WebP images are allowed.'),
            code='invalid_image_type'
        )
