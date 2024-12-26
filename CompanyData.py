"""
This module offers possibilities to handle API data from the NBB in various ways
and to the user's needs. The Class CompanyData encapsulates the two-step 
procedure in order to retrieve financial data. 

First step:
    Send URI containing unique Company Identifier, receive a reference table
    containing all filings for this company, and providing unique URI's for 
    retrieving a unique filing.

Second step:
    From the last filing up, it is possible to request more than one filing for
    a company. The result is a dictionary containing key-value pair, 
    i.e {unique_reference: data_dict}

Several functions are available for use in Python, with Pandas or an export 
function to Excel.

Data that can be retrieved:
    - Financial Data.
    - Administrator Data, if provided.
    - Participating Interests, if provided.
    - Shaerholders, if provided.
"""

import uuid
import re
import json
import os
from dotenv import load_dotenv
import pandas as pd
import requests
import fnmatch
from datetime import datetime

import dictionaries as dct

load_dotenv()
api_key = os.getenv('NBB_CBSO_sub_key')


class CompanyData:
    def __init__(self, company_number: str):
        """
        Initialize with a Company ID.
        """
        self.company_number = self._clean_input(company_number)

    def _clean_input(self, user_input: str) -> str:
        """
        Return only-numeric string or raise a ValueError.
        Remove non-numeric characters.
        
        Important: function checks the numeric correct input, not whether the 
        company ID is in the databank.
        """
        user_input = user_input.strip()
        cleaned_input = re.sub(r"\D", '', user_input)
        if len(cleaned_input) in [10, 11]:
            return cleaned_input
        else:
            raise ValueError("Wrong input - Length mismatch")
               
    def _reference_uri_creation(self) -> str:
        """
        Return an API compatible URL based on input.

        Default database is 'authentic'. Other options are 'extracts' and 
        'improved' but the function is not yet adjusted to process this.
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
        Return API response (bytes object) or HTTP Error Code.
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
    def _handle_df_of_references(
            self, 
            df_of_references: pd.DataFrame) -> pd.DataFrame:
        """
        Return filtered DataFrame.

        Select 'AccountingDataURL' column, only available for 'Jaarrekening' and
        not for 'Geconsolideerde Jaarrekening'. 
        Compare bookyears and select latest filing, in case correction was 
        submitted.
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
    
    def fetch_references(
            self, 
            year_span=1, 
            accept_reference="application/json") -> pd.DataFrame:
        """
        Return DataFrame. 
        """
        api_answer = self._api_call(
            self._reference_uri_creation(), 
            accept_reference)
        
        if isinstance(api_answer, Exception):
            return pd.DataFrame() # If 404 error, alternative way?
        
        df_of_references = pd.json_normalize(json.loads(api_answer))
        df_of_references = self._handle_df_of_references(df_of_references)
        df_of_references = df_of_references.tail(year_span)
        return df_of_references
        
    def fetch_data(
            self, 
            reference_df: pd.DataFrame, 
            accept_submission='application/x.jsonxbrl') -> dict:
        """
        Make API call based on requested years and return dictionary. 

        The amount of keys in the dictionary is equal to the amount of years 
        requested in 'fetch_references()'. Currently, it does not accept XBRL 
        format.
        """
        data_dictionary = {}
        if not reference_df.empty:
            reference_URLs = reference_df['AccountingDataURL']
            dates_dict = (reference_df.set_index('ReferenceNumber')
                        [['ExerciseDates.startDate', 'ExerciseDates.endDate']]
                        .to_dict('index'))
            
            for data_url in reference_URLs:
                try:
                    data = self._api_call(
                                    url=data_url, 
                                    accept_form=accept_submission)
                    response_dict = json.loads(data)
                    reference_number = response_dict.get('ReferenceNumber')
                    response_dict['Span'] = dates_dict[reference_number]
                    data_dictionary[reference_number] = response_dict
                except Exception as e:
                    e = 'Not a JSONXBRL'
                    print(e)
        else:
            pass # If 404 error, alternative way?
        return data_dictionary

## Functions to manipulate data
# Under construction
def format_id(company_id: str, prefix=False) -> str:
    '''
    Return CompanyID in required format.
    '''
    company_id = company_id.strip()
    cleaned_input = re.sub(r"\D", '', company_id)
    if len(cleaned_input) in [10, 11]:
        if prefix:
            part1 = cleaned_input[:4]
            part2 = cleaned_input[4:7]
            part3 = cleaned_input[7:]
            return f"BE {part1}.{part2}.{part3}"
        else:
            return cleaned_input
    else:
        raise ValueError("Wrong input - Length mismatch")

