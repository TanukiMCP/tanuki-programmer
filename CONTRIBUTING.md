# Contributing to Tanuki-Programmer

We welcome contributions to the Tanuki-Programmer project! By contributing, you help us build a more powerful and versatile autonomous programming system. Please take a moment to review this document to understand how you can contribute effectively.

## 1. Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## 2. How to Contribute

### 2.1. Reporting Bugs

-   Before submitting a new bug report, please check the existing issues to see if your problem has already been reported.
-   If not, open a new issue and provide a clear and concise description of the bug.
-   Include steps to reproduce the bug, expected behavior, actual behavior, and any relevant error messages or screenshots.
-   Specify your operating system, Python version, Docker version, and any other relevant environment details.

### 2.2. Suggesting Enhancements

-   We welcome ideas for new features or improvements to existing ones.
-   Open a new issue and clearly describe the enhancement. Explain why it would be valuable to the project and how it might be implemented.

### 2.3. Contributing Code

We appreciate code contributions, whether it's a bug fix, a new feature, or an improvement to existing code.

#### General Guidelines:

-   **Fork the Repository:** Start by forking the `tanuki-programmer` repository on GitHub.
-   **Create a New Branch:** Create a new branch for your feature or bug fix from the `main` branch. Use a descriptive name (e.g., `feature/add-new-agent`, `bugfix/fix-api-auth`).
-   **Code Style:** Adhere to the existing code style (e.g., PEP 8 for Python). We use `flake8` for linting (see `.github/workflows/ci.yml`).
-   **Tests:** Write unit and integration tests for your changes. Ensure all existing tests pass.
-   **Documentation:** Update relevant documentation (`docs/`, `README.md`) for any new features or significant changes.
-   **Commit Messages:** Write clear, concise, and descriptive commit messages. Follow conventional commits if possible (e.g., `feat: add new agent type`, `fix: resolve sandbox timeout issue`).
-   **Pull Requests (PRs):**
    -   Open a pull request to the `main` branch of the `tanuki-programmer` repository.
    -   Provide a clear title and description for your PR.
    -   Reference any related issues (e.g., `Closes #123`, `Fixes #456`).
    -   Be responsive to feedback and be prepared to iterate on your changes.

#### Specific Areas for Code Contributions:

-   **Agent Development:** Implement new specialized agents or improve existing ones.
-   **Tool Integrations:** Add support for new external tools (linters, debuggers, cloud APIs).
-   **Sandbox Enhancements:** Improve the security, performance, or language support of the code execution sandbox.
-   **Orchestration Logic:** Refine the `Orchestrator`'s decision-making, planning, or response aggregation.
-   **Resource Management:** Optimize adapter loading, memory management, or monitoring.
-   **Data Synthesis:** Improve data generation strategies or add new datasets.
-   **Deployment:** Enhance deployment scripts or add support for new platforms.
-   **UI/CLI Improvements:** Improve the user experience of the local interfaces.

## 3. Development Environment Setup

Refer to `docs/setup_guide.md` for detailed instructions on setting up your development environment, including Python, Docker, and local LLM setup.

## 4. Licensing

By contributing to Tanuki-Programmer, you agree that your contributions will be licensed under the [MIT License](LICENSE).

Thank you for your interest in contributing to Tanuki-Programmer! We look forward to your valuable input.
