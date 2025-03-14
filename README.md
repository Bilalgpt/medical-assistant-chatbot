# MediChat: AI Medical Database Assistant

MediChat is an intelligent chat interface that allows medical professionals to query and analyze medical data using natural language. Built with LangChain and Groq's LLM models, this application provides an intuitive way to explore patient records, diagnoses, medications, and treatment plans without needing to write SQL queries.

## Features

* **Natural Language Queries**: Ask questions about medical data in plain English
* **Interactive Dashboard**: View key statistics and visualizations of your medical database
* **Multi-Database Support**: Connect to either SQLite or external MySQL databases
* **Intelligent Visualization**: Automatic chart generation for relevant queries
* **Multiple AI Models**: Choose from different LLM models for different needs
* **Comprehensive Medical Schema**: Includes patients, doctors, medications, records, and prescriptions
* **Sample Data Generator**: Automatic creation of realistic medical data for testing

## Getting Started

### Prerequisites

* Python 3.8+
* Groq API key (obtain from console.groq.com)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Bilalgpt/medical-assistant-chatbot.git
cd medical-assistant-chatbot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run medical_chatbot.py
```

The database will be automatically initialized with sample medical data on first run.

## Usage

1. Enter your Groq API key in the sidebar
2. Select your preferred AI model
3. Start asking questions about the medical database:
   * "How many patients have hypertension?"
   * "List all medications prescribed for depression"
   * "What are the most common diagnoses?"
   * "Which doctor has seen the most patients?"
   * "Show me all patients with type 2 diabetes"

## Database Schema

MediChat uses a comprehensive medical database with the following tables:
* **patients**: Patient demographics, contact information
* **doctors**: Physician information, specializations
* **medications**: Drug information, categories, side effects
* **medical_records**: Patient visits, diagnoses, treatment plans
* **prescriptions**: Medication orders, dosages, instructions

## Connecting to External Databases

To connect to an external MySQL medical database:
1. Select "Connect to external Medical Database" in the sidebar
2. Enter your MySQL connection details
3. Make sure your external database schema matches MediChat's schema

## Customization

You can modify the `medical_database.py` file to:
* Add more sample data
* Extend the database schema
* Change the types of medical conditions and medications

## Limitations

* Currently supports SQLite and MySQL databases
* Requires internet connection for LLM access
* Limited to the medical schema defined in the application
