from database.db_handlers.base_handler import BaseHandler
from database.models import *
from pprint import pprint
import os
from config import CVPDF_PATH
# from database.models import CvCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import update as sql_update, delete as sql_delete
from sqlalchemy import and_
import json
from database.db_config import commit_rollback
from fastapi import HTTPException, status


project = {'project_name': 'N/A', 'time': 'N/A', 'position': 'N/A', 'domain': 'N/A', 'used_technologies': 'N/A', 'detailed_descriptions': 'N/A'}
exper = {'company_name': 'N/A', 'time': 'N/A', 'position': 'N/A', 'domain': 'N/A', 'used_technologies': 'N/A', 'detailed_descriptions': 'N/A'}
personal_info = {'name': 'N/A', 'earliest_university_year': 'N/A', 'earliest_university_name': 'N/A', 'birthday': 'N/A', 'gender': 'N/A', 'nationality': 'N/A', 'desired_position': 'N/A', 'desired_salary': 'N/A', 'desired_work_location': 'N/A'}
address = {'street': 'N/A', 'ward': 'N/A', 'district': 'N/A', 'province': 'N/A'}
contact_info = {'phone': 'N/A', 'email': 'N/A', 'urls': 'N/A'}
education = {'institution_name': 'N/A', 'time': 'N/A', 'degree': 'N/A', 'major': 'N/A', 'gpa': 'N/A'}
skill = ['spoken_language', 'programming_language', 'soft_skill', 'hard_skill']
cert = ['language_certificates', 'other_certificates']
refer = ['name', 'company', 'phone', 'email']
pub = ['title', 'author_name', 'year']


