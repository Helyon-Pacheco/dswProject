from abc import ABC, abstractmethod
from typing import List
from .notification import Notification
from ..enums.notification_type import NotificationType
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ValidationResult(BaseModel):
    errors: List[str]

class INotifier(ABC):
    @abstractmethod
    def get_notifications(self) -> List[Notification]:
        pass

    @abstractmethod
    def has_notification(self) -> bool:
        pass

    @abstractmethod
    def handle(self, notification: Notification):
        pass

    @abstractmethod
    def handle_message(self, message: str, type: Optional[NotificationType] = NotificationType.INFORMATION):
        pass

    @abstractmethod
    def handle_exception(self, exception: Exception):
        pass

    @abstractmethod
    def notify_validation_errors(self, validation_result: ValidationResult):
        pass

    @abstractmethod
    def clean(self):
        pass

class Notifier(INotifier):
    def __init__(self):
        self._notifications: List[Notification] = []

    def get_notifications(self) -> List[Notification]:
        return self._notifications

    def has_notification(self) -> bool:
        return bool(self._notifications)

    def handle(self, notification: Notification):
        if notification is None:
            raise ValueError("notification cannot be None")
        self._notifications.append(notification)

    def handle_message(self, message: str, type: Optional[NotificationType] = NotificationType.INFORMATION):
        if not message.strip():
            raise ValueError("Message cannot be null or whitespace.")
        self._notifications.append(Notification(message=message, type=type))

    def handle_exception(self, exception: Exception):
        if exception is None:
            raise ValueError("exception cannot be None")
        self.handle_exception_internal(exception)

    def handle_exception_internal(self, exception: Exception):
        friendly_message = self.generate_friendly_message(exception)
        self._notifications.append(Notification(message=friendly_message, type=NotificationType.ERROR))

    def generate_friendly_message(self, exception: Exception) -> str:
        if isinstance(exception, ValueError):
            return f"There was an issue with the provided value: {exception.args[0]}"
        elif isinstance(exception, KeyError):
            return f"A required key was missing: {exception.args[0]}"
        elif isinstance(exception, IndexError):
            return f"An index out of range error occurred: {exception.args[0]}"
        else:
            return f"An unexpected error occurred: {exception.args[0]}. Please try again later or contact support."

    def notify_validation_errors(self, validation_result: ValidationResult):
        if validation_result is None:
            raise ValueError("validationResult cannot be None")
        for error in validation_result.errors:
            self.handle_message(error, NotificationType.ERROR)

    def clean(self):
        self._notifications.clear()