def _last_filing(company_dict: dict) -> str:
    """
    Return latest reference.
    """
    latest_year = max(
        [str(key.split(sep='-')[0]) for key in company_dict.keys()]
        )
    last_reference = fnmatch.filter(list(company_dict.keys()), 
                                      str(latest_year) + '*')[0]
    return last_reference

def _fetch_address(address_dict: dict) -> str:
    """
    Return string.
    """
    address_str = ''
    of_interest = ['Street', 'Number', 'Box', 'City', 'Country']
    for k, v in address_dict.items():
        try:
            if (v is not None) and (k in of_interest):
                address_str += f'{str(v.replace('pcd:m', '')\
                                       .replace('cty:m', ''))} '
        except:
            address_str = 'Address dictionary not found or got error'
    return address_str.strip()

def _fetch_legal_form(legal_form_dict: dict) -> str:
    """
    """
    legal_form_str = ''
    for v in legal_form_dict.values():
        try:
            if v is not None:
                legal_form_str += f'{str(v.replace('lgf:m', ''))} '
        except:
            legal_form_str = 'error in legal form dictionary or not found'
    return legal_form_str.strip()

def _fetch_mandate(mandate_dct: dict) -> str:
    """
    Return string.
    """
    mandate_str = f'{mandate_dct.get('FunctionMandate')\
                     .replace('fct:m', 'FunctionCode ')}, '
    mandate_str += f'from {mandate_dct.get('MandateDates').get('StartDate', 'NA')} '
    mandate_str += f'until {mandate_dct.get('MandateDates').get('EndDate', 'NA')}'
    return mandate_str.strip()

def _fetch_representative(rep_dict: dict) -> str:
    """
    Return name representative
    """
    rep_str = f'{rep_dict.get('FirstName').title()} '
    rep_str += f'{rep_dict.get('LastName').title()}'
    return rep_str.strip()

def _fetch_administrators(admin_dict: dict) -> dict:
    """
    Get values from nested dict-list to flat dict.
    """
    representatives = []
    rep_address = []
    entity = []
    entity_id = []
    entity_address = []
    mandate = []

    for typeOfAdmin, admin_lst in admin_dict.items():
        if (typeOfAdmin == 'LegalPersons') and admin_lst: 
            for item in admin_lst:
                dimension = len(item['Representatives'])
                for rep_dct in item['Representatives']:
                    representatives.append(_fetch_representative(rep_dct))
                    rep_address.append(_fetch_address(rep_dct['Address']))
                entity += [item['Entity'].get('Name') for x in range(0, dimension)]
                entity_id += [item['Entity'].get('Identifier') for x in range(0, dimension)]
                entity_address += [_fetch_address(item['Entity'].get('Address')) for x in range(0, dimension)]
                if item['Mandates']:
                    for mandate_dct in item['Mandates']:
                        mandate.append(_fetch_mandate(mandate_dct))  
                else:
                    mandate.append('NA')

        if (typeOfAdmin == 'NaturalPersons') and admin_lst:
            for item in admin_lst:
                representatives.append(_fetch_representative(item['Person']))
                rep_address.append(_fetch_address(item['Person']['Address']))
                entity.append('NA')
                entity_id.append('NA')
                entity_address.append('NA')
                if item['Mandates']:
                    for mandate_dct in item['Mandates']:
                        mandate.append(_fetch_mandate(mandate_dct))  
                else:
                    mandate.append('NA') 
    
    admin_dct = {
        'Representatives': representatives,
        'Rep. Address': rep_address,
        'Entity': entity,
        'Entity ID': entity_id,
        'Entity Address': entity_address,
        'Mandate': mandate
    }
    return admin_dct

