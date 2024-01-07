# Redash Chat Add-On for YouTube Data Exploration

## Table of content
- [Redash Chat Add-On for YouTube Data Exploration](#redash-chat-add-on-for-youtube-data-exploration)
  - [Overview](#overview)
  - [Business Need](#business-need)
  - [Project Scope](#project-scope)
  - [Key Features](#key-features)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [Data Sources](#data-sources)
  - [Screenshots](#screenshots)
  - [Contributions](#contributions)
  - [License](#license)

## Overview
Welcome to the GitHub repository for our innovative Redash chat add-on designed to revolutionize data analysis capabilities, with a specific focus on comprehensive YouTube data exploration. This project aims to empower our team members by enabling seamless conversations in a question-and-answer format, allowing for autonomous knowledge discovery through natural language interactions.

## Business Need
Our company recognizes the need for enhanced data analysis capabilities to extract deep, meaningful, and actionable insights from our business intelligence (BI) platforms. The project extends to the development of a Redash add-on in the frontend and an intelligent backend capable of translating user queries into various forms:

- Summaries of visualizations in current dashboards
- Insights about data returned by existing SQL queries
- Auto-generation of SQL queries and visualizations
- Auto-generation of new Redash dashboards from existing and auto-generated SQL queries

By bridging the gap between natural language and complex SQL queries, this tool aims to democratize data analytics, making it accessible to team members with non-technical backgrounds. The integration of this add-on with Redash is expected to streamline analytical processes, making data exploration more efficient, user-friendly, and conducive to strategic decision-making.

## Project Scope
The scope of this project encompasses the development of both frontend and backend components. The Redash chat add-on will facilitate interactive conversations, while the intelligence backend will interpret user queries, generate SQL queries, and provide insightful visualizations. The backend API developed during this project holds the potential for broader usability in various data analysis and BI projects.

## Key Features
- Natural language interaction for querying Redash dashboards and connected databases
Summarization of visualizations
- Insights extraction from existing SQL queries
- Auto-generation of SQL queries and visualizations
- Auto-generation of new Redash dashboards

## Installation

1. **Clone this Repository:**

    Clone this repository:
    ```bash 
    git clone https://github.com/AbelBekele/10-Academy-Week-2.git
    ```

    Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. **Set Up Python Environment:**

    ```bash
    python -m venv your_env_name
    ```

    Replace `your_env_name` with the desired name for your environment.
    
    **Activate the Environment:**

    - On Windows:

    ```bash
    .\your_env_name\scripts\activate
    ```

    - On macOS/Linux:

    ```bash
    source your_env_name/bin/activate
    ```

## Getting Started

Explore the repository to understand the project structure and components. Refer to the [Installation](#installation) section for setup instructions. Detailed documentation for each component is available within their respective folders.

Navigate to the `Redash/app/components/chat` folder to the frontend part of the project.

Navigate to the `Redash/redash/handlers/chatbot` folder to the backend part of the project.

## Screenshots

Navigate to the `screenshots` folder to view visual representations of the project.

## Contributions

We welcome contributions to this repository. Please submit pull requests with improvements to code, documentation, or visualizations. Refer to the [Contribution Guidelines](CONTRIBUTING.md) for details.

## License

This repository is licensed under the [MIT License](LICENSE).