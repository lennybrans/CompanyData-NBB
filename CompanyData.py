import uuid
import re
import json
import os
from dotenv import load_dotenv
import pandas as pd
import requests

import dictionaries as dct

load_dotenv()
api_key = os.getenv('NBB_CBSO_sub_key')


class CompanyData:
    def __init__(self, company_number: str):
        """
        Initialize with a list of company numbers.
        """
        self.company_number = self._clean_input(company_number)

    def _clean_input(self, user_input: str) -> str:
        '''
        Returns only-numeric string or raises a ValueError.
        Removes non-numeric characters. 
        Important: it checks the numeric correct input, not whether the 
        company ID is in the databank.
        '''
        user_input = user_input.strip()
        cleaned_input = re.sub(r"\D", '', user_input)
        if len(cleaned_input) in [10, 11]:
            return cleaned_input
        else:
            raise ValueError("Wrong input - Length mismatch")
               
    def _reference_url_creation(self):
        """
        Returns an API compatible URL based on input.
        Default database is 'authentic'. Other options are 'extracts' and 
        'improved' but the function is not yet adjusted to handle this.
        """
        environment = "https://ws.cbso.nbb.be/"
        database = "authentic/"
        action = "legalEntity/"
        company_id = self.company_number + "/"
        type_action = "references"

        url = environment + database + action + company_id + type_action
        return url
    
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
            'User-Agent': 'PostmanRuntime/7.37.3',
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
# identifier across companies/industries to select the 'Jaarrekening'.
    def _handle_df_of_references(self, df_of_references):
        """
        Function filters the DataFrame of References.
        - Selects 'AccountingDataURL' colum, which only is available for 
          'Jaarrekening' and not for 'Geconsolideerde Jaarrekening'. 
        - Compares bookyears and selects the latest submission, in case 
          a correction was submitted.
        """
        df_of_references.sort_values(
            ['ExerciseDates.endDate', 'DepositDate'],
            ignore_index=True, 
            inplace=True,
            )

        df_of_references.dropna(
            subset=['AccountingDataURL'],
            axis=0,
            inplace=True,
            )

        df_of_references.drop_duplicates(
            subset=['ExerciseDates.startDate', 'ExerciseDates.endDate'],
            keep='last',
            ignore_index=True,
            inplace=True,
            )

        return df_of_references
    
    def fetch_references(self, 
                         year_span=1, 
                         accept_reference="application/json"):
        """
        Function makes an API call for references and returns a DataFrame with 
        the references from the NBB for one specific company ID (KBO-nummer). 
        Default year span is one year (last submission).
        """
        api_answer = self._api_call(
            self._reference_url_creation(), 
            accept_reference,
            )
        
        if isinstance(api_answer, Exception):
            return pd.DataFrame() # If 404 error, alternative way?
        
        df_of_references = pd.json_normalize(json.loads(api_answer))
        df_of_references = self._handle_df_of_references(df_of_references)
        df_of_references = df_of_references.tail(year_span)
        return df_of_references
        
    def fetch_data(self, 
                   reference_variable: pd.DataFrame, 
                   accept_submission='application/x.jsonxbrl') -> dict:
        """
        Function makes an API call for data. Add variable containing the 
        reference list or vector it.
        Returns the data in a dictionary. The amount of keys in the dictionary 
        is equal to the amount of years requested in the references.
        Currently, it does not accept XBRL format.
        """
        data_dictionary = {}
        if not reference_variable.empty:
            reference_URLs = reference_variable.AccountingDataURL
            dates_dict = (reference_variable.set_index('ReferenceNumber')
                        [['ExerciseDates.startDate', 'ExerciseDates.endDate']]
                        .to_dict('index'))
            
            for data_url in reference_URLs:
                try:
                    data = self._api_call(
                        url=data_url, 
                        accept_form=accept_submission
                        )
                    data_dict = json.loads(data)
                    reference_number = data_dict.get('ReferenceNumber')
                    # data_dict.update(dates_dict) ?
                    data_dict['Span'] = dates_dict[reference_number]
                    data_dictionary[reference_number] = data_dict
                except Exception as e:
                    e = 'Not a JSONXBRL'
                    print(e)
        else:
            pass # If 404 error, alternative way?
        return data_dictionary

## Functions to manipulate data
# Under construction
def _extract_fin_data(company_data_dict: dict) -> dict:
    """
    Function returns a dictionary with Reference Number as key and a DataFrame 
    as value.
    """
    if company_data_dict:
        financial_dict = {}
        
        for key, value in company_data_dict.items():
            df = pd.json_normalize(
                value, 
                record_path=['Rubrics'], 
                meta=[
                    'EnterpriseName',
                    'ReferenceNumber',
                    ['Span', 'ExerciseDates.startDate'],
                    ['Span', 'ExerciseDates.endDate']]
                )
            financial_dict[key] = df
    else:
        financial_dict = {} # If 404 error, alternative way?
    return financial_dict