def _fetch_participating_interests(pi_list: list) -> dict:
    """
    Get values from nested dict-list to flat dict.
    """
    name_participant = []
    entity_id = []
    entity_address = []
    account_date = []
    currency = []
    equity = []
    net_result = []
    interest_held_line = []
    type_of_share = []
    number_of_shares = []
    percentage_directly_held = []
    percentage_subsidiaries = []

    for dictionary in pi_list:
        if dictionary['Entity']:
            dimension = len(dictionary['ParticipatingInterestHeld'])
            name_participant += [
                dictionary['Entity'].get('Name') for x in range(0, dimension)]
            entity_id += [
                dictionary['Entity'].get('Identifier') for x in range(0, dimension)]
            entity_address += [_fetch_address(
                dictionary['Entity'].get('Address')) for x in range(0, dimension)]
            account_date += [
                dictionary['AccountDate'] for x in range(0, dimension)]
            currency += [
                dictionary['Currency'] for x in range(0, dimension)]
            equity += [
                dictionary['Equity'] for x in range(0, dimension)]
            net_result += [
                dictionary['NetResult'] for x in range(0, dimension)]
            for item in dictionary['ParticipatingInterestHeld']:
                interest_held_line += [
                    item.get('Line') for x in range(0, dimension)]
                type_of_share += [
                    item.get('Nature') for x in range(0, dimension)]
                number_of_shares += [
                    item.get('Number') for x in range(0, dimension)]
                percentage_directly_held += [
                    item.get('PercentageDirectlyHeld') for x in range(0, dimension)]
                percentage_subsidiaries += [
                    item.get('PercentageSubsidiaries') for x in range(0, dimension)]
    
    pi_dct = {
        'Participant Name':name_participant,
        'Entity ID': entity_id,
        'Entity Address': entity_address,
        'Account Date': account_date,
        'Currency': [x.replace('ccy:m', '') for x in currency],
        'Equity': equity,
        'Net Result': net_result,
        'Line': interest_held_line,
        'Type': type_of_share,
        'Number of Shares': number_of_shares,
        '% directly held': percentage_directly_held,
        '% subsidiaries': percentage_subsidiaries
    }
    return pi_dct

def _fetch_shareholders(shareholder_dict: dict, last_filing) -> dict:
    if shareholder_dict['EntityShareHolders']:
        print(f'Entity Shareholders found in {last_filing} update code')
    elif shareholder_dict['IndividualShareHolders']:
        print(f'Individual Shareholders found in {last_filing}, update code')
    else:
        raise ValueError('Not found')

def _fetch_company_info(company_dict: dict) -> dict:
    """
    Get info to dict.
    """
    company_info_dct = {
        'ReferenceNumber':[company_dict.get('ReferenceNumber', 'No Reference found')],
        'EnterpriseName':[company_dict.get('EnterpriseName', 'No Enterprisename found')],
        'Address': [_fetch_address(company_dict['Address'])],
        'Legal Form':[_fetch_legal_form(company_dict['LegalForm'])],
    }
    return company_info_dct

def fetch_quantative_data(company_dict: dict) -> pd.DataFrame:
    """
    Return four DataFrames and failed list.
    """
    last_reference = _last_filing(company_dict)
    failed = []
    
    try:
        company_df = pd.DataFrame(
            _fetch_company_info(
                company_dict[last_reference]
            )
        )
    except:
        company_df = pd.DataFrame()
        failed.append(f'Company Info {last_reference} not found')
        
    try:
        admin_df = pd.DataFrame(
            _fetch_administrators(
                company_dict[last_reference]['Administrators']
                )
            )
    except:
        admin_df = pd.DataFrame()
        failed.append(f'Administrators {last_reference} not found')

    try:
        pi_df = pd.DataFrame(
            _fetch_participating_interests(
                company_dict[last_reference]['ParticipatingInterests']
            )
        )
    except:
        pi_df = pd.DataFrame()
        failed.append(f'Participating Interests {last_reference} not found')

    try:
        shareholders_df = pd.DataFrame(
            _fetch_shareholders(
                company_dict[last_reference]['Shareholders'],
                last_reference
            )
        )
    except:
        shareholders_df = pd.DataFrame()
        failed.append(f'Shareholders {last_reference} not found')

        
    # return write to excel? add parameter
    return company_df, admin_df, pi_df, shareholders_df, failed

def _period_check(temp_dict: dict):
    begin = datetime.strptime(temp_dict.get('StartDate')\
                              .replace('-','/'), "%Y/%m/%d")
    end = datetime.strptime(temp_dict.get('EndDate')\
                            .replace('-','/'), "%Y/%m/%d")

    if (end - begin).days >= 362:
        return True
    else:
        return False

def fetch_fin_data(company_dict: dict, period='N'):

    df = pd.DataFrame()

    for symbol in period:
        for k, v in company_dict.items():
            temp_dict = {'Symbol': symbol}
            temp_dict['Reference'] = k
            temp_dict['EnterpriseName'] = v.get('EnterpriseName')
            temp_dict['StartDate'] = v['Span'].get('ExerciseDates.startDate')
            temp_dict['EndDate'] = v['Span'].get('ExerciseDates.endDate')
            
            for item in v['Rubrics']:
                if item['Period']==symbol:
                    temp_dict[item.get('Code','0')]=float(item.get('Value', '0'))

            inventory_cycle_crude(temp_dict) 

            df = pd.concat([
                df, 
                pd.DataFrame(data=temp_dict, 
                             index=[0])
                             ], ignore_index=True, sort=False)
    
    
    df.rename(mapper=dct.reversed_dict, axis=1, inplace=True)
    df.sort_values(['StartDate', 'Symbol'], 
                   ascending=[False, True],
                   inplace=True)
    df.set_index('Reference', drop=True, inplace=True)
    df.fillna(0, inplace=True)
    return df

