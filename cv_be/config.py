OPENAI_MODEL = 'gpt-3.5-turbo-16k'
# OPENAI_MODEL = 'gpt-4'

CVPDF_PATH = "data/cv/cv_pdf"
JDTXT_PATH = "data/jd/jd_txt"
JDSCORE_PATH = "data/jd/jd_scoring"
TMP_PATH = "data/tmp"
CV_EXTRACTION_PATH = "data/cv/cv_extraction"
JD_EXTRACTION_PATH = "data/jd/jd_extraction"
DUPLICATED_PATH = "data/cv/duplicated"
CV_PROMPT_PATH = "resources/prompt/cv_extract_v1.6.txt"
JD_PROMPT_PATH = "resources/prompt/jd_extract_v1.7.txt"
CHROMADB = "service/db_service/chromadb"

SCORING_PROMPT = "resources/prompt/scoring.txt"

SCORING_TABLE = {"cv_filename":[],
                 "Education match":[], 
                 "Skill match": [],
                 "Experience match": [],
                 "Overall score": [],
                 "Overall evaluation": []}

        