def fetch_fin_data(company_data: dict, period='N') -> pd.DataFrame:
    """
    Function returns a DataFrame with financial data. The 'N' argument selects
    the data for the current year. It is also possible to select the data from
    the previous year by changing it to 'NM1'.
    """
    fin_data = pd.DataFrame()
    financial_dict = _extract_fin_data(company_data)
    
    if financial_dict:
        for symbol in period:
            for key, value in financial_dict.items():
                df = value[value['Period'] == symbol].set_index('Code')
                book_codes_dict = dct.bookcodes_dictionary.copy()
                for k, v in book_codes_dict.items():
                    if v in df.index:
                        book_codes_dict[k] = float(df.loc[v, "Value"])
                    else:
                        book_codes_dict[k] = int(0)
                
                book_codes_dict['EnterpriseName'] = df['EnterpriseName'].iloc[0]
                book_codes_dict['StartDate'] = df['Span.ExerciseDates.startDate'].iloc[0]
                book_codes_dict['EndDate'] = df['Span.ExerciseDates.endDate'].iloc[0]
                result = pd.DataFrame([book_codes_dict], index=[key])
                fin_data = pd.concat([fin_data, result])
        fin_data = fin_data.sort_index(axis=0)
    else:
        pass
    return fin_data

def days_sales_outstanding(financial_data: pd.DataFrame) -> pd.DataFrame:
    '''
    '''
    handelsvorderingen = financial_data[
        'Handelsvorderingen (40)'
        ]
    geendoss_handelseff = financial_data[
        'Door de vennootschap geëndosseerde handelseffecten in omloop (9150)'
        ]
    omzet = financial_data[
        'Omzet (70)'
        ]
    andere_bedrijfsopbr = financial_data[
        'Andere bedrijfsopbrengsten (74)'
        ]
    exploit_subs = financial_data[
        'Andere - exploitatiesubsidies en vanwege de overheid ontvangen '
        'compenserende bedragen (740)'
        ]
    btw_door_vennootschap = financial_data[
        'In rekening gebrachte belasting op de toegevoegde waarde '
        '- door vennootschap (9146)'
        ]
    
    numerator = handelsvorderingen + geendoss_handelseff
    denominator = (omzet + andere_bedrijfsopbr
                   - exploit_subs + btw_door_vennootschap)
    
    if denominator == 0:
        dso = 'Zero Division'
    else:
        dso = round(numerator/denominator * 365)

    financial_data['DSO'] = dso
    return financial_data

def days_payables_outstanding(financial_data: pd.DataFrame) -> pd.DataFrame:
    '''
    '''
    handelsschulden = financial_data[
        'Handelsschulden (44)'
        ]
    aankopen = financial_data[
        'Aankopen (600/8)'
        ]
    diensten_diverse = financial_data[
        'Diensten en diverse goederen (61)'
        ]
    btw_aan_vennootschap = financial_data[
        'In rekening gebrachte belasting op de toegevoegde waarde '
        '- aan vennootschap (9145)'
        ]
    
    numerator = handelsschulden
    denominator = aankopen + diensten_diverse + btw_aan_vennootschap
    
    if denominator == 0:
        dpo = 'Zero Division'
    else:
        dpo = round(numerator/denominator * 365)
    
    financial_data['DPO'] = dpo
    return financial_data

def inventory_cycle_finished(financial_data: pd.DataFrame) -> pd.DataFrame:
    '''
    '''
    # Numerator
    bedrijfskosten = (
        financial_data['Handelsgoederen, grond- en hulpstoffen (60)']
        + financial_data['Diensten en diverse goederen (61)'] 
        + financial_data['Bezoldigingen, sociale lasten en pensioenen (62)'] 
        + financial_data['Afschrijvingen en waardeverminderingen op '
                         'oprichtingskosten, op immateriële en materiële vaste '
                         'activa (630)'] 
        + financial_data['Waardeverminderingen op voorraden, op bestellingen in'
                         ' uitvoering en op handelsvorderingen: toevoegingen '
                         '(terugnemingen) (631/4)'] 
        + financial_data["Voorzieningen voor risico's en kosten: toevoegingen "
                         "(bestedingen en terugnemingen) (635/8)"] 
        + financial_data['Andere bedrijfskosten (640/8)'] 
        + financial_data['Als herstructureringskosten geactiveerde '
                         'bedrijfskosten (649)']
    )

    # Denominator
    wijziging_voorraad = financial_data[
        'Voorraad goederen in bewerking en gereed product en bestellingen in '
        'uitvoering: toename (afname) (71)'
        ]
    geprod_vaste_act = financial_data[  
        'Geproduceerde vaste activa (72)'
        ]
    exploit_subs = financial_data[
        'Andere - exploitatiesubsidies en vanwege de overheid ontvangen '
        'compenserende bedragen (740)'
        ]
    overheid_kapsub = financial_data[
        'Door de overheid toegekende subsidies, aangerekend op de '
        'resultatenrekening: Kapitaalsubsidies (9125)'
        ]
    goed_bewerking = financial_data[
        'Goederen in bewerking (32)'
        ]
    gereed_product = financial_data[
        'Gereed product (33)'
        ]
    onroerend_verkoop = financial_data[
        'Onroerende goederen bestemd voor verkoop (35)'
        ]
    best_in_uitvoering = financial_data[
        'Bestellingen in uitvoering (37)'
        ]
    
    
    numerator = (bedrijfskosten - wijziging_voorraad - geprod_vaste_act
                 - exploit_subs - overheid_kapsub)
    denominator = (goed_bewerking + gereed_product 
                   + onroerend_verkoop + best_in_uitvoering)
    
    if denominator == 0:
        doi = int(0)
    else:
        doi = round(numerator/denominator)

    financial_data['DIO_finished'] = doi
    return financial_data

