
from config import SCORING_PROMPT, JDTXT_PATH, JDSCORE_PATH, SCORING_TABLE, CV_EXTRACTION_PATH, JD_EXTRACTION_PATH
from service.api_service.extraction_service import CvExtraction, JdExtraction
from config import OPENAI_MODEL
import openai
import os
import json
import numpy as np
from typing import List, Dict, Any
from numpy.linalg import norm
from service.api_service.openai_service import OpenAIService
import env

openai.api_key = env.OPENAI_API_KEY


class ScoringService:

    def pdf2text() -> None:
        for jd_file in os.listdir(JDTXT_PATH):
            if jd_file.endswith('.pdf'):
                text = JdExtraction.text_extract(os.path.join(JDTXT_PATH, jd_file))
                with open(os.path.join(JDTXT_PATH, jd_file[:-4]+'.txt'), 'w') as file:
                    file.write(text)
                #   Remove JD pdf file
                os.remove(os.path.join(JDTXT_PATH, jd_file))
    
    
    @staticmethod
    def get_json_info(json_data: Dict, features: List[str], spec_features=List[str], is_cv=False):
        data_str = "\n"
        for feature, spec_feature in zip(features, spec_features):
            if is_cv:
                data_str += f"     {feature}:\n"
            data = json_data[feature]
            
            if isinstance(data, list):
                for info in data:
                    if isinstance(info, dict) :                    
                        if spec_feature in info.keys():
                            data_ext = "; ".join(info[spec_feature])
                            data_str += f"\t- {spec_feature}: {data_ext}\n"
                        else:
                            for key, val in info.items():
                                data_ext = "; ".join(val)
                                data_str += f"\t- {key}: {data_ext}\n"
                        data_str += "\n"
                    elif isinstance(info, str):
                        data_str += f"\t- {info}\n"
            elif isinstance(data, dict):                  
                if spec_feature in data.keys():
                    data_ext = "; ".join(data[spec_feature])
                    data_str += f"\t- {spec_feature}: {data_ext}\n"
                else:
                    for key, val in data.items():
                        data_ext = "; ".join(val)
                        data_str += f"\t- {key}: {data_ext}\n" 
        return data_str
    
    
    @staticmethod    
    def gen_pair(cv_file: str, jd_file: str):
        with open(SCORING_PROMPT, 'r') as file:
            template = file.read()
        #   Read extracted CV
        with open(os.path.join(CV_EXTRACTION_PATH, cv_file)) as file:
            cv_json = json.load(file)  

        with open(os.path.join(JD_EXTRACTION_PATH, jd_file)) as file:
            jd_json = json.load(file)  
                
        #   Get "Job_title" from CV and JD respectively
        cv_title = ScoringService.get_json_info(cv_json, 
                                ["personal_information", "industry"],
                                ["desired_position", None],
                                is_cv=True)
        jd_title = ScoringService.get_json_info(jd_json, ["job_title"], [None])
                
        #   Get "Job_summary" from CV and JD respectively
        cv_summary = ScoringService.get_json_info(cv_json, ["summary"], [None], is_cv=True)
        jd_summary = ScoringService.get_json_info(jd_json, ["job_summary"], [None])
                
        #   Get "Qualifications and Skills" from CV and JD respectively
        cv_qua = ScoringService.get_json_info(cv_json, 
                                              ["skills", "certificates", "achievements_and_honors"], 
                                              [None, None, None], 
                                              is_cv=True)
        jd_qua = ScoringService.get_json_info(jd_json, ["qualifications_and_skills"], [None])
                
        #   Get "Education" and Skills from CV and JD respectively
        cv_edu = ScoringService.get_json_info(cv_json, ["education"], [None], is_cv=True)
        jd_edu = ScoringService.get_json_info(jd_json, ["education"], [None])
                
        #   Get "Knowledge and Experiences" and Skills from CV and JD respectively
        cv_exper = ScoringService.get_json_info(cv_json, 
                                ["project", "experience", "publications"], 
                                [None, None, None], 
                                is_cv=True)
        jd_exper = ScoringService.get_json_info(jd_json, ["expertise_and_experience"], [None])
                
        #   Get "Knowledge and Experiences" and Skills from CV and JD respectively
        cv_benefit = ScoringService.get_json_info(cv_json, 
                                ["personal_information"], 
                                ["desired_salary"], 
                                is_cv=True)
        jd_benefit = ScoringService.get_json_info(jd_json, ["benefits_and_salary"], [None])
        
        return {
                  "title": (cv_title, jd_title), 
                  "summary": (cv_summary, jd_summary), 
                  "qualification": (cv_qua, jd_qua), 
                  "education": (cv_edu, jd_edu), 
                  "experience": (cv_exper, jd_exper), 
                  "benefit": (cv_benefit, jd_benefit)
               }
    
    
    @staticmethod
    def text_embedding(text):
        response = openai.Embedding.create(model="text-embedding-ada-002", input=text)
        return response["data"][0]["embedding"]
    
    
    @staticmethod
    def cal_distance(cv_content, jd_content):
        #   Get embedding vector with text-embedding-ada-002
        cv_vec = np.asarray(ScoringService.text_embedding(cv_content))
        jd_vec = np.asarray(ScoringService.text_embedding(jd_content))
        cosine = np.dot(cv_vec, jd_vec)/(norm(cv_vec)*norm(jd_vec))
        return cosine
    
    @staticmethod
    def get_score(data_pair):
        jd_file = data_pair[0]
        cv_file = data_pair[1]
        pairs = ScoringService.gen_pair(cv_file=cv_file, jd_file=jd_file)
        results = {}
        for name, pair in pairs.items():
            dist = ScoringService.cal_distance(pair[0], pair[1])
            results[name] = dist    
            results['jd_filename'] = str(os.path.splitext(jd_file)[0])
            results['cv_filename'] = str(os.path.splitext(cv_file)[0])
        print(" >> Get scoring")
        return results