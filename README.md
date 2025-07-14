# Employee Work Time Recognizer

## Overview
A modular Python application that uses your laptop webcam to automatically recognize and log employee work times, free times, and activities (such as working, sleeping, eating, and idling). Designed for easy extension and clear code organization.

## Features
- Webcam integration (laptop webcam)
- Activity recognition: working, sleeping, eating, idling
- Time logging with timestamps
- Local storage of logs (CSV/JSON)
- Report generation (daily/weekly summaries)
- (Optional) Simple dashboard UI

## Project Structure
```
employee-work-recognizer/
│
├── camera/                # Webcam access and video capture
├── detection/             # Activity recognition (ML models, logic)
├── logging/               # Time logging and storage
├── reporting/             # Report generation
├── ui/                    # (Optional) User interface/dashboard
├── main.py                # Entry point
├── requirements.txt       # Dependencies
└── README.md              # Project overview
```

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Code Organization Principles
- Each feature/component is in its own directory.
- Code is modular and easy to extend.
- Clear separation of concerns for maintainability.

## License
MIT License 