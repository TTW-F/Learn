from .auth import router as auth_router
from .students import router as students_router

__all__ = ["auth_router", "students_router"]