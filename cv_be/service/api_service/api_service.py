from datetime import datetime
from fastapi import HTTPException, status

class ApiService:
    """method for api service"""
    @staticmethod
    def calculate_age(date_str):
        try:
            # Parse the input date string into a datetime object
            birth_date = datetime.strptime(date_str, "%d/%m/%Y")

            # Get the current date
            current_date = datetime.now()

            # Calculate the age by subtracting the birth date from the current date
            age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))

            return age

        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Please use dd/mm/yyyy.") 
        
    @staticmethod
    def filter_sections(data, choose_sections: []):
        keys = set(data.keys())
        del_keys = keys - set(choose_sections)
        for key in del_keys:
            del data[key]
        data_list = []
        for key in data.keys():
            data_list.append(f"{str(key).capitalize()}: {', '.join(data[key])}")
        data_str = " || ".join(data_list)
        return data_str



 
    
                        