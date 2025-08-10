# src/agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaseAgent(ABC):
    """
    An abstract base class for all specialist agents in the framework.

    This class defines the common interface that all agents must implement,
    ensuring that the Orchestrator and Dispatcher can interact with any agent
    in a consistent manner. It also provides a common constructor for loading
    the agent's system prompt, which defines its core behavior and persona.
    """

    def __init__(self, system_prompt_path: str):
        """
        Initializes the agent and loads its system prompt.

        Args:
            system_prompt_path: The file path to the .txt or .md file
                                containing the agent's system prompt.
        """
        self.system_prompt_path = Path(system_prompt_path)
        self.system_prompt = self._load_system_prompt()
        agent_name = self.__class__.__name__
        logging.info(f"Initialized {agent_name} with prompt from {system_prompt_path}")

    def _load_system_prompt(self) -> str:
        """
        Loads the system prompt content from the specified file path.
        """
        try:
            with self.system_prompt_path.open('r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logging.error(f"System prompt file not found: {self.system_prompt_path}")
            # Depending on requirements, you might raise an error or default to an empty prompt
            raise
        except Exception as e:
            logging.error(f"Error reading system prompt file {self.system_prompt_path}: {e}")
            raise

    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        The core logic method for the agent. This must be implemented by all subclasses.

        This method receives a task from the Dispatcher, performs its specialized
        logic, and returns a result payload.

        Args:
            task: A dictionary containing the data and instructions for the task.

        Returns:
            A dictionary containing the result of the task execution.
        """
        pass

