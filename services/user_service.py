# Borrow Service Module
# This module handles borrow record management operations
# TODO: Implement borrow service logic (borrow, return, track records, overdue management)
"""User service for the library CLI."""
from typing import Optional
from models.user import User
from utils.file_handler import read_json, write_json

USERS_FILE = "users.json"

VALID_ROLES = ("member", "librarian", "admin")


class UserService:
    """Handles user management (admin/librarian operations)."""

    def __init__(self):
        """Initialize the user service."""
        self._ensure_file()

    def _ensure_file(self):
        """Make sure the users JSON file exists and is a list."""
        data = read_json(USERS_FILE)
        if not isinstance(data, list):
            write_json(USERS_FILE, [])

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _load_all(self) -> list[dict]:
        return read_json(USERS_FILE)

    def _save_all(self, users: list[dict]):
        write_json(USERS_FILE, users)

    @staticmethod
    def _safe(user_dict: dict) -> dict:
        """Strip password/salt before returning to caller."""
        return {k: v for k, v in user_dict.items() if k not in ("password", "salt")}

    def _find_idx(self, user_id: str) -> int:
        """Return list index for user by UUID, or -1."""
        for i, u in enumerate(self._load_all()):
            if u.get("id") == user_id:
                return i
        return -1

    # ── Public API ─────────────────────────────────────────────────────────────

    def get_all_users(self) -> list[dict]:
        """Return all users (password fields removed).

        Returns:
            List of safe user dicts.
        """
        return [self._safe(u) for u in self._load_all()]

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Return a single user by UUID (password removed), or None.

        Args:
            user_id: UUID of the user.

        Returns:
            Safe user dict or None.
        """
        idx = self._find_idx(user_id)
        if idx == -1:
            return None
        return self._safe(self._load_all()[idx])

    def get_user_by_username(self, username: str) -> Optional[dict]:
        """Return a single user by username (password removed), or None.

        Args:
            username: Login name.

        Returns:
            Safe user dict or None.
        """
        for u in self._load_all():
            if u.get("username", "").lower() == username.lower():
                return self._safe(u)
        return None

    def update_user(self, user_id: str, name: Optional[str] = None,
                    email: Optional[str] = None, phone: Optional[str] = None,
                    address: Optional[str] = None) -> dict:
        """Update a user's profile details.

        Args:
            user_id: UUID of the user to update.
            name: New display name (optional).
            email: New email (optional).
            phone: New phone number (optional).
            address: New address (optional).

        Returns:
            dict with 'success' (bool), 'message' (str).
            On success also includes 'user' (safe dict).
        """
        users = self._load_all()
        idx = next((i for i, u in enumerate(users) if u.get("id") == user_id), -1)

        if idx == -1:
            return {"success": False, "message": f"User with ID '{user_id}' not found."}

        if name and name.strip():
            users[idx]["name"] = name.strip()
        if email and email.strip():
            # Check uniqueness
            for u in users:
                if u.get("email", "").lower() == email.strip().lower() and u.get("id") != user_id:
                    return {"success": False, "message": "That email is already in use."}
            users[idx]["email"] = email.strip()
        if phone is not None:
            users[idx]["phone"] = phone.strip()
        if address is not None:
            users[idx]["address"] = address.strip()

        from datetime import datetime
        users[idx]["updated_at"] = datetime.now().isoformat()

        self._save_all(users)
        return {
            "success": True,
            "message": "User profile updated successfully.",
            "user": self._safe(users[idx]),
        }

    def update_role(self, user_id: str, new_role: str) -> dict:
        """Change a user's role.

        Args:
            user_id: UUID of the user.
            new_role: One of 'member', 'librarian', 'admin'.

        Returns:
            dict with 'success' (bool) and 'message' (str).
        """
        if new_role not in VALID_ROLES:
            return {"success": False, "message": f"Role must be one of: {', '.join(VALID_ROLES)}."}

        users = self._load_all()
        idx = next((i for i, u in enumerate(users) if u.get("id") == user_id), -1)

        if idx == -1:
            return {"success": False, "message": f"User with ID '{user_id}' not found."}

        old_role = users[idx].get("role", "member")
        users[idx]["role"] = new_role

        from datetime import datetime
        users[idx]["updated_at"] = datetime.now().isoformat()

        self._save_all(users)
        return {
            "success": True,
            "message": (
                f"Role updated from '{old_role}' to '{new_role}' "
                f"for user '{users[idx].get('username', user_id)}'."
            ),
        }

    def deactivate_user(self, user_id: str) -> dict:
        """Deactivate a user account (prevents login).

        Args:
            user_id: UUID of the user.

        Returns:
            dict with 'success' (bool) and 'message' (str).
        """
        users = self._load_all()
        idx = next((i for i, u in enumerate(users) if u.get("id") == user_id), -1)

        if idx == -1:
            return {"success": False, "message": f"User with ID '{user_id}' not found."}

        if not users[idx].get("is_active", True):
            return {"success": False, "message": "User is already deactivated."}

        users[idx]["is_active"] = False

        from datetime import datetime
        users[idx]["updated_at"] = datetime.now().isoformat()

        self._save_all(users)
        return {
            "success": True,
            "message": f"User '{users[idx].get('username', user_id)}' has been deactivated.",
        }

    def reactivate_user(self, user_id: str) -> dict:
        """Reactivate a previously deactivated user account.

        Args:
            user_id: UUID of the user.

        Returns:
            dict with 'success' (bool) and 'message' (str).
        """
        users = self._load_all()
        idx = next((i for i, u in enumerate(users) if u.get("id") == user_id), -1)

        if idx == -1:
            return {"success": False, "message": f"User with ID '{user_id}' not found."}

        if users[idx].get("is_active", True):
            return {"success": False, "message": "User is already active."}

        users[idx]["is_active"] = True

        from datetime import datetime
        users[idx]["updated_at"] = datetime.now().isoformat()

        self._save_all(users)
        return {
            "success": True,
            "message": f"User '{users[idx].get('username', user_id)}' has been reactivated.",
        }

    def delete_user(self, user_id: str) -> dict:
        """Permanently delete a user account.

        Args:
            user_id: UUID of the user.

        Returns:
            dict with 'success' (bool) and 'message' (str).
        """
        users = self._load_all()
        idx = next((i for i, u in enumerate(users) if u.get("id") == user_id), -1)

        if idx == -1:
            return {"success": False, "message": f"User with ID '{user_id}' not found."}

        username = users[idx].get("username", user_id)
        users.pop(idx)
        self._save_all(users)
        return {"success": True, "message": f"User '{username}' has been permanently deleted."}

    def renew_membership(self, user_id: str, days: int = 365) -> dict:
        """Extend a user's membership expiry date.

        Args:
            user_id: UUID of the user.
            days: Number of days to extend from today (default 365).

        Returns:
            dict with 'success' (bool) and 'message' (str).
        """
        users = self._load_all()
        idx = next((i for i, u in enumerate(users) if u.get("id") == user_id), -1)

        if idx == -1:
            return {"success": False, "message": f"User with ID '{user_id}' not found."}

        from datetime import datetime, timedelta
        new_expiry = datetime.now() + timedelta(days=days)
        users[idx]["membership_expiry"] = new_expiry.isoformat()
        users[idx]["updated_at"] = datetime.now().isoformat()

        self._save_all(users)
        return {
            "success": True,
            "message": (
                f"Membership for '{users[idx].get('username', user_id)}' "
                f"renewed until {new_expiry.strftime('%Y-%m-%d')}."
            ),
        }

    def get_users_by_role(self, role: str) -> list[dict]:
        """Return all users with a specific role.

        Args:
            role: Role to filter by ('member', 'librarian', 'admin').

        Returns:
            List of safe user dicts.
        """
        return [self._safe(u) for u in self._load_all() if u.get("role") == role] 
