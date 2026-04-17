# AI Resume Analyzer

AI Resume Analyzer is a Streamlit-based project that analyzes PDF resumes, extracts key details, identifies likely career domains, recommends courses and skills, and calculates a simple resume score.

## Project Goal

The main purpose of this project is to:

- upload a resume in PDF format
- extract `name`, `email`, `phone`, `skills`, and `page count`
- identify the likely job domain of the candidate
- recommend useful skills and courses
- calculate a basic resume writing score
- store analyzed data in a MySQL database

## Technologies Used

### 1. `Streamlit`

Used to build the user interface.

It powers:

- file upload
- sidebar controls
- resume analysis output
- progress bars
- admin dashboard

### 2. `pdfminer3`

Used to read and extract raw text from PDF resumes.

### 3. `spaCy`

Used for name detection through the `en_core_web_sm` model.

### 4. `Regex`

Used to extract email addresses, phone numbers, and fallback skills manually.

### 5. `pymysql`

Used to connect the app with a MySQL database.

### 6. `streamlit-tags`

Used to display skills in tag format.

### 7. `plotly`

Used for charts and analytics in the admin section.

### 8. `Pillow`

Used to load and display the project logo.

### 9. `Courses.py`

Stores course recommendations and video links for different career domains.

## Folder Structure

```text
AI_Resume_Analyzer/
|-- App.py
|-- resume_parser_custom.py
|-- Courses.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- AI_Resume_Analyzer_Roadmap.pdf
|-- Logo/
`-- Uploaded_Resumes/
```

## Important Files

### `App.py`

This is the main application file.

It contains:

- Streamlit UI
- PDF upload logic
- resume analysis flow
- recommendation logic
- resume scoring
- admin dashboard
- MySQL insert logic

### `resume_parser_custom.py`

This is the custom parsing module.

It handles:

- PDF text extraction
- page counting
- name extraction
- email extraction
- phone number extraction
- skills extraction

### `Courses.py`

This file contains:

- recommended courses
- resume improvement videos
- interview preparation videos

### `requirements.txt`

Lists the Python packages required for this project.

## Resume Analysis Flow

1. The user opens the Streamlit app.
2. The user uploads a PDF resume.
3. The resume is saved inside the `Uploaded_Resumes/` folder.
4. `pdfminer3` extracts the text from the PDF.
5. `resume_parser_custom.py` extracts name, email, phone, skills, and page count.
6. `App.py` applies safety checks to improve weak or missing parser output.
7. The app predicts a likely field based on detected skills:
   - Data Science
   - Web Development
   - Android Development
   - iOS Development
   - UI/UX Development
8. Recommended skills and courses are shown based on the detected field.
9. The resume is checked for important sections such as:
   - Objective
   - Declaration
   - Hobbies
   - Achievements
   - Projects
10. A resume score is calculated.
11. The final result is displayed in the UI.
12. The analyzed data can be stored in MySQL.

## Database Information

This project uses MySQL.

The current connection settings in code are:

```python
host='localhost'
user='avi'
password='1234'
db='cv'
```

Table name:

- `user_data`

## How To Run

### 1. Activate the virtual environment

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
pip install nltk
pip install spacy==2.3.5
python -m spacy download en_core_web_sm
```

### 3. Start MySQL

Make sure:

- the MySQL server is running
- the `cv` database is accessible
- the configured username and password are valid

### 4. Run the Streamlit app

```powershell
.\.venv\Scripts\python.exe -m streamlit run App.py
```

## Current Limitations

- Database credentials are hardcoded in the code.
- Admin username and password are hardcoded.
- Uploaded resumes are saved in the project folder.
- `nltk.download('stopwords')` runs at startup.
- Some UI strings may still have encoding issues.
- The scoring logic is still based on basic keyword checks.

## Roadmap

### Phase 1. Cleanup

- remove unused temporary files
- maintain the `README.md`
- use `.gitignore` properly
- remove duplicate or unnecessary files

### Phase 2. Stability

- move hardcoded database credentials into an `.env` file
- secure admin credentials
- improve upload validation
- improve error handling

### Phase 3. Parsing Improvement

- improve name detection
- improve skill extraction
- improve field prediction accuracy
- make section detection more robust

### Phase 4. UI Improvement

- cleaner layout
- better score cards
- grouped tips panel
- better mobile responsiveness

### Phase 5. Production Readiness

- deployment setup
- logging
- automated file cleanup
- proper configuration management

## Future Improvement Ideas

- better ATS-style scoring
- resume matching against job descriptions
- downloadable PDF report
- email notifications
- stronger authentication for admin access
- improved analytics

## Important Note

The `Uploaded_Resumes/` folder contains runtime resume files, so it was not fully deleted during cleanup.

Safe garbage cleanup usually includes:

- `__pycache__/`
- `.pyc` files
- temporary files
