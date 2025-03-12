# models/__init__.py
from .users import users
from .access import Access
from .userBIAccess import Userbiaccess
from .accessWeb import accessWeb

from .userWebAccess import userWebAccess

__all__ = ["users", "Access", "Userbiaccess", "accessWeb","userWebAccess"]
