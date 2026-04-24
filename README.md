# Smart-Seat
Smart automatic seat allocation system 

#Problem Statement


# Tech Stack
## First option
- Backend: Python(FastAPI)
- Frontend: JavaScript,HTML,CSS
- Storage:SQL

# Authors
- Nomfundo Mtiyane
- Michael
- Daylen
- Amahle
- Caitlin

# How to Run the Project


## 1. Clone the Repository (terminal or GitHub desktop)

## 2. Backend Setup using terminal (These instructions can vary depending on how you want to set it up)
- Note: Use the folder name that you clone the repository to on your device e.g. Smart-Seat
- Run the following commands:
  - cd Smart-Seat
  - python -m venv venv (Create the virtual environment if you want to use one, although not necessarily required)
  - venv\Scripts\activate (If using venv)
  - pip install -r requirements.txt (Install dependencies)
  - uvicorn backend.main:backend --reload (Run the FastAPI server)

- To stop the server, press CTRL + C.
- The backend runs at: http://127.0.0.1:8000
- Swagger UI for testing: http://127.0.0.1:8000/docs

## 3. Frontend Setup (Recommended method - Visual Studio Code)
- Install the extension for viewing html files: Live Preview
- Once installed, open the project in VS Code and navigate to the frontend folder
- Inside is all the frontend files
- To see the UI display, right click on an html file and click "Show Preview"
- The user flow begins at home-page.html
