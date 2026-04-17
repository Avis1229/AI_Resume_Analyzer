import spacy
import re
import os
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io

class ResumeParser:
    def __init__(self, resume_file):
        self.resume_file = resume_file
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spacy model...")
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
    def get_extracted_data(self):
        text = self._extract_text_from_pdf()
        doc = self.nlp(text)
        
        data = {
            'name': self._extract_name(doc, text),
            'email': self._extract_email(text),
            'mobile_number': self._extract_phone(text),
            'skills': self._extract_skills(text),  # 🔥 IMPROVED
            'no_of_pages': self._get_number_of_pages(),
            'text': text
        }
        return data
    
    def _extract_text_from_pdf(self):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams(all_texts=True))
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        
        text = ""
        with open(self.resume_file, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
        
        converter.close()
        fake_file_handle.close()
        return text
    
    def _get_number_of_pages(self):
        count = 0
        with open(self.resume_file, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                count += 1
        return count
    
    def _extract_name(self, doc, text):
        """Extract a likely name while handling bullet and inline formats."""
        
        # Fix 1: remove bullet characters from the raw text first
        clean_text = text.replace('•', ' | ').replace(',', ' ')
        lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
        
        # Keywords that should not be treated as names
        non_name_keywords = {
            'career', 'objective', 'education', 'technical', 'skills', 'certifications',
            'projects', 'strengths', 'languages', 'experience', 'summary', 'profile',
            'contact', 'phone', 'email', 'address', 'linkedin', 'github', 'resume',
            'machine', 'learning', 'data', 'science', 'artificial', 'intelligence',
            'deep', 'python', 'java', 'developer', 'engineer', 'analyst',
            'student', 'professional', 'work', 'bca', 'btech', 'mba', 'bachelor', 'master',
            'university', 'mentor', 'bareilly', 'uttar', 'pradesh', 'unified', 'invertis'
        }
        
        # Fix 2: inspect the first 10 lines after better cleaning
        for line in lines[:10]:
            # Temporarily remove email and phone text
            temp_line = re.sub(r'\S+@\S+\.\S+', '', line)  # Email remove
            temp_line = re.sub(r'[\+\d\(\)\-\.\s]{7,}', '', temp_line)  # Phone remove
            temp_line = re.sub(r'linkedin\.com/\S+', '', temp_line)  # LinkedIn remove
            temp_line = temp_line.strip()
            
            # Keep only likely alphabetic name candidates
            if re.match(r'^[A-Za-z\s\.\-]+$', temp_line):
                words = temp_line.split()
                # A realistic name usually has 2 to 4 words
                if 2 <= len(words) <= 4:
                    # Exclude lines containing known non-name keywords
                    temp_lower = temp_line.lower()
                    if not any(keyword in temp_lower for keyword in non_name_keywords):
                        return temp_line.title()
        
        # Fix 3: if a line is mixed, try the first two words
        for line in lines[:5]:
            words = line.replace('|', ' ').split()
            # Check the first two words
            if len(words) >= 2:
                candidate = ' '.join(words[:2])
                # Keep only alphabetic candidates
                if re.match(r'^[A-Za-z\s]+$', candidate):
                    cand_lower = candidate.lower()
                    if not any(keyword in cand_lower for keyword in non_name_keywords):
                        return candidate.title()
        
        # Fallback: Spacy entity
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text.strip()
                invalid = ['machine learning', 'deep learning', 'data science', 'unified mentor']
                if not any(inv in name.lower() for inv in invalid):
                    if re.match(r'^[A-Za-z\s]+$', name):
                        return name.title()
        
        return "Unknown"
    
    def _extract_email(self, text):
        """Extract email while handling bullet-separated text."""
        # Fix: replace bullets with spaces
        clean_text = text.replace('•', ' ').replace(',', ' ')
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, clean_text)
        return emails[0] if emails else "Not Found"
    
    def _extract_phone(self, text):
        """Extract phone number while handling +91 and bullet-separated text."""
        # Fix: remove bullets before matching
        clean_text = text.replace('•', ' ').replace(',', ' ')
        
        patterns = [
            r'\+91\s?\d{10}',                    # +91 8127123913
            r'\+91\d{10}',                       # +918127123913
            r'\d{10}',                           # 8127123913
            r'\d{5}\s?\d{5}',                    # 81271 23913
        ]
        
        for pattern in patterns:
            phones = re.findall(pattern, clean_text)
            if phones:
                phone = phones[0].replace(' ', '')
                if len(phone) == 10:
                    return phone
                elif len(phone) == 12 and phone.startswith('91'):
                    return '+' + phone
                elif phone.startswith('+91'):
                    return phone
                return phone
        
        return "Not Found"
    
    def _extract_skills(self, text):
        """Extract skills using keyword matching and simple fallbacks."""
        # Fix: clean the text to handle commas and special characters
        # Example: "JavaScript,MERN Stack,React.js" has no space after commas
        text_clean = text.replace(',', ', ').replace('•', ' ')
        text_lower = text_clean.lower()
        
        # Fix: use a broader skills database
        skills_db = {
            # Programming Languages
            'python', 'java', 'c', 'c++', 'c#', 'javascript', 'typescript', 'go', 'rust', 
            'ruby', 'perl', 'scala', 'php', 'swift', 'kotlin', 'dart', 'r',
            
            # Web Development
            'html', 'css', 'react', 'react.js', 'angular', 'vue', 'node.js', 'nodejs',
            'express', 'express.js', 'django', 'flask', 'next.js', 'gatsby',
            'mern stack', 'mean stack', 'full stack', 'frontend', 'backend',
            'web development', 'rest api', 'graphql', 'json', 'xml',
            
            # Databases
            'mongodb', 'mongo', 'mysql', 'postgresql', 'sqlite', 'redis', 
            'firebase', 'supabase', 'dynamodb', 'cassandra', 'oracle',
            
            # Tools & Technologies
            'git', 'github', 'gitlab', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'jenkins', 'ci/cd', 'terraform', 'nginx', 'apache',
            
            # Data Science / AI
            'tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning',
            'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'data analysis',
            'data visualization', 'statistics', 'nlp', 'computer vision', 'ai',
            'artificial intelligence', 'ml', 'dl', 'data mining', 'big data',
            'tableau', 'power bi', 'excel', 'plotly', 'jupyter',
            
            # Mobile Development
            'android', 'ios', 'flutter', 'react native', 'xcode', 'android studio',
            
            # Design & Others
            'figma', 'adobe xd', 'sketch', 'photoshop', 'illustrator', 'ui design',
            'ux design', 'wireframing', 'prototyping', 'shopify', 'wordpress',
            'vs code', 'visual studio code', 'antigravity', 'stitch', 'vercel'
        }
        
        found_skills = []
        
        for skill in skills_db:
            # Fix: check multiple matching patterns
            patterns = [
                r'\b' + re.escape(skill) + r'\b',  # Exact match
                r'\b' + re.escape(skill.replace('.', '')) + r'\b',  # Without dots (react.js -> reactjs)
                r'\b' + re.escape(skill.replace(' ', '')) + r'\b',  # Without spaces (mern stack -> mernstack)
            ]
            
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    # Add the skill in a cleaner display format
                    display_skill = skill.title().replace('.Js', '.js').replace(' Ai', ' AI').replace(' Ml', ' ML')
                    if display_skill not in found_skills:
                        found_skills.append(display_skill)
                    break
        
        # Fix: if only 1-2 skills are found, try manual extraction from text
        if len(found_skills) < 3:
            # Search for a skills section
            lines = text_lower.split('\n')
            for i, line in enumerate(lines):
                if 'skills' in line and i < len(lines) - 1:
                    # Skills are likely to appear in the next 3 lines
                    for j in range(1, 4):
                        if i + j < len(lines):
                            skill_line = lines[i + j]
                            # Skills may be separated by commas, semicolons, colons, or pipes
                            potential_skills = re.split(r'[,;:\|]', skill_line)
                            for ps in potential_skills:
                                ps_clean = ps.strip()
                                # Keep only reasonable text fragments
                                if len(ps_clean) > 2 and re.match(r'^[a-z0-9\s\+\.]+$', ps_clean):
                                    if ps_clean not in [s.lower() for s in found_skills]:
                                        # Prefer common skill-like words or longer valid fragments
                                        common_skills = ['javascript', 'react', 'node', 'mongodb', 'express', 'html', 'css', 'python', 'java']
                                        if any(cs in ps_clean for cs in common_skills) or len(ps_clean) > 3:
                                            found_skills.append(ps_clean.title())
        
        return found_skills if found_skills else ['Not Specified']
