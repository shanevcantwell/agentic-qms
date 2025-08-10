# src/framework/orchestrator.py

import yaml
from pathlib import Path
from typing import Dict, Any, List
import logging

from .dispatcher import Dispatcher

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Orchestrator:
    """
    Manages and executes complex workflows defined in external files.

    The Orchestrator reads a workflow configuration (e.g., a YAML file),
    interprets the sequence of steps, and uses a Dispatcher instance to
    delegate tasks to the appropriate agents.
    """

    def __init__(self, dispatcher: Dispatcher):
        """
        Initializes the Orchestrator with a dispatcher instance.

        Args:
            dispatcher: An instance of the Dispatcher class to handle task routing.
        """
        if not isinstance(dispatcher, Dispatcher):
            raise TypeError("dispatcher must be an instance of Dispatcher")
        self.dispatcher = dispatcher
        logging.info("Orchestrator initialized.")

    def run_workflow(self, workflow_path: str) -> None:
        """
        Parses and executes a workflow from a specified YAML file.

        The workflow file should define a sequence of steps, with each step
        specifying the target agent and the task payload.

        Example YAML structure:
        --------------------
        workflow_name: "Example Validation Workflow"
        steps:
          - name: "Step 1: Initial Analysis"
            agent: "analyst_agent"
            task:
              description: "Analyze the initial user query."
              data: "..."

          - name: "Step 2: Data Retrieval"
            agent: "retrieval_agent"
            task:
              description: "Retrieve relevant documents based on analysis."
              query: "..."
        --------------------

        Args:
            workflow_path: The file path to the YAML workflow definition.
        """
        logging.info(f"Starting workflow from: {workflow_path}")
        try:
            workflow_file = Path(workflow_path)
            if not workflow_file.exists():
                logging.error(f"Workflow file not found at: {workflow_path}")
                return

            with workflow_file.open('r') as f:
                workflow_config = yaml.safe_load(f)

        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file {workflow_path}: {e}")
            return
        except Exception as e:
            logging.error(f"An unexpected error occurred while reading the workflow file: {e}")
            return

        steps: List[Dict[str, Any]] = workflow_config.get("steps", [])
        if not steps:
            logging.warning(f"No steps found in workflow: {workflow_path}")
            return

        logging.info(f"Executing workflow: '{workflow_config.get('workflow_name', 'Untitled')}'")
        for i, step in enumerate(steps):
            step_name = step.get("name", f"Unnamed Step {i+1}")
            destination_agent = step.get("agent")
            task = step.get("task")

            if not all([destination_agent, task]):
                logging.error(f"Step '{step_name}' is missing 'agent' or 'task' definition. Skipping.")
                continue

            logging.info(f"--- Executing Step {i+1}: {step_name} ---")
            result = self.dispatcher.route_task(task, destination_agent)
            logging.info(f"--- Step {i+1} Result: {result} ---")

        logging.info("Workflow execution completed.")

