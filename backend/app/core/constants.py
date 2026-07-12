"""Application-wide constants."""

# Supported file types (SAGE_BLUEPRINT.md Section 133 / 138)
SUPPORTED_FILE_EXTENSIONS = {".pdf", ".docx", ".txt", ".csv", ".xlsx", ".png", ".jpg", ".jpeg"}

# Memory categories (Section 34 / 71)
MEMORY_CATEGORIES = {"preference", "goal", "fact", "event", "note"}

# Memory source types
MEMORY_SOURCES = {"explicit", "automatic", "imported"}

# Task priority levels (Section 218)
TASK_PRIORITIES = {"low", "medium", "high", "critical"}

# Task statuses (Section 219)
TASK_STATUSES = {"pending", "in_progress", "completed", "cancelled"}

# Reminder schedule types (Section 74 / 151)
REMINDER_SCHEDULE_TYPES = {"once", "recurring"}

# Message roles (Section 69)
MESSAGE_ROLES = {"user", "assistant", "system", "tool"}

# Tool execution statuses (Section 75)
TOOL_EXECUTION_STATUSES = {"started", "success", "failed"}

API_V1_PREFIX = "/api/v1"
