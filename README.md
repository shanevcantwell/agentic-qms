# Agentic Quality Management System (AQMS)

This repository implements a multi-agent framework for robust AI synthesis based on the principles of ISO 9001. It is designed not as a simple command hierarchy, but as a resilient, self-auditing quality management system capable of continuous, evidence-based improvement.

## Core Principles

*   **Tribal Cognition:** Treats LLMs from different providers (e.g., Google, Anthropic) as distinct "cognitive tribes" with unique strengths and biases, leveraging their diversity for more robust outcomes.
*   **Quality Management System (QMS):** The architecture is modeled on ISO 9001, focusing on process control, evidence-based validation, and continuous improvement through a Plan-Do-Check-Act cycle.
*   **Configuration as Code:** All system prompts, workflow definitions, and governance policies are treated as version-controlled artifacts within the `/qms` directory.
*   **Separation of Concerns:** The core framework logic (`/src`), the QMS configuration (`/qms`), and generated documentation (`/docs`) are strictly separated.

## Architectural Overview

*   **/qms/**: The heart of the QMS. Contains all configuration for agent personas (prompts), process definitions (workflows), and high-level system rules (governance).
*   **/src/**: Contains all Python source code for the agent framework, the agents themselves, and any supporting tools.
*   **/docs/**: Contains generated artifacts, such as the HTML diagrams produced by the system. This directory can be used for publishing results.
*   **/scripts/**: Houses utility and setup scripts for managing the repository.

## Getting Started

1.  Clone the repository: `git clone <repo_url>`
2.  Navigate to the directory: `cd agentic-qms`
3.  Set up the Python environment: `python -m venv .venv && source .venv/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt` (once `pyproject.toml` is populated)
5.  Run an initial workflow: `python -m src.framework.orchestrator --workflow qms/workflows/diagram_generation.yaml`