def excel_export(company_dict, filename, period='N'):
    """
    Export to excel. Filename has to provide path.
    """
    df = fetch_fin_data(company_dict, period)
    df1, df2, df3, df4, failed = fetch_quantative_data(company_dict)
    with pd.ExcelWriter(filename) as writer:
        df1.to_excel(writer, sheet_name='Company Info')
        df.to_excel(writer, sheet_name='Fin. Data')
        df2.to_excel(writer, sheet_name='Admin Data')
        df3.to_excel(writer, sheet_name='Part. Interest')
        df4.to_excel(writer, sheet_name='Shareholders')
    print(failed)
############################# Under review ####################################

def days_sales_outstanding(temp_dict: dict) -> dict:
    '''
    '''
    if not _period_check(temp_dict):
        return temp_dict
    
    # numerator
    handelsvorderingen = temp_dict.get('40', 0)
    geendoss_handelseff = temp_dict.get('9150', 0)

    # denominator
    omzet = temp_dict.get('70', 0)
    if omzet == 0:
        temp_dict['DSO'] = 'Revenue (70) not given'
        return temp_dict
    
    andere_bedrijfsopbr = temp_dict.get('74', 0)
    exploit_subs = temp_dict.get('740', 0)
    btw_door_vennootschap = temp_dict.get('9146', 0)
    
    numerator = handelsvorderingen + geendoss_handelseff
    denominator = (omzet + andere_bedrijfsopbr
                   - exploit_subs + btw_door_vennootschap)
    
    if denominator == 0:
        dso = 'Zero Division'
    else:
        dso = round(numerator/denominator * 365)

    temp_dict['DSO'] = dso
    return temp_dict

def days_payables_outstanding(temp_dict: dict) -> dict:
    '''
    '''
    handelsschulden = temp_dict.get('44', 0)
    aankopen = temp_dict.get('600/8', 0)
    diensten_diverse = temp_dict.get('61', 0)
    btw_aan_vennootschap = temp_dict.get('9145', 0)
    
    numerator = handelsschulden
    denominator = aankopen + diensten_diverse + btw_aan_vennootschap
    
    if denominator == 0:
        dpo = 'Zero Division'
    else:
        dpo = round(numerator/denominator * 365)
    
    temp_dict['DPO'] = dpo
    return temp_dict

def inventory_cycle_finished(temp_dict: dict) -> dict:
    '''
    '''
    if not _period_check(temp_dict):
        return temp_dict
    
    # Numerator
    bedrijfskosten = (
        temp_dict.get('60', 0) + temp_dict.get('61', 0)
        + temp_dict.get('62', 0) + temp_dict.get('630', 0)
        + temp_dict.get('631/4', 0) + temp_dict.get('635/80', 0)
        + temp_dict.get('640/8', 0) + temp_dict.get('649',0)
    )

    wijziging_voorraad = temp_dict.get('71', 0)
    geprod_vaste_act = temp_dict.get('72', 0)
    exploit_subs = temp_dict.get('740', 0)
    overheid_kapsub = temp_dict.get('9125', 0)

    # Denominator
    goed_bewerking = temp_dict.get('32', 0)
    gereed_product = temp_dict.get('33', 0)
    onroerend_verkoop = temp_dict.get('35', 0)
    best_in_uitvoering = temp_dict.get('37', 0)
    
    numerator = (bedrijfskosten - wijziging_voorraad - geprod_vaste_act
                 - exploit_subs - overheid_kapsub)
    denominator = (goed_bewerking + gereed_product 
                   + onroerend_verkoop + best_in_uitvoering)
    
    if denominator == 0:
        dio = int(0)
    else:
        dio = round(numerator/denominator)

    temp_dict['DIO_finished'] = dio
    return temp_dict

def inventory_cycle_crude(temp_dict: dict) -> dict:
    '''
    '''
    if not _period_check(temp_dict):
        return temp_dict
    
    handelsgoederen_toename = temp_dict.get('60', 0)
    grondstoffen = temp_dict.get('30/31', 0)   
    handelsgoederen = temp_dict.get('34', 0)
    onroerend_verkoop = temp_dict.get('35', 0)
    vooruitbetalingen = temp_dict.get('36', 0)

    numerator = handelsgoederen_toename
    denominator = (grondstoffen + handelsgoederen 
                   + onroerend_verkoop + vooruitbetalingen)
    
    if denominator == 0:
        dio = int(0)
    else:
        dio = round(numerator/denominator)

    temp_dict['DIO_crude'] = dio
    return temp_dict

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
    