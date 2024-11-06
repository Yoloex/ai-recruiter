# AI Interview Agent README

## Overview

AI Interview Agent is an interactive, AI-powered application built using OpenAI and Gradio.
It simulates a job interview experience by taking job description data and processing user inputs to provide realistic interview scenarios.
The agent extracts job requirements, facilitates conversations with users, and provides text-to-speech and speech-to-text functionalities for an engaging, voice-driven experience.

## Features

- Job Description Input:

    Users can input company name, job title, job description, company mission, and core values.
- Automatic Requirement Extraction:
  
    Extracts key requirements from the job description for better interview responses.
- Interactive Chat Interface:
  
  Uses Gradio's Chatbot component for interaction.
- Voice Integration:
  
  The system utilizes text-to-speech (TTS) and speech-to-text (STT) for an immersive experience.
- Dynamic Presets:
  
  Customizes interview responses based on the job information provided.
- Session Management:
  
  Start and clear the interview session through simple button clicks.

## Installation

1. Clone the repository

   ```bat
   git clone git@github.com:Yoloex/ai-recruiter.git
   cd ai-recruiter
   ```

2. Install dependencies

   ```bat
   pip install -r requirements.txt
   ```

## Usage

```bat
python run.py
```

The Gradio UI will launch. Then, fill in Company, Job Title, Job Description, Company Core Values and Mission.

## Future Improvements

- Export conversation history
- Reduce latency
- Job Description and Resume PDF Parsing