class CvHandler(BaseHandler):
    
    async def update_by_cvname(session: AsyncSession, data_res, **kwargs):
        filename = data_res[0].strip()
        json_data = data_res[1]
        
        #   Add Project
        project_data = json_data["project"]["description"]
        project_name = [] if project_data else ['N/A']
        time = [] if project_data else ['N/A']
        position = [] if project_data else ['N/A']
        domain = [] if project_data else ['N/A']
        used_technologies = [] if project_data else ['N/A']
        detailed_descriptions = [] if project_data else ['N/A']
        for data in project_data:
            project_name.extend(data['project_name'])
            time.extend(data['time'])
            position.extend(data['position'])
            domain.extend(data['domain'])
            used_technologies.extend(data['used_technologies'])
            detailed_descriptions.extend(data['detailed_descriptions'])
            
        project_info = Project(project_name=project_name, 
                               time=time, 
                               position=position, 
                               domain=domain, 
                               used_technologies=used_technologies, 
                               detailed_descriptions=detailed_descriptions)
        
        
        #   Add Experience
        exper_data = json_data["experience"]["description"]        
        company_name = [] if exper_data else ['N/A']
        time = [] if exper_data else ['N/A']
        position = [] if exper_data else ['N/A']
        domain = [] if exper_data else ['N/A']
        used_technologies = [] if exper_data else ['N/A']
        detailed_descriptions = [] if exper_data else ['N/A']
        for data in exper_data:
            company_name.extend(data['company_name'])
            time.extend(data['time'])
            position.extend(data['position'])
            domain.extend(data['domain'])
            used_technologies.extend(data['used_technologies'])
            detailed_descriptions.extend(data['detailed_descriptions'])
            
        exper_info = Experience(company_name=company_name, 
                                time=time, 
                                position=position, 
                                domain=domain, 
                                used_technologies=used_technologies, 
                                detailed_descriptions=detailed_descriptions)
        
        
        #   Add Personal Information
        person_data = json_data["personal_information"]["description"]
            
        person_info = PersonalInformation(name=person_data['name'], 
                                          earliest_university_year=person_data['earliest_university_year'], 
                                          earliest_university_name=person_data['earliest_university_name'], 
                                          birthday=person_data['birthday'], 
                                          gender=person_data['gender'], 
                                          nationality=person_data['nationality'], 
                                          desired_position=person_data['desired_position'], 
                                          desired_salary=person_data['desired_salary'], 
                                          desired_work_location=person_data['desired_work_location'])
        
        
        #   Add Contact Information
        contact_data = json_data["contact_information"]["description"]
        address_info = Address(street=contact_data['address']['street'], 
                               ward=contact_data['address']['ward'], 
                               district=contact_data['address']['district'], 
                               province=contact_data['address']['province/city'])  
        contact_info = ContactInformation(phone=contact_data['phone'], 
                                          email=contact_data['email'], 
                                          address_id=address_info.id, 
                                          urls=contact_data['urls'])
        
        #   Add Education
        edu_data = json_data["education"]["description"]
        institution_name = []
        time = [] if edu_data else ['N/A']
        degree = [] if edu_data else ['N/A']
        major = [] if edu_data else ['N/A']
        gpa = [] if edu_data else ['N/A']
        for data in edu_data:
            institution_name.extend(data['institution_name'])
            time.extend(data['time'])
            degree.extend(data['degree'])
            major.extend(data['major'])
            gpa.extend(data['gpa'])
        edu_info = Education(institution_name=institution_name, 
                             time=time, 
                             degree=degree, 
                             major=major, 
                             gpa=gpa)
        
        #   Add Skill
        skill_data = json_data["skills"]["description"]
        skill_info = Skill(spoken_language=skill_data['spoken_language'], 
                           programming_language=skill_data['programming_language'], 
                           soft_skill=skill_data['soft_skill'], 
                           hard_skill=skill_data['hard_skill'])
        
        #   Add Certificate
        cert_data = json_data["certificates"]["description"]
        cert_info = Certificate(language_certificates=cert_data['language_certificates'], 
                                other_certificates=cert_data['other_certificates'])
        
        #   Add Reference
        refer_data = json_data["references"]["description"]
        name = [] if refer_data else ['N/A']
        company = [] if refer_data else ['N/A']
        phone = [] if refer_data else ['N/A']
        email = [] if refer_data else ['N/A']
        for data in refer_data:
            name.extend(data['name'])
            company.extend(data['company'])
            phone.extend(data['phone'])
            email.extend(data['email'])
        refer_info = Reference(name=name, 
                               company=company, 
                               phone=phone, 
                               email=email)
        
        #   Add Publication
        pub_data = json_data["publications"]["description"]
        title = [] if pub_data else ['N/A']
        author_name = [] if pub_data else ['N/A']
        year = [] if pub_data else ['N/A']
        for data in pub_data:
            title.extend(data['title'])
            author_name.extend(data['author_name'])
            year.extend(data['year'])
        pub_info = Publication(title=title, 
                               author_name=author_name, 
                               year=year)
        
        #   Add IQ
        iq_data = json_data["iq"]["description"]
        iq_info = IQ(iq_level=iq_data["iq_level"],
                     explanation=iq_data["explanation"])
        
        #   Add EQ
        eq_data = json_data["eq"]["description"]
        eq_info = EQ(self_awareness_level=eq_data["self_awareness_level"],
                     self_regulation_level=eq_data["self_regulation_level"],
                     motivation_level=eq_data["motivation_level"],
                     empathy_level=eq_data["empathy_level"],
                     social_skills_level=eq_data["social_skills_level"],
                     explanation=eq_data["explanation"])
        
        #   Tie all together and add to whole database
        cv = CV(cv_name=filename,
                project_id=project_info.id,
                exper_id=exper_info.id,
                strength=json_data["strength"]["description"],
                weakness=json_data["weakness"]["description"],
                numerology=json_data["numerology"]["description"],
                personal_info_id=person_info.id,
                contact_info_id=contact_info.id,
                education_id=edu_info.id,
                skill_id=skill_info.id,
                cert_id=cert_info.id,
                refer_id=refer_info.id,
                public_id=pub_info.id,
                achievements_and_honors=json_data["achievements_and_honors"]["description"],
                objective=json_data["objectives"]["description"],
                social_activities=json_data["social_activities"]["description"],
                iq_id=iq_info.id,
                eq_id=eq_info.id,
                industry=json_data["industry"]["description"],
                summary=json_data["summary"]["description"])
        
        #   Add and save changes
        tables = [project_info, exper_info, person_info, address_info, contact_info, edu_info, skill_info, cert_info, refer_info, pub_info, iq_info, eq_info, cv]
        for table in tables:
            print("=======================================")
            print(table)
            session.add(table)
            commit_rollback(session)
        return True
