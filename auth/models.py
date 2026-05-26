"""Data models for CogniESL auth."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: str
    email: str
    password_hash: str
    created_at: str
    subscription_tier: str = "free"  # free | pro
    stripe_customer_id: str = ""


@dataclass
class UserPublic:
    """Safe version of User to return from API (no password_hash)."""
    id: str
    email: str
    created_at: str
    subscription_tier: str
