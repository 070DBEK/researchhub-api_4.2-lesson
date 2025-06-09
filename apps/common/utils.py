"""
Common utility functions.
"""
import uuid
import os
from django.utils.text import slugify
from django.core.files.storage import default_storage


def generate_unique_filename(filename):
    """
    Generate a unique filename using UUID.
    """
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return unique_filename


def upload_to_path(instance, filename):
    """
    Generate upload path for files.
    """
    model_name = instance.__class__.__name__.lower()
    unique_filename = generate_unique_filename(filename)
    return f"{model_name}s/{unique_filename}"


def create_slug(text, max_length=50):
    """
    Create a URL-friendly slug from text.
    """
    slug = slugify(text)
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')
    return slug


def get_client_ip(request):
    """
    Get client IP address from request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """
    Get user agent from request.
    """
    return request.META.get('HTTP_USER_AGENT', '')


def safe_delete_file(file_path):
    """
    Safely delete a file from storage.
    """
    try:
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
            return True
    except Exception:
        pass
    return False
