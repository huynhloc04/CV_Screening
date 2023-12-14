import json
from typing import Dict, Any
from openpyxl import load_workbook



def project_process(sh, key_char, key_num, projects):
    
    add_data = {"project_name": [], "time": [], "position": [], "domain": [], "used_technologies": [], "detailed_descriptions": []}
    
    for project in projects:
        for key, val in project.items():
            if 'N/A' in val:
                val[0] = '-'
            if key == "project_name":
                add_data[key].append("\n")
            if key == "time":
                add_data[key].append("\n")
            if key == "position":
                add_data[key].append("\n")
            if key == "domain":
                add_data[key].append("\n")
            if key == "used_technologies":
                add_data[key].append("\n")
            if key == "detailed_descriptions":
                add_data[key].append("\n")
            add_data[key].extend(val)
    
    for key in add_data.keys():
        curr_data = '\n '.join(add_data[key])[2:]
        sh[key_char+key_num] = curr_data
        key_char = chr(ord(key_char) + 1)
        
        
def exper_process(sh, key_char, key_num, projects):
    
    add_data = {"company_name": [], "time": [], "position": [], "domain": [], "used_technologies": [], "detailed_descriptions": []}
    
    for project in projects:
        for key, val in project.items():
            if 'N/A' in val:
                val[0] = '-'
            if key == "company_name":
                add_data[key].append("\n")
            if key == "time":
                add_data[key].append("\n")
            if key == "position":
                add_data[key].append("\n")
            if key == "domain":
                add_data[key].append("\n")
            if key == "used_technologies":
                add_data[key].append("\n")
            if key == "detailed_descriptions":
                add_data[key].append("\n")
            add_data[key].extend(val)
    
    for key in add_data.keys():
        curr_data = '\n '.join(add_data[key])[2:]
        sh[key_char+key_num] = curr_data
        key_char = chr(ord(key_char) + 1)
        
        
def person_process(sh, key_char, key_num, value):    
    for key, val in value.items():
        if 'N/A' in val:
            val[0] = '-'
        if key == "name":
            sh[key_char+key_num] = val[0]
        if key == "earliest_university_year":
            sh[key_char+key_num] = val[0]
        if key == "birthday":
            sh[key_char+key_num] = val[0]
        if key == "gender":
            sh[key_char+key_num] = val[0]
        if key == "nationality":
            sh[key_char+key_num] = val[0]
        if key == "desired_position":
            sh[key_char+key_num] = val[0]
        if key == "desired_salary":
            sh[key_char+key_num] = val[0]
        if key == "desired_work_location":
            sh[key_char+key_num] = val[0]
        key_char = chr(ord(key_char) + 1)
        
        
def contact_process(sh, key_char, key_num, value):  
    key_char_st = key_char[:-1]
    key_char_nd = key_char[-1]
    for key, val in value.items():
        if 'N/A' in val:
            val[0] = '-'
        if key == "phone":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "email":
            key_char = "AA"
            key_char_st = key_char[:-1]
            key_char_nd = key_char[-1]
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "address":
            for sub_key, sub_val in val.items():
                if 'N/A' in sub_val:
                    sub_val[0] = '-'
                if sub_key == "street":
                    sh[key_char_st+key_char_nd+key_num] = sub_val[0]
                if sub_key == "ward":
                    sh[key_char_st+key_char_nd+key_num] = sub_val[0]
                if sub_key == "district":
                    sh[key_char_st+key_char_nd+key_num] = sub_val[0]
                if sub_key == "province/city":
                    sh[key_char_st+key_char_nd+key_num] = sub_val[0]
                key_char_nd = chr(ord(key_char_nd) + 1)   
        if key == "urls":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        key_char_nd = chr(ord(key_char_nd) + 1)
        
        
def edu_process(sh, key_char, key_num, institutes):
    
    add_data = {"institution_name": [], "time": [], "degree": [], "major": [], "gpa": []}
    
    for institute in institutes:
        for key, val in institute.items():            
            if 'N/A' in val:
                val[0] = '-'
            if key == "institution_name":
                add_data[key].append("\n")
            if key == "time":
                add_data[key].append("\n")
            if key == "degree":
                add_data[key].append("\n")
            if key == "major":
                add_data[key].append("\n")
            if key == "gpa":
                add_data[key].append("\n")
            add_data[key].extend(val)
    
    key_char_st = key_char[:-1]
    key_char_nd = key_char[-1]
    for key in add_data.keys():
        curr_data = '\n '.join(add_data[key])[2:]
        sh[key_char_st+key_char_nd+key_num] = curr_data
        key_char_nd = chr(ord(key_char_nd) + 1)
        
        
def skill_process(sh, key_char, key_num, value):
    key_char_st = key_char[:-1]
    key_char_nd = key_char[-1]
    
    for key, val in value.items():
        if 'N/A' in val:
            val[0] = '-'
        if key == "spoken_language":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "programming_language":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "soft_skill":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "hard_skill":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        key_char_nd = chr(ord(key_char_nd) + 1)
        
        
