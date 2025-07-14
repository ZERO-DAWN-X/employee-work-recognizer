# Product Requirements Document (PRD)

## Product Name
Employee Work Time Recognizer

## Objective
Automatically recognize and log an employee’s work times, free times, and activities (e.g., working, sleeping, eating, idling) using a laptop webcam.

## Key Features
1. **Webcam Integration**
   - Access and capture video from the laptop’s webcam.
2. **Activity Recognition**
   - Detect and classify activities: working, sleeping, eating, idling/free time.
3. **Time Logging**
   - Log the start and end times of each detected activity.
   - Store logs locally (CSV, JSON, or database).
4. **Reporting**
   - Generate daily/weekly reports of time spent on each activity.
5. **User Interface (Optional, for later)**
   - Simple dashboard to view logs and reports.

## Constraints
- Runs locally on a laptop (Windows).
- Uses only the laptop’s webcam.
- All data stays on the local machine for privacy.

## Success Criteria
- Accurately detects and logs activities.
- Easy to use and extend.
- Well-organized, modular codebase with clear component separation.

## Project Structure
- **camera/**: Webcam access and video capture
- **detection/**: Activity recognition logic and models
- **logging/**: Time logging and storage
- **reporting/**: Report generation
- **ui/**: (Optional) User interface/dashboard
- **main.py**: Application entry point
- **requirements.txt**: Dependencies
- **README.md**: Project overview

## Development Approach
- Build step by step, verifying each part before moving to the next.
- Organize code for clarity, reusability, and maintainability.
- Use modular components for each feature. 