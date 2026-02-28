"""Access control policies for Telegram operations.

Similar to OpenClaw bot policies but for user account access.
Default: read-only for all. Override as needed.
"""

from enum import Enum
from typing import Optional, Dict, Set, List
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


class AccessLevel(Enum):
    """Access permission levels."""
    BLOCKED = "blocked"  # No access
    READ = "read"       # Read-only (default)
    WRITE = "write"     # Read and write


class ChatType(Enum):
    """Telegram chat types."""
    DM = "dm"           # Direct messages
    BOT = "bot"         # Bot chats
    GROUP = "group"     # Group chats
    CHANNEL = "channel" # Channels
    SUPERGROUP = "supergroup"  # Supergroups


@dataclass
class ChatPolicy:
    """Policy for a specific chat."""
    chat_id: int
    access: AccessLevel = AccessLevel.READ
    allow_forward: bool = False
    allow_media_download: bool = False


@dataclass
class TypePolicy:
    """Policy for a chat type (DM, group, channel, etc)."""
    chat_type: ChatType
    access: AccessLevel = AccessLevel.READ
    allow_forward: bool = False
    allow_media_download: bool = False


@dataclass
class AccessPolicy:
    """Complete access control policy.
    
    Hierarchy:
    1. Specific chat policy (if exists) → use it
    2. Chat type policy (if exists) → use it
    3. Default policy → use it
    """
    
    # Default policy (applies to everything not specified)
    default_access: AccessLevel = AccessLevel.READ
    default_allow_forward: bool = False
    default_allow_media_download: bool = False
    
    # Type-based policies (apply to all chats of that type)
    type_policies: Dict[ChatType, TypePolicy] = field(default_factory=dict)
    
    # Specific chat policies (override type and default)
    chat_policies: Dict[int, ChatPolicy] = field(default_factory=dict)
    
    # Blocked chat IDs (shortcut for access=BLOCKED)
    blocked_chats: Set[int] = field(default_factory=set)
    
    # Blocked chat types
    blocked_types: Set[ChatType] = field(default_factory=set)

    def get_access_level(self, chat_id: int, chat_type: Optional[ChatType] = None) -> AccessLevel:
        """Get access level for a chat.
        
        Args:
            chat_id: Chat ID
            chat_type: Chat type (if known)
            
        Returns:
            Access level (BLOCKED, READ, or WRITE)
        """
        # 1. Check if chat is in blocked list
        if chat_id in self.blocked_chats:
            return AccessLevel.BLOCKED
        
        # 2. Check specific chat policy
        if chat_id in self.chat_policies:
            return self.chat_policies[chat_id].access
        
        # 3. Check if type is blocked
        if chat_type and chat_type in self.blocked_types:
            return AccessLevel.BLOCKED
        
        # 4. Check type-based policy
        if chat_type and chat_type in self.type_policies:
            return self.type_policies[chat_type].access
        
        # 5. Use default
        return self.default_access

    def can_read(self, chat_id: int, chat_type: Optional[ChatType] = None) -> bool:
        """Check if reading is allowed."""
        level = self.get_access_level(chat_id, chat_type)
        return level != AccessLevel.BLOCKED

    def can_write(self, chat_id: int, chat_type: Optional[ChatType] = None) -> bool:
        """Check if writing is allowed."""
        level = self.get_access_level(chat_id, chat_type)
        return level == AccessLevel.WRITE

    def can_forward(self, chat_id: int, chat_type: Optional[ChatType] = None) -> bool:
        """Check if forwarding is allowed."""
        if not self.can_read(chat_id, chat_type):
            return False
        
        # Check specific policy
        if chat_id in self.chat_policies:
            return self.chat_policies[chat_id].allow_forward
        
        # Check type policy
        if chat_type and chat_type in self.type_policies:
            return self.type_policies[chat_type].allow_forward
        
        return self.default_allow_forward

    def can_download_media(self, chat_id: int, chat_type: Optional[ChatType] = None) -> bool:
        """Check if media download is allowed."""
        if not self.can_read(chat_id, chat_type):
            return False
        
        # Check specific policy
        if chat_id in self.chat_policies:
            return self.chat_policies[chat_id].allow_media_download
        
        # Check type policy
        if chat_type and chat_type in self.type_policies:
            return self.type_policies[chat_type].allow_media_download
        
        return self.default_allow_media_download

    def allow_chat(self, chat_id: int, access: AccessLevel = AccessLevel.READ):
        """Allow access to specific chat."""
        self.chat_policies[chat_id] = ChatPolicy(
            chat_id=chat_id,
            access=access
        )
        logger.info(f"Chat {chat_id}: {access.value} access allowed")

    def block_chat(self, chat_id: int):
        """Block specific chat."""
        self.blocked_chats.add(chat_id)
        logger.info(f"Chat {chat_id}: blocked")

    def allow_type(self, chat_type: ChatType, access: AccessLevel = AccessLevel.READ):
        """Allow access to chat type."""
        self.type_policies[chat_type] = TypePolicy(
            chat_type=chat_type,
            access=access
        )
        logger.info(f"Type {chat_type.value}: {access.value} access allowed")

    def block_type(self, chat_type: ChatType):
        """Block chat type."""
        self.blocked_types.add(chat_type)
        logger.info(f"Type {chat_type.value}: blocked")

    @classmethod
    def read_only(cls) -> "AccessPolicy":
        """Create read-only policy (default)."""
        return cls(
            default_access=AccessLevel.READ,
            default_allow_forward=False,
            default_allow_media_download=False,
        )

    @classmethod
    def permissive(cls) -> "AccessPolicy":
        """Create permissive policy (read/write all)."""
        return cls(
            default_access=AccessLevel.WRITE,
            default_allow_forward=True,
            default_allow_media_download=True,
        )

    def __repr__(self) -> str:
        return (
            f"AccessPolicy(default={self.default_access.value}, "
            f"blocked_chats={len(self.blocked_chats)}, "
            f"type_policies={len(self.type_policies)}, "
            f"chat_policies={len(self.chat_policies)})"
        )
