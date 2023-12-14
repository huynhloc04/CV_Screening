import os
import json
import pandas as pd
import time
from schema import cv_status
import concurrent.futures
from database.db_config import db
import app.parse_xlsx as par_xl
from typing import List
from openpyxl import load_workbook
from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse
from fastapi import Depends, HTTPException, status, Request, UploadFile, File, Form
from service.db_service.db_service import DatabaseService
from service.api_service.extraction_service import CvExtraction, JdExtraction
from service.api_service.openai_service import OpenAIService
from service.api_service.scoring_service import ScoringService
from config import CVPDF_PATH, CV_EXTRACTION_PATH, JD_EXTRACTION_PATH, JDTXT_PATH, JDSCORE_PATH, TMP_PATH, DUPLICATED_PATH
from service.api_service.api_service import ApiService


router = APIRouter(prefix="/api", tags=['CVPROCESS'])


@router.post('/cv_uploadpdf')
async def storing_cv(request: Request, cv_files: List[UploadFile] = File(...), session=Depends(db.get_session)):
    # only accept post method
    if request.method == "POST":
        #--------cv upload---------
        for file in cv_files:
            file_cleaned = await DatabaseService.clean_filename(file.filename)
            if not await DatabaseService.check_duplicate(file_cleaned, CVPDF_PATH):
                await DatabaseService.save_cvpdf(cv_file=file)
                # await DatabaseService.store_postgrescv(session=session, cv_file=file)

        return JSONResponse(content={'result': True}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


@router.post('/upload_jd')
async def storing_jd(request: Request, jd_files: List[UploadFile] = File(...), session=Depends(db.get_session)):
    # only accept post method
    if request.method == "POST":
        for file in jd_files:
            file_cleaned = await DatabaseService.clean_filename(file.filename)
            if not await DatabaseService.check_duplicate(file_cleaned, JDTXT_PATH):
                await DatabaseService.save_jdtxt(jd_file=file)
        return JSONResponse(content={"result": True}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


@router.get('/load_cvpdflist')
async def get_cvlist(request:Request):
    # only accept post method
    if request.method == "GET":
        cv_files = os.listdir(CVPDF_PATH)
        return JSONResponse(content={'result': True, 'data': cv_files}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


@router.get('/load_jdlist')
async def get_cvlist(request:Request):
     # only accept post method
    if request.method == "GET":
        cv_files = os.listdir(JDTXT_PATH)
        return JSONResponse(content={'result': True, 'data': cv_files}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


async def extract_cv_info(session):
    prompts = []
    cv_names = []        
        # get all cv need to extract 
    for cv_file in os.listdir(CVPDF_PATH):
        if not await DatabaseService.check_duplicate(cv_file, CV_EXTRACTION_PATH): # only extract cv that is not extracted
                # extract text content of the CV
            prompt_template = CvExtraction.get_cvtext(cv_file=cv_file)
                # add query to the cv text 
            full_query = await CvExtraction.add_query(prompt_template) 
            prompts.append(full_query)
            cv_names.append(cv_file[:-4])

    start = time.time()   

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # calling openai
        results = list(executor.map(OpenAIService.gpt_api, prompts, cv_names))

    for result in results:
        # save extracted cv json to local folder
        await DatabaseService.store_extractjson(extracted_json=result[1], cv_file=result[0].strip())
        # await DatabaseService.update_cv(session=session, data=result, status=cv_status['READY']) # update cv status with user_email, foldername and cv_name

    elaps_time = time.time() - start
    print(f" >> Extract in {elaps_time}")

@router.get('/cv_extract')
async def extract_cv(request: Request, session=Depends(db.get_session)):
    # only accept post method
    if request.method == "GET":
        if not os.path.exists(CVPDF_PATH):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cv pdf folder not existed!")
        if not os.path.exists(CV_EXTRACTION_PATH):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cv extraction folder not existed!")
        if len(os.listdir(CVPDF_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert at least 1 CV PDF")

        await extract_cv_info(session)

        return JSONResponse(content={'result': True}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


def jdpdf2text() -> None:
    for jd_file in os.listdir(JDTXT_PATH):
        if jd_file.endswith('.pdf'):
            text = JdExtraction.text_extract(os.path.join(JDTXT_PATH, jd_file))
            with open(os.path.join(JDTXT_PATH, jd_file[:-4]+'.txt'), 'w') as file:
                file.write(text)
            #   Remove JD pdf file
            os.remove(os.path.join(JDTXT_PATH, jd_file))

async def extract_jd_info(session):
    prompts = []
    jd_names = []        
    # Get all cv need to extract 
    jdpdf2text()               
    for jd_file in os.listdir(JDTXT_PATH):
        if not await DatabaseService.check_duplicate(jd_file, JD_EXTRACTION_PATH): # only extract cv that is not extracted
                # extract text content of the CV
            prompt_template = JdExtraction.get_jdtext(jd_file=jd_file) 
                # add query to the cv text 
            full_query = await JdExtraction.add_query(prompt_template) 
            prompts.append(full_query)
            jd_names.append(jd_file[:-4])

    start = time.time()   

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # calling openai
        results = list(executor.map(OpenAIService.gpt_api, prompts, jd_names))

    for result in results:
        # save extracted jd json to local folder
        await DatabaseService.jd_store_extraction(extracted_json=result[1], jd_file=result[0].strip())
        # await DatabaseService.update_cvstatus(session=session, cv_file=cv_file, status=cv_status['READY'])

    elaps_time = time.time() - start
    print(f" >> Extract in {elaps_time}")
    
@router.get('/jd_extract')
async def extract_jd(request: Request, session=Depends(db.get_session)):
    # only accept post method
    if request.method == "GET":
        if not os.path.exists(JDTXT_PATH):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="JD folder not existed!")
        if not os.path.exists(JD_EXTRACTION_PATH):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="JD extraction folder not existed!")
        if len(os.listdir(JDTXT_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert at least 1 JD txt")

        #   Convert pdf file to text file (if any)
        await extract_jd_info(session)

        return JSONResponse(content={'result': True}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


@router.get('/cv_score')
async def score_cv(request: Request, session=Depends(db.get_session)):
    # only accept post method
    if request.method == "GET":

        #--------scoring-----------
        if len(os.listdir(CVPDF_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert at least 1 CV PDF")
        if len(os.listdir(JDTXT_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert at least 1 JD TXT/PDF.")
        
        #   Let's extract CVs and JDs first
        await extract_cv_info(session)
        await extract_jd_info(session)
        
        data = []
        for jd_json in os.listdir(JD_EXTRACTION_PATH):
            #   Create each score directory corresponding JD, one JD folder contain multtiple scored CVs 
            if not os.path.exists(os.path.join(JDSCORE_PATH, jd_json[:-5])):
                os.mkdir(os.path.join(JDSCORE_PATH, jd_json[:-5]))
            
            if not await DatabaseService.check_duplicate(file=jd_json, path=JDTXT_PATH): 
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" Parquet not existed")
            for cv_json in os.listdir(CV_EXTRACTION_PATH):
                if not await DatabaseService.check_duplicatescore(cv_file=cv_json, jd_file=jd_json): # Request score for not scored cv
                    #  Request openai for score of jd and cv
                    data.append([jd_json, cv_json])
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(ScoringService.get_score, data))
            
        for result in results:
            #  Add score to socre file for each jd
            jd_filename = result['jd_filename']
            cv_filename = result['cv_filename']
            #   Write JSON result to local
            with open(os.path.join(JDSCORE_PATH, jd_filename, f"{cv_filename}.json"), "w") as outfile:
                json.dump(result, outfile)
            # await DatabaseService.add_cvscore(jd_filename, cv_filename, result)

        return JSONResponse(content={'result': True}, status_code=status.HTTP_200_OK)    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")

@router.post('/load_score')
async def load_score(request: Request, jd_file: str = Form(...)):
    # only accept post method
    if request.method == "POST":
        if not await DatabaseService.check_duplicate(jd_file, JDTXT_PATH):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="JD file not exist in database yet, please upload it")
        if not await DatabaseService.check_duplicate(jd_file, JDSCORE_PATH):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please request score API first")
        if len(os.listdir(CVPDF_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert at least 1 CV PDF")
        jd_file_cleaned = await DatabaseService.clean_filename(jd_file)
        filename = os.path.splitext(jd_file_cleaned)[0]
        
        json_dict = {}
        for file in os.listdir(os.path.join(JDSCORE_PATH, filename)):    
            if file.endswith('.json'):
                with open(os.path.join(JDSCORE_PATH, filename, file), 'r') as file:
                    data = json.load(file)
                json_dict[data["cv_filename"]] = data
            
        return JSONResponse(content={"result": True, "data": json_dict}, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


@router.post("/load_cv_extract")
async def load_cv_extracted(request: Request, cv_file: str = Form(...)):
    global CV_EXTRACTION_PATH
    # only accept post method
    if request.method == "POST":
        if len(os.listdir(CVPDF_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert at least 1 CV PDF")
        if len(os.listdir(CV_EXTRACTION_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please request extraction API first")
        
        cv_file_cleaned = await DatabaseService.clean_filename(cv_file)
        
        cv_filename = os.path.splitext(cv_file_cleaned)[0]
        if not await DatabaseService.check_duplicate(cv_file_cleaned, CV_EXTRACTION_PATH):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CV file not extracted yet or cv not upload yet")
        extract_json = cv_filename + ".json"
        CV_EXTRACTION_PATH = os.path.join(CV_EXTRACTION_PATH, extract_json)
        with open(CV_EXTRACTION_PATH, 'r') as f:
            data = json.load(f)
        data["cv_filename"] = [str(cv_filename)]
        return JSONResponse(content={"result": True, "data": data}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


@router.post("/load_jd_extract")
async def load_jd_extracted(request: Request, jd_file: str = Form(...)):
    global JD_EXTRACTION_PATH
    # only accept post method
    if request.method == "POST":
        if len(os.listdir(JDTXT_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert at least 1 JD TXT")
        if len(os.listdir(JD_EXTRACTION_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please request JD extraction API first")
        
        jd_file_cleaned = await DatabaseService.clean_filename(jd_file)
        
        jd_filename = os.path.splitext(jd_file_cleaned)[0]
        if not await DatabaseService.check_duplicate(jd_file_cleaned, JD_EXTRACTION_PATH):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="JD file not extracted yet or JD not upload yet")
        extract_json = jd_filename + ".json"
        JD_EXTRACTION_PATH = os.path.join(JD_EXTRACTION_PATH, extract_json)
        with open(JD_EXTRACTION_PATH, 'r') as f:
            data = json.load(f)
        data["jd_filename"] = [str(jd_filename)]
        return JSONResponse(content={"result": True, "data": data}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


@router.get("/check_duplicate")
async def check_dup_cv(request: Request, session=Depends(db.get_session)):
    # global dup_checked
    if request.method == "GET":
        if len(os.listdir(CVPDF_PATH)) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert at least 2 CVs PDF")
        
        print(" >> Start checking duplicate.")
        #   Extract CVs if any CV hasnt extracted yet
        await extract_cv_info(session=session)
        #   Check duplicate after uploading 
        extracted_names = [file.split('.')[0] for file in os.listdir(CV_EXTRACTION_PATH)]               
        checked_names = [file.split('.')[0] for file in os.listdir(DUPLICATED_PATH)]    
        diffs = list(set(extracted_names) - set(checked_names))    #  CVs that have not been extracted yet 
        
        #   Start checking duplicate CVs
        await DatabaseService.check_dup(diffs)
   
        #   Fill missing rows to xlsx files
        DatabaseService.fill_info() 
        
        print(" >> Check duplicate CVs complete!!!")
        return JSONResponse(content={'result': True}, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


@router.get("/load_extractshort")
async def load_extractshort(request: Request):
    if request.method == "GET":
        if len(os.listdir(CVPDF_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert at least 1 CV PDF")
        if len(os.listdir(CV_EXTRACTION_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please request extraction API first")

        list_data = []        
        for file in os.listdir(CV_EXTRACTION_PATH):
            if file.endswith(".json"):
                cv_filename = os.path.splitext(file)[0]
                file_path = os.path.join(CV_EXTRACTION_PATH, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                short_data = {}
                short_data["cv_filename"] = [str(cv_filename)]
                short_data['name'] = data['personal_information']['description']['name']
                short_data['birthday'] = data['personal_information']['description']['birthday']
                short_data['desired_position'] = data['personal_information']['description']['desired_position']
                short_data['gender'] = data['personal_information']['description']['gender']
                short_data['strength'] = data['strength']['description']
                short_data['weakness'] = data['weakness']['description']
                short_data['numerology'] = data['numerology']['description']
                short_data['iq'] = [f"{str(key).capitalize()}: {', '.join(val)}" for key, val in data['iq']['description'].items()]
                short_data['eq'] = [f"{str(key).capitalize()}: {', '.join(val)}" for key, val in data['eq']['description'].items()]
                short_data['education'] = [ApiService.filter_sections(data=part, choose_sections=['institution_name', 'time', 'degree', 'gpa']) for part in data['education']['description']]
                short_data['work_experience'] = [ApiService.filter_sections(data=part, choose_sections=['company_name', 'time', 'position']) for part in data['experience']['description']]
                short_data['language'] = data['skills']['description']['spoken_language']
                short_data['certificates'] = [f"{str(key).capitalize()}: {', '.join(data['certificates']['description'][key])}" for key in data['certificates']['description'].keys()]
                short_data['objectives'] = data['objectives']['description']
                
                list_data.append(short_data)

        return JSONResponse(content={"result": True, "data": list_data}, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")


@router.get("/extraction_excel")
async def get_excelextraction(request: Request):
    """ Load extraction of all cv"""
    if request.method == "GET":
        if len(os.listdir(CVPDF_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert at least 1 CV PDF")
        if len(os.listdir(CV_EXTRACTION_PATH)) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please request extraction API first")
        
        #   Read file.xlsx
        wb = load_workbook("resources/template/cv_extract.xlsx")
        sh = wb.active
        
        idx = 4
        for file in os.listdir(CV_EXTRACTION_PATH):
            if file.endswith(".json"):
                file_path = os.path.join(CV_EXTRACTION_PATH, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                par_xl.parse(sh, filename=file[:-5]+".pdf", data=data, idx=idx)  
                idx += 1  
        #   Save file.xlsx output
        wb.save(os.path.join(TMP_PATH, "extraction.xlsx"))
    
        return FileResponse(os.path.join(TMP_PATH, "extraction.xlsx"), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="extraction.xlsx")

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fetching method!")

            
@router.get("/delete_all")
async def delete_all(request: Request):
    try: 
        data_dir = [CVPDF_PATH, CV_EXTRACTION_PATH, JD_EXTRACTION_PATH, JDTXT_PATH, JDSCORE_PATH, TMP_PATH, DUPLICATED_PATH]
        for directory in data_dir:
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    os.remove(file_path)
                    print(f" >> File {name} deleted")
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    os.rmdir(dir_path)
                    print(f" >> Folder {name} deleted")
        return JSONResponse(content={'result': True}, status_code=status.HTTP_200_OK)
    
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete all!")
