from __future__ import annotations

class MonitorBase:
    _accessors: int = 0
    _instance: MonitorBase = None
    
    @classmethod
    def get_instance(cls) -> MonitorBase:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


    @classmethod
    def set_instance(cls, p_instance: MonitorBase):
        cls._instance = p_instance


    @classmethod
    def increase_accessors(cls):
        if cls._accessors == 0 and cls._instance is None:
            cls._instance = cls()
        cls._accessors += 1
        
    @classmethod
    def decrease_accessors(cls):
        cls._accessors -= 1
        
        if cls._accessors == 0:
            cls._instance.shutdown()
            cls._instance = None
    
    def __init__(self):
        pass
    
    def shutdown(self):
        pass