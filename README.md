# Heart Health Assistant

A simple Flask web app that asks a few health questions and gives a rule-based heart risk summary in a conversational chat interface.

## Features

- Chat-style UI instead of a plain form
- Asks about symptoms:
  - Chest pain
  - Shortness of breath
  - Sweating
  - Fatigue
  - Dizziness
- Asks about basic health history:
  - Age
  - High blood pressure
  - Diabetes
  - High cholesterol
- Returns a risk level:
  - Low Risk
  - Medium Risk
  - High Risk
- Shows a risk score percentage
- Gives next-step guidance and simple medical context
- Includes a dark-themed, mobile-friendly UI

## Requirements

- Python 3.10 or newer
- Flask

## Setup

1. Open a terminal in the project folder.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the App

Start the Flask server:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## How It Works

The app uses simple rule-based logic. For example:

- Chest pain + shortness of breath + sweating usually gives a high-risk result
- Mild symptoms with fewer warning signs may produce medium risk
- Fatigue alone or no major symptoms usually produces low risk

The result includes:

- Risk score
- Possible related conditions
- Recommended medical checks
- Warning signs to watch for
- A short action checklist

## Project Structure

```text
.
├── app.py
├── requirements.txt
└── templates/
    └── index.html
```

## Notes

This project is for educational purposes only and does not replace professional medical advice. If someone has severe chest pain, trouble breathing, or other emergency symptoms, seek immediate medical care.
