"""Agent Pool - Resource pooling and management for agents."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid


class AgentType(Enum):
    NVIDIA_GPU = "nvidia"
    AWS_TRAINIUM = "trainium"
    GOOGLE_TPU = "tpu"
    CPU = "cpu"


class Protocol(Enum):
    MCP = "mcp"
    A2A = "a2a"
    CUSTOM = "custom"
    HTTP = "http"


@dataclass
class PooledAgent:
    agent_id: str
    capacity: int
    in_use: bool = False
    current_load: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentPool:
    """Resource pooling and management for agents."""
    
    def __init__(self, min_size: int = 0, max_size: int = 100):
        self.agents: Dict[str, PooledAgent] = {}
        self.min_size = min_size
        self.max_size = max_size
    
    def add_agent(self, agent_id: str, capacity: int = 10, metadata: Dict[str, Any] = None) -> bool:
        if len(self.agents) >= self.max_size:
            return False
        
        agent = PooledAgent(agent_id=agent_id, capacity=capacity, metadata=metadata or {})
        self.agents[agent_id] = agent
        return True
    
    def remove_agent(self, agent_id: str) -> bool:
        agent = self.agents.get(agent_id)
        if not agent or agent.in_use:
            return False
        
        del self.agents[agent_id]
        return True
    
    def acquire(self, capacity_needed: int = 1) -> Optional[str]:
        for agent_id, agent in self.agents.items():
            if not agent.in_use and agent.capacity >= capacity_needed:
                agent.in_use = True
                agent.current_load = capacity_needed
                return agent_id
        return None
    
    def release(self, agent_id: str) -> bool:
        agent = self.agents.get(agent_id)
        if not agent:
            return False
        
        agent.in_use = False
        agent.current_load = 0
        return True
    
    def get_available(self) -> List[str]:
        return [a.agent_id for a in self.agents.values() if not a.in_use]
    
    def get_stats(self) -> Dict[str, Any]:
        total = len(self.agents)
        in_use = sum(1 for a in self.agents.values() if a.in_use)
        total_capacity = sum(a.capacity for a in self.agents.values())
        used_capacity = sum(a.current_load for a in self.agents.values())
        
        return {
            "total_agents": total,
            "in_use": in_use,
            "available": total - in_use,
            "total_capacity": total_capacity,
            "used_capacity": used_capacity,
            "utilization": used_capacity / max(total_capacity, 1)
        }


__all__ = ["AgentPool", "PooledAgent", "AgentType", "Protocol"]
