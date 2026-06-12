"""
License verification module for VISIL.
Validates user authorization before running sensitive operations.
"""

import os
import json
from datetime import datetime
from pathlib import Path


class LicenseManager:
    """
    Manages license verification for VISIL.
    Requires valid license file in user's system.
    """

    LICENSE_HEADER = "VISIL-LICENSE-V1"
    
    def __init__(self, license_path=None):
        """Initialize license manager with optional custom license path."""
        if license_path is None:
            license_path = os.path.expanduser("~/.visil/license.json")
        self.license_path = license_path

    def verify_license(self):
        """
        Verify that a valid license exists.
        Raises ValueError if license is missing or invalid.
        """
        if not os.path.exists(self.license_path):
            raise ValueError(
                f"VISIL License not found. "
                f"Please contact Vera Lynn DeGraw for authorization. "
                f"Expected location: {self.license_path}"
            )

        try:
            with open(self.license_path, 'r') as f:
                license_data = json.load(f)
        except Exception as e:
            raise ValueError(f"Invalid license file: {str(e)}")

        # Verify required fields
        required_fields = ["header", "licensee", "issued_date", "signature"]
        for field in required_fields:
            if field not in license_data:
                raise ValueError(f"License missing required field: {field}")

        # Verify header
        if license_data["header"] != self.LICENSE_HEADER:
            raise ValueError("Invalid license header")

        # Verify expiration if present
        if "expiration_date" in license_data:
            exp_date = datetime.fromisoformat(license_data["expiration_date"])
            if datetime.now() > exp_date:
                raise ValueError("License has expired")

        return True

    def check_before_execution(self):
        """
        Decorator-compatible method to enforce license verification.
        Use with @license_manager.check_before_execution
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                self.verify_license()
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def get_licensee(self):
        """Get the licensed user's name."""
        try:
            self.verify_license()
            with open(self.license_path, 'r') as f:
                license_data = json.load(f)
            return license_data.get("licensee", "Unknown")
        except:
            return None


# Global license manager instance
_license_manager = LicenseManager()


def require_license(func):
    """
    Decorator to require valid license before function execution.
    Usage:
        @require_license
        def sensitive_operation():
            pass
    """
    def wrapper(*args, **kwargs):
        _license_manager.verify_license()
        return func(*args, **kwargs)
    return wrapper
