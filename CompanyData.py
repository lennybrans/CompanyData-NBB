from dotenv import load_dotenv
import uuid
import re
import requests
import json
import pandas as pd
import os
import numpy as np

import dictionaries as dct

load_dotenv()
api_key = os.getenv('NBB_CBSO_sub_key')


class CompanyData:
    def __init__(self, company_number: str):
        """
        Initialize with a list of company numbers.
        """
        self.company_number = self._clean_input(company_number)

# Refactoring OK: Raises ValueError i.c.o. wrong input length-wise
    def _clean_input(self, user_input: str) -> str:
        '''
        Function removes non-numeric characters. 
        Returns only-numeric string or raises a ValueError. 
        Important: it checks the numeric correct input, not whether the 
        company ID is in the databank.
        '''
        user_input = user_input.strip()
        cleaned_input = re.sub(r"\D", '', user_input)
        if len(cleaned_input) in [10, 11]:
            return cleaned_input
        else:
            raise ValueError(
                "Wrong input - Length mismatch")
        
# Refactoring OK        
    def _reference_url_creation(self):
        """
        Function generates URL to receive the reference list from NBB.
        Default database is authentic. Other options are 'extracts' and 
        'improved' but the function is not yet adjusted to handle this.
        """
        environment = "https://ws.cbso.nbb.be/"
        database = "authentic/"
        action = "legalEntity/"
        company_id = self.company_number + "/"
        type_action = "references"

        url = environment + database + action + company_id + type_action
        return url
    
# Refactoring OK: Prints HTTP-error or returns it to the tool
    def _api_call(self, url: str, accept_form: str) -> bytes:
        """
        Function makes API call for references list. 
        Return bytes object or HTTP Error Code.
        """
        uuid_code = str(uuid.uuid4())
        hdr = {
            'X-Request-Id': uuid_code,
            'NBB-CBSO-Subscription-Key': api_key,
            'Accept': accept_form,
            'User-Agent': 'PostmanRuntime/7.37.3'
        }

        try:
            response = requests.get(url, headers=hdr)
            response.raise_for_status()
            print(response.status_code)
            api_answer = response.content
            return api_answer
        except requests.exceptions.HTTPError as http_err:
            return http_err
        except requests.exceptions.RequestException as req_err:
            print(f"This is a Request Error: {req_err}")
            return req_err
        except Exception as err:
            print(f"This is a regular Error: {err}")
            return err
        
# Needs an update: 'Geconsolideerde Jaarrekening' is not yet available via API
# but might be in the future. Unfortunately, the 'ModelType' is not a unique 
# indicator across companies/industries to select the 'Jaarrekening'.
    def _handle_df_of_references(self, df_of_references):
        """
        Function filters the DataFrame of References.
        - Selects only 'Jaarrekening' and not 'Geconsolideerde Jaarrekening'. 
        - Compares bookyears and selects the latest submission, in case of 
          a correction.
        """
        df_of_references.sort_values(
            ['ExerciseDates.endDate', 'DepositDate'],
            ignore_index=True, 
            inplace=True)

        df_of_references.dropna(
            subset=['AccountingDataURL'],
            axis=0,
            inplace=True)

        df_of_references.drop_duplicates(
            subset=['ExerciseDates.startDate', 'ExerciseDates.endDate'],
            keep='last',
            ignore_index=True,
            inplace=True)

        return df_of_references
    
# Refactoring OK 
    def fetch_references(self, 
                         year_span=1, 
                         accept_reference="application/json"):
        """
        Function makes an API call for references. 
        Returns a DataFrame with the references from the NBB for one specific
        company ID (KBO-nummer). 
        Default year span is one year (last submission).
        """
        api_answer = self._api_call(
            self._reference_url_creation(), 
            accept_reference
            )
        
        # In web tool use return the error, otherwise raise the error
        if isinstance(api_answer, Exception):
            no_submission = ValueError(
                "No submission found in NBB database. " +
                "Please, double check company ID.")
            print(api_answer)
            return no_submission
        
        df_of_references = pd.json_normalize(json.loads(api_answer))
        df_of_references = self._handle_df_of_references(df_of_references)
        df_of_references = df_of_references.tail(year_span)
        return df_of_references
    
# Refactoring OK    
    def fetch_data(self, 
                   reference_variable, 
                   accept_submission='application/x.jsonxbrl') -> dict:
        """
        Function makes an API call for data. Add variable containing the 
        reference list or vector it.
        Returns the data in a dictionary. The amount of keys in the dictionary 
        is equal to the amount of years requested in the references.
        """
        data_dictionary = {}
        reference_URLs = reference_variable['AccountingDataURL']
        for data_url in reference_URLs:
            try:
                data = self._api_call(
                    url=data_url, 
                    accept_form=accept_submission
                    )
                data_dict = json.loads(data)
                reference_number = data_dict['ReferenceNumber']
                data_dictionary[reference_number]=data_dict
            except Exception as e:
                e = 'Not a JSONXBRL'
                print(e)
        return data_dictionary

## Functions to manipulate data
# Under construction
def _extract_fin_data(company_data_dict: dict) -> dict:
    """
    Function returns dictionary with reference number as key and a DataFrame 
    as value.
    """
    fin_data_dict = {}
    for key, value in company_data_dict.items():
        df = pd.json_normalize(
            value, 
            record_path='Rubrics', 
            meta='ReferenceNumber')
        fin_data_dict[key]=df
    return fin_data_dict

def fetch_fin_data(company_data, period='N'):
    """
    Function returns a DataFrame with financial data.
    """
    fin_data = pd.DataFrame()
    financial_dict = _extract_fin_data(company_data)
    
    for symbol in period:
        for key, value in financial_dict.items():
            df = value[value['Period']==symbol].set_index('Code')
            book_codes_dict = dct.bookcodes_dictionary.copy()
            for k, v in book_codes_dict.items():
                if v in df.index:
                    book_codes_dict[k] = df.loc[v, "Value"]
                else:
                    book_codes_dict[k] = np.nan
                    
            book_codes_dict['Period']=symbol
            result = pd.DataFrame([book_codes_dict], index=[key])
            fin_data = pd.concat([fin_data, result])
    fin_data = fin_data.sort_index(axis=0)
    
    return fin_data