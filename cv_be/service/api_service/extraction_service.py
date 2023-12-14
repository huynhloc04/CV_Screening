from time import time
from config import CV_PROMPT_PATH, JD_PROMPT_PATH, CVPDF_PATH, JDTXT_PATH
import pdftotext
from fastapi import HTTPException, status
from typing import Any
import os


class CvExtraction:
    
    def text_extract(filename):
        with open(filename, 'rb') as f:
            pdf = pdftotext.PDF(f)
        text = ''.join(pdf)
        return text
        
    @staticmethod
    async def add_query(prompt_template):
        """add query to the data to create prompt"""
        with open(CV_PROMPT_PATH, 'r') as file:
            prompt = file.read()
        prompt_template += prompt
        print(" >> Add query")
        return prompt_template
    
    @staticmethod
    def get_cvtext(cv_file: str):
        """extract text from cv"""
        # only read pdf
        cv_path = os.path.join(CVPDF_PATH, cv_file)
        if cv_path.lower().endswith('.pdf'):
            text = CvExtraction.text_extract(cv_path)
        else:
            with open(cv_path, 'r') as file:
                text = file.read()
        prompt_template = f"""
        [Resume]: 
        {text}
        
        [Extract Requirements]
        """  
        print(" >> Get cv text")
        return prompt_template
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot get CV text data!")
    


class JdExtraction:
    
    def text_extract(filename):
        with open(filename, 'rb') as f:
            pdf = pdftotext.PDF(f)
        text = ''.join(pdf)
        return text
        
    @staticmethod
    async def add_query(prompt_template):
        """add query to the data to create prompt"""
        with open(JD_PROMPT_PATH, 'r') as file:
            prompt = file.read()
        prompt_template += prompt
        print(" >> Add query")
        return prompt_template
    
    @staticmethod
    def get_jdtext(jd_file: str):
        
        jd_path = os.path.join(JDTXT_PATH, jd_file)
        if jd_path.lower().endswith('.txt'):
            #   Read JD text file
            with open(jd_path, 'r') as file:
                text = file.read()
            prompt_template = f"""
            [Job Description]: 
            {text}
            
            [Extract Requirements]
            """  
            print(" >> Get JD text")
            return prompt_template
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot get JD text data!")
    

