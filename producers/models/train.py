"""Defines CTA Train Model"""
from enum import IntEnum
import logging


logger = logging.getLogger(__name__)


class Train:
    """Defines CTA Train Model"""

    status = IntEnum("status", "out_of_service in_service broken_down", start=0)

    def __init__(self, train_id, status):
        self.train_id = train_id
        self.status = status
        if self.status is None:
            self.status = Train.status.out_of_service

    def __str__(self):
        return f"Train ID {self.train_id} is {self.status.name.replace('_', ' ')}"

    def __repr__(self):
        return str(self)

    def broken(self):
        return self.status == Train.status.broken_down