def inventory_cycle_crude(financial_data: pd.DataFrame) -> pd.DataFrame:
    '''
    '''
    handelsgoederen_toename = financial_data[
        'Handelsgoederen, grond- en hulpstoffen (60)'
        ]
    grondstoffen = financial_data[
        'Grond- en hulpstoffen (30/31)'
        ]   
    handelsgoederen = financial_data[
        'Handelsgoederen (34)'
        ]
    onroerend_verkoop = financial_data[
        'Onroerende goederen bestemd voor verkoop (35)'
        ]
    vooruitbetalingen = financial_data[
        'Vooruitbetalingen (36)'
        ]
    
    numerator = handelsgoederen_toename
    denominator = (grondstoffen + handelsgoederen 
                   + onroerend_verkoop + vooruitbetalingen)
    
    if denominator == 0:
        doi = int(0)
    else:
        doi = round(numerator/denominator)

    financial_data['DIO_crude'] = doi
    return financial_data

def ccc(financial_data: pd.DataFrame) -> pd.DataFrame:
    """
    Returns ccc.
    """
    dso = days_sales_outstanding(financial_data)
    dpo = days_payables_outstanding(financial_data)
    dio_crude = inventory_cycle_crude(financial_data)
    dio_finished = inventory_cycle_finished(financial_data)
    ccc = dso + (dio_crude + dio_finished) - dpo
    financial_data['ccc'] = ccc
    return financial_data

def ebit_da(financial_data: pd.DataFrame, calc='ebit') -> pd.DataFrame:
    winst_verlies = financial_data[
        'Winst (Verlies) van het boekjaar vóór belasting (9903)'
    ]
    opbr_fin_activa = financial_data[
        'Opbrengsten uit financiële vaste activa (750)'
    ]
    opbr_vlot_activa = financial_data[
        'Opbrengsten uit vlottende activa (751)'
    ]
    andere_fin_opbr = financial_data[
        'Andere financiële opbrengsten (752/9)'
    ]
    kosten_schulden = financial_data[
        'Kosten van schulden (650)'
    ]
    andere_fin_kosten = financial_data[
        'Andere financiële kosten (652/9)'
    ]
    andere_niet_rec_fin_opbr = financial_data[
        'Niet-recurrente financiële opbrengsten (76B)'
    ]
    andere_niet_rec_fin_kosten = financial_data[
        'Niet-recurrente financiële kosten (66B)'
    ]

    ebit = (winst_verlies - opbr_fin_activa - opbr_vlot_activa 
            - andere_fin_opbr + kosten_schulden + andere_fin_kosten 
            - andere_niet_rec_fin_opbr + andere_niet_rec_fin_kosten
    )
    if calc == 'ebit':
        financial_data['ebit'] = ebit
        return financial_data
    
    da_fixed_activa = financial_data[
        'Afschrijvingen en waardeverminderingen op oprichtingskosten, op '
        'immateriële en materiële vaste activa (630)'
    ]
    da_inventory = financial_data[
        'Waardeverminderingen op voorraden, op bestellingen in uitvoering en '
        'op handelsvorderingen: toevoegingen (terugnemingen) (631/4)'
    ]
    da_cur_act_non_inv_non_so = financial_data[
        'Waardeverminderingen op vlottende activa andere dan voorraden, '
        'bestellingen in uitvoering en handelsvorderingen: toevoegingen '
        '(terugnemingen) (651)'
    ]
    ebitda = ebit + da_fixed_activa + da_inventory + da_cur_act_non_inv_non_so
    if calc == 'ebitda':
        financial_data['ebitda'] = ebitda
        return financial_data