def cert_process(sh, key_char, key_num, certs):
    
    add_data = {"language_certificates": [], "other_certificates": []}
    
    for key, val in certs.items():
        if 'N/A' in val:
            val[0] = '-'
        if key == "language_certificates":
            add_data['language_certificates'].append("\n")
            add_data['language_certificates'].extend(val)
        if key == "other_certificates":
            add_data['other_certificates'].append("\n")
            add_data['other_certificates'].extend(val)
    
    key_char_st = key_char[:-1]
    key_char_nd = key_char[-1]
    for key in add_data.keys():
        curr_data = '\n '.join(add_data[key])[2:]
        sh[key_char_st+key_char_nd+key_num] = curr_data
        key_char_nd = chr(ord(key_char_nd) + 1)
        

def refer_process(sh, key_char, key_num, refers):    
    add_data = {"name": [], "phone": [], "email": [], "company": []}    
    for refer in refers:
        for key, val in refer.items():
            if 'N/A' in val:
                val[0] = '-'
            if key == "name":
                add_data[key].append("\n")
            if key == "phone":
                add_data[key].append("\n")
            if key == "email":
                add_data[key].append("\n")
            if key == "company":
                add_data[key].append("\n")
            add_data[key].extend(val)
    
    key_char_st = key_char[:-1]
    key_char_nd = key_char[-1]
    for key in add_data.keys():
        curr_data = '\n '.join(add_data[key])[2:]
        sh[key_char_st+key_char_nd+key_num] = curr_data
        key_char_nd = chr(ord(key_char_nd) + 1)
        
        
def pub_process(sh, key_char, key_num, publics):    
    add_data = {"title": [], "author_name": [], "year": []}    
    for public in publics:
        for key, val in public.items():
            if 'N/A' in val:
                val[0] = '-'
            if key == "title":
                add_data[key].append("\n")
            if key == "author_name":
                add_data[key].append("\n")
            if key == "year":
                add_data[key].append("\n")
            add_data[key].extend(val)
    
    key_char_st = key_char[:-1]
    key_char_nd = key_char[-1]
    for key in add_data.keys():
        curr_data = '\n '.join(add_data[key])[2:]
        sh[key_char_st+key_char_nd+key_num] = curr_data
        key_char_nd = chr(ord(key_char_nd) + 1)
        
        
def iq_process(sh, key_char, key_num, value):
    key_char_st = key_char[:-1]
    key_char_nd = key_char[-1]
    
    for key, val in value.items():
        if 'N/A' in val:
            val[0] = '-'
        if key == "iq_score":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "explanation":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        key_char_nd = chr(ord(key_char_nd) + 1)
        
        
def eq_process(sh, key_char, key_num, value):
    key_char_st = key_char[:-1]
    key_char_nd = key_char[-1]
    
    for key, val in value.items():
        if 'N/A' in val:
            val[0] = '-'
        if key == "self_awareness":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "self_regulation":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "motivation":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "empathy":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "social_skills":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        if key == "explanation":
            sh[key_char_st+key_char_nd+key_num] = val[0]
        key_char_nd = chr(ord(key_char_nd) + 1)
        

def parse(sh, filename: str, data: Dict, idx: int):        
    data_dict = {}
    vals = ['B', 'H', 'N', 'O', 'P', 'Q', 'R', 'Z', 'AG', 'AL', 'AP', 'AR', 'AS', 'AW', 'AZ', 'BA', 'BB', 'BC', 'BE', 'BK']

    # data_dict["cv_name"] = 'A'
    for i, key in enumerate(data.keys()):
        data_dict[key] = vals[i]
    #   Write to xlsx
    sh[f"A{idx}"] = filename
    for key, val in data.items():
        key_char = data_dict[key]
        key_num = str(idx)
        if key == 'project':
            project_process(sh, key_char, key_num, val)
        if key == 'experience':
            exper_process(sh, key_char, key_num, val)
        if key == 'strength':
            if 'N/A' in val:
                val[0] = '-'
            sh[key_char+key_num] = val[0]
        if key == 'weakness':
            if 'N/A' in val:
                val[0] = '-'
            sh[key_char+key_num] = val[0]
        if key == 'numerology':
            if 'N/A' in val:
                val[0] = '-'
            sh[key_char+key_num] = val[0]
        if key == 'personal_information':
            person_process(sh, key_char, key_num, val)
        if key == 'contact_information':
            contact_process(sh, key_char, key_num, val)
        if key == 'education':
            edu_process(sh, key_char, key_num, val)
        if key == 'skills':
            skill_process(sh, key_char, key_num, val)        
        if key == 'certificates':
            cert_process(sh, key_char, key_num, val)     
        if key == 'achievements_and_honors':
            if 'N/A' in val:
                val[0] = '-'
            sh[key_char+key_num] = val[0]    
        if key == 'references':
            refer_process(sh, key_char, key_num, val) 
        if key == 'publications':
            pub_process(sh, key_char, key_num, val)   
        if key == 'objectives':
            if 'N/A' in val:
                val[0] = '-'
            sh[key_char+key_num] = val[0]
        if key == 'social_activities':
            if 'N/A' in val:
                val[0] = '-'
            sh[key_char+key_num] = val[0]
        if key == 'hobbies_and_interests':
            if 'N/A' in val:
                val[0] = '-'
            sh[key_char+key_num] = val[0]   
        if key == 'iq':
            iq_process(sh, key_char, key_num, val)
        if key == 'eq':
            eq_process(sh, key_char, key_num, val)
        if key == 'industry':
            if 'N/A' in val:
                val[0] = '-'
            sh[key_char+key_num] = val[0]  
        if key == 'summary':
            if 'N/A' in val:
                val[0] = '-'
            sh[key_char+key_num] = val[0]  