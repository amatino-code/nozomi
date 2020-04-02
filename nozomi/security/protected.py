"""
Nozomi
Protected Protocol
Copyright Amatino Pty Ltd
"""
from nozomi.security.agent import Agent
from nozomi.security.permission_record import PermissionRecord
from nozomi.security.read_protected import ReadProtected


class Protected(ReadProtected):
    """
    Abstract protocol defining an interface for objects to whom access is
    limited.
    """

    permission_record: PermissionRecord = NotImplemented

    def grants_read_to(self, agent: Agent) -> bool:
        """Return True if an Agent may read this object"""
        if not isinstance(self.permission_record, PermissionRecord):
            raise NotImplementedError('.permission_record not implemented')
        return self.permission_record.records_read_permission_for(agent)

    def grants_write_to(self, agent: Agent) -> bool:
        """Return True if an Agent may write to this object"""
        if not isinstance(self.permission_record, PermissionRecord):
            raise NotImplementedError('.permission_record not implemented')
        return self.permission_record.records_write_permission_for(agent)

    def grants_admin_to(self, agent: Agent) -> bool:
        if not isinstance(self.permission_record, PermissionRecord):
            raise NotImplementedError('.permission_record not implemented')
        return self.permission_record.records_admin_permission_for(agent)

    def is_owned_by(self, agent: Agent) -> bool:
        if not isinstance(self.permission_record, PermissionRecord):
            raise NotImplementedError('.permission_record not implemented')
        return self.permission_record.records_ownership_by(agent)
