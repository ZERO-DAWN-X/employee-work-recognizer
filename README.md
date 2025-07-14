# Employee Work Time Recognizer

![Project Status](https://img.shields.io/badge/status-active-brightgreen)

---

> **A modern, modular Python application for recognizing and logging employee work activities using your laptop webcam.**

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [User Interface](#user-interface)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Code Organization Principles](#code-organization-principles)
- [License](#license)

---

## Overview
Employee Work Time Recognizer leverages computer vision to automatically detect and log work, free, and idle times. Designed with a focus on modularity, clean code, and a modern user experience.

---

## Features
- Minimal, modern PyQt5 GUI
- Real-time webcam feed
- Modular architecture for easy extension
- Activity recognition (work, sleep, eat, idle) *(in progress)*
- Local time logging and reporting *(upcoming)*
- Professional UX/UI principles

---

## User Interface

![GUI Screenshot](ui/screenshot.png)

*Above: Minimal, modern interface with clear controls and a central webcam feed. Designed for clarity and ease of use.*

---

## Project Structure

| Folder/File      | Purpose                                 |
|------------------|-----------------------------------------|
| `camera/`        | Webcam access and video capture         |
| `detection/`     | Activity recognition logic and models   |
| `logging/`       | Time logging and storage                |
| `reporting/`     | Report generation                       |
| `ui/`            | User interface (PyQt5)                  |
| `main.py`        | Application entry point                 |
| `requirements.txt`| Dependencies                            |
| `README.md`      | Project overview                        |

---

## Setup & Installation

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd employee-work-recognizer
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```sh
   python main.py
   ```

---

## Usage
- Launch the app to access the webcam and view the modern GUI.
- Use the Start/Stop buttons to control the webcam feed.
- Future updates will add activity detection, logging, and reporting.

---

## Code Organization Principles
- **Component-based:** Each feature is in its own directory.
- **Modular:** Code is easy to extend and maintain.
- **Separation of concerns:** UI, detection, logging, and reporting are clearly separated.
- **Professional UX/UI:** Clean, minimal, and user-focused design.

---

## License
MIT License 