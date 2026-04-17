# AI Resume Analyzer

AI Resume Analyzer ek Streamlit based project hai jo PDF resume upload karke usme se basic information nikalta hai, skills identify karta hai, job field suggest karta hai, courses recommend karta hai, resume score deta hai, aur admin panel me user data show karta hai.

## Project Ka Simple Goal

Is project ka main purpose hai:

- resume upload karna
- resume se `name`, `email`, `phone`, `skills`, `pages` nikalna
- candidate ka likely field batana
- useful courses recommend karna
- resume writing score dikhana
- admin side par stored data dekhna

## Project Me Kya Kya Use Hua Hai

### 1. `Streamlit`

Frontend UI banane ke liye use hua hai.

Isse ye cheezein bani hain:

- file upload
- buttons and sidebar
- resume analysis output
- progress bar
- admin dashboard

### 2. `pdfminer3`

PDF resume ka text read karne ke liye use hua hai.

Ye resume ke andar ka raw text nikalta hai jisse aage analysis hota hai.

### 3. `spaCy`

Name detection ke liye use hua hai.

Project `en_core_web_sm` model se person name identify karne ki koshish karta hai.

### 4. `Regex`

Regex ka use email, phone number aur manual skill extraction ke liye hua hai.

### 5. `pymysql`

MySQL database se connect karne ke liye use hua hai.

Database me user ka analyzed data store hota hai.

### 6. `streamlit-tags`

Skills ko tag format me dikhane ke liye use hua hai.

### 7. `plotly`

Admin dashboard me charts dikhane ke liye use hua hai.

### 8. `Pillow`

Logo image load karne ke liye use hua hai.

### 9. `Courses.py`

Is file me different domains ke recommended courses aur videos ka data hai.

## Folder Structure

```text
AI_Resume_Analyzer/
├── App.py
├── resume_parser_custom.py
├── Courses.py
├── requirements.txt
├── README.md
├── .gitignore
├── Logo/
└── Uploaded_Resumes/
```

## Important Files Samjho

### `App.py`

Ye main application file hai.

Is file me:

- Streamlit UI hai
- PDF upload logic hai
- resume analysis flow hai
- recommendation logic hai
- resume score logic hai
- admin panel hai
- MySQL insert logic hai

### `resume_parser_custom.py`

Ye custom parser file hai.

Isme:

- PDF text extraction
- page count
- name extraction
- email extraction
- phone extraction
- skills extraction

### `Courses.py`

Is file me different career categories ke liye:

- courses
- resume videos
- interview videos

store kiye gaye hain.

### `requirements.txt`

Project ke Python packages is file me listed hain.

## Resume Analysis Ka Flow

1. User Streamlit app open karta hai.
2. User PDF resume upload karta hai.
3. Resume `Uploaded_Resumes/` folder me save hota hai.
4. `pdfminer3` PDF ka text extract karta hai.
5. `resume_parser_custom.py` name, email, phone, skills, pages nikalta hai.
6. `App.py` safety checks laga kar missing data ko improve karta hai.
7. Skills ke basis par field detect hota hai:
   - Data Science
   - Web Development
   - Android Development
   - iOS Development
   - UI/UX Development
8. Matching field ke hisaab se recommended skills aur courses dikhte hain.
9. Resume ke sections check hote hain:
   - Objective
   - Declaration
   - Hobbies
   - Achievements
   - Projects
10. Resume score calculate hota hai.
11. Result UI me show hota hai.
12. Data MySQL database me save hota hai.

## Admin Flow

Admin login ke baad:

- stored user data table me dikhta hai
- CSV export possible hai
- pie charts show hote hain

## Database Info

Project MySQL use karta hai.

Current code ke hisaab se connection:

```python
host='localhost'
user='avi'
password='1234'
db='cv'
```

Table name:

- `user_data`

## Run Karne Ka Simple Tarika

### 1. Virtual environment activate karo

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Packages install karo

```powershell
pip install -r requirements.txt
pip install nltk
pip install spacy==2.3.5
python -m spacy download en_core_web_sm
```

### 3. MySQL start karo

Ensure karo ki:

- MySQL server chal raha ho
- `cv` database accessible ho
- given username/password valid ho

### 4. Streamlit app run karo

```powershell
.\.venv\Scripts\python.exe -m streamlit run App.py
```

## Current Limitations

- DB credentials code ke andar hardcoded hain
- admin username/password hardcoded hai
- uploaded resumes project folder me save hote hain
- `nltk.download('stopwords')` app start par run hota hai
- kuch UI strings me encoding issue dikh sakta hai
- score logic basic keyword check par based hai

## Simple Roadmap

### Phase 1. Cleanup

- unused temp files remove karo
- `README.md` maintain karo
- `.gitignore` use karo
- duplicate files hatao

### Phase 2. Stability

- hardcoded DB credentials ko `.env` me shift karo
- admin credentials secure karo
- upload validation improve karo
- error handling better karo

### Phase 3. Parsing Improvement

- better name detection
- better skill extraction
- more accurate field prediction
- section detection ko robust banao

### Phase 4. UI Improvement

- cleaner layout
- better score cards
- grouped tips panel
- mobile-friendly interface

### Phase 5. Production Readiness

- deployment setup
- logging
- file cleanup automation
- proper config management

## Future Improvement Ideas

- ATS score improvement
- resume keyword matching against job description
- download report as PDF
- email notification
- authentication for admin panel
- better analytics

## Important Note

`Uploaded_Resumes/` folder me resumes store hote hain. Ye runtime data hai, isliye is folder ko completely delete nahi kiya gaya.

Safe garbage cleanup me generally:

- `__pycache__/`
- `.pyc` files
- temp files

remove karne chahiye.
