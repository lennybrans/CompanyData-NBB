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
    - Shareholders, if provided.
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
    """Represent the data requested and available from the NBB."""
    def __init__(self, company_id: str, year=1):
        """
        Initialise the class' attributes.
        """
        self.id = self._clean_input(company_id)
        self.reference_table = self._fetch_references()
        try:
            self.latest_filing_info = self.reference_table.tail(1)\
                .to_dict(orient='records')[0]
            self.last_reference = self.latest_filing_info.get('ReferenceNumber')
            self.enterpriseName = self.latest_filing_info.get('EnterpriseName')
            self.legalForm = self.latest_filing_info.get('LegalForm')
            self.address = {
                'Street': self.latest_filing_info.get('Address.Street'),
                'Number': self.latest_filing_info.get('Address.Number'),
                'Box': self.latest_filing_info.get('Address.Box'),
                'PostalCode': self.latest_filing_info.get('Address.PostalCode'),
                'City': self.latest_filing_info.get('Address.City'),
                'Country': self.latest_filing_info.get('Address.CountryCode')
                }
            self.data = self._fetch_data(year=year)
        except:
            pass

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
        company_id = self.id + "/"
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
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return ValueError(
                    f'No match found for {self.id} in NBB database')
            elif e.response.status_code == 429:
                raise ValueError(
                    f'Try again later, too many requests!')
            else:
                return e
            
        # For future errors
        except requests.exceptions.RequestException as req_err:
            print(f"This is a Request Error: {req_err}")
            raise req_err
        except Exception as err:
            print(f"This is a regular Error: {err}")
            raise err
    
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
    
    def _fetch_references(
            self,
            accept_reference="application/json") -> pd.DataFrame:
        """
        Return DataFrame. 
        """
        api_answer = self._api_call(
            self._reference_uri_creation(), 
            accept_reference)
        
        if isinstance(api_answer, ValueError):
            print(api_answer)
        else:
            df_of_references = pd.json_normalize(json.loads(api_answer))
            df_of_references = self._handle_df_of_references(df_of_references)
            return df_of_references

    def _fetch_data(
            self, 
            accept_type='application/x.jsonxbrl',
            year=1) -> dict:
        """
        Make API call based on requested years and return dictionary. 

        The amount of keys in the dictionary is equal to the amount of years 
        requested in 'fetch_references()'. Currently, it does not accept XBRL 
        format.
        """
        data_dictionary = {}
        reference_df = self.reference_table.tail(year)
    
        if not reference_df.empty:
            reference_URLs = reference_df['AccountingDataURL']
            add_info_dict = (reference_df.set_index('ReferenceNumber')
                        [['ExerciseDates.startDate', 'ExerciseDates.endDate',
                          'ModelType', 'DepositType',
                          'ActivityCode','LegalForm']]
                        .to_dict('index'))
            
            for data_url in reference_URLs:
                try:
                    data = self._api_call(
                                    url=data_url, 
                                    accept_form=accept_type)
                    response_dict = json.loads(data)
                    uniq_id = response_dict.get('ReferenceNumber')
                    response_dict['Additional Info'] = add_info_dict[uniq_id]
                    data_dictionary[uniq_id] = Filing(response_dict)
                except Exception as e:
                    print(e)
                    e = 'Not a JSONXBRL'
                    print(e)
        else:
            pass # If 404 error, alternative way?
        return data_dictionary

    def _fetch_address(self, address_dict: dict) -> str:
        """
        Return string.
        """
        address_str = ''
        of_interest = ['Street', 'Number', 'Box', 'PostalCode', 'City', 'Country']
        for k, v in address_dict.items():
            if (v is not None) and (k in of_interest):
                address_str += f'{v.replace('pcd:m', '').replace('cty:m', '')} '
        return address_str.strip()

    def _fetch_mandate(self, mandate_dct: dict) -> str:
        """
        Return string.
        """
        mandate_str = f'{mandate_dct.get('FunctionMandate')\
                        .replace('fct:m', 'FunctionCode ')}, '
        mandate_str += f'from {mandate_dct.get('MandateDates').get('StartDate', 'NA')} '
        mandate_str += f'until {mandate_dct.get('MandateDates').get('EndDate', 'NA')}'
        return mandate_str.strip()

    def _fetch_representative(self, rep_dict: dict) -> str:
        """
        Return name representative
        """
        rep_str = f'{rep_dict.get('FirstName').title()} '
        rep_str += f'{rep_dict.get('LastName').title()}'
        return rep_str.strip()

    def _fetch_administrators(self, admin_dict: dict) -> dict:
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
                        representatives.append(self._fetch_representative(rep_dct))
                        rep_address.append(self._fetch_address(rep_dct['Address']))
                    entity += [item['Entity'].get('Name') for x in range(0, dimension)]
                    entity_id += [item['Entity'].get('Identifier') for x in range(0, dimension)]
                    entity_address += [self._fetch_address(item['Entity'].get('Address')) for x in range(0, dimension)]
                    if item['Mandates']:
                        for mandate_dct in item['Mandates']:
                            mandate.append(self._fetch_mandate(mandate_dct))  
                    else:
                        mandate.append('NA')

            if (typeOfAdmin == 'NaturalPersons') and admin_lst:
                for item in admin_lst:
                    representatives.append(self._fetch_representative(item['Person']))
                    rep_address.append(self._fetch_address(item['Person']['Address']))
                    entity.append('NA')
                    entity_id.append('NA')
                    entity_address.append('NA')
                    if item['Mandates']:
                        for mandate_dct in item['Mandates']:
                            mandate.append(self._fetch_mandate(mandate_dct))  
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

    def _fetch_participating_interests(self, pi_list: list) -> dict:
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

        for pi_dict in pi_list:
            if pi_dict['Entity']:
                dimension = len(pi_dict['ParticipatingInterestHeld'])
                name_participant += [
                    pi_dict['Entity'].get('Name') for x in range(0, dimension)]
                entity_id += [
                    pi_dict['Entity'].get('Identifier') for x in range(0, dimension)]
                entity_address += [self._fetch_address(
                    pi_dict['Entity'].get('Address')) for x in range(0, dimension)]
                account_date += [
                    pi_dict['AccountDate'] for x in range(0, dimension)]
                currency += [
                    pi_dict['Currency'] for x in range(0, dimension)]
                equity += [
                    pi_dict['Equity'] for x in range(0, dimension)]
                net_result += [
                    pi_dict['NetResult'] for x in range(0, dimension)]
                for item in pi_dict['ParticipatingInterestHeld']:
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
            f'% directly held': percentage_directly_held,
            f'% subsidiaries': percentage_subsidiaries
        }
        return pi_dct

    def _fetch_shareholders(shareholder_dict: dict, last_filing) -> dict:
        if shareholder_dict['EntityShareHolders']:
            print(f'Entity Shareholders found in {last_filing} update code')
        elif shareholder_dict['IndividualShareHolders']:
            print(f'Individual Shareholders found in {last_filing}, update code')
        else:
            raise ValueError('Not found')

    def fetch_quantative_data(self) -> pd.DataFrame:
        """
        Return four DataFrames and failed list.
        """
        last_filing = self.data[self.last_reference]
        failed = []
        
        try:
            company_df = pd.DataFrame({
                'Company ID': self.id,
                'Company Name': self.enterpriseName,
                'Address': self._fetch_address(self.address),
                'LegalForm': self.legalForm 
            }, index=[0])
        except:
            company_df = pd.DataFrame()
            failed.append(f'Company Info {self.id} not found')
            
        try:
            admin_df = pd.DataFrame(
                self._fetch_administrators(last_filing['Administrators'])
                )
        except:
            admin_df = pd.DataFrame()
            failed.append(f'Administrators {self.last_reference} not found')

        try:
            pi_df = pd.DataFrame(
                self._fetch_participating_interests(
                    last_filing['ParticipatingInterests']
                )
            )
        except:
            pi_df = pd.DataFrame()
            failed.append(f'Part. Interests {self.last_reference} not found')

        try:
            shareholders_df = pd.DataFrame(
                self._fetch_shareholders(last_filing['Shareholders'],
                                         self.last_reference)
            )
        except:
            shareholders_df = pd.DataFrame()
            failed.append(f'Shareholders {self.last_reference} not found')
   
        # return write to excel? add parameter
        return company_df, admin_df, pi_df, shareholders_df, failed

class Filing:
    """Represent an individual filing."""
    def __init__(self, response_dictionary):
        """Initialise atrributes."""
        self.dictionary = response_dictionary
        self.enterpriseName = self.dictionary['EnterpriseName']
        self.filing_reference = self._extract(key='ReferenceNumber')
        self.startDate = self._extract(
            key='ExerciseDates.startDate', nested='Additional Info')
        self.endDate = self._extract(
            key='ExerciseDates.endDate', nested='Additional Info')
        self.modelType = self._extract(
            key='ModelType', nested='Additional Info')
        self.activityCode = self._extract(
            key='ActivityCode', nested='Additional Info')
        self.legalForm = self._extract(
            key='LegalForm', nested='Additional Info')
        self.depositType = self._extract(
            key='DepositType', nested='Additional Info')

    def _extract(self, key, nested=False):
        if not nested:
            return self.dictionary[key]
        else:
            return self.dictionary[nested].get(key)
    
    def fetch_fin_data(self, period='N', metrics=True):

        df = pd.DataFrame()

        for symbol in period:
            temp_dict = {
                'Symbol': symbol,
                'ReferenceNumber': self.filing_reference,
                'EnterpriseName': self.enterpriseName,
                'StartDate': self.startDate,
                'EndDate': self.endDate,
                }
                
            for item in self.dictionary['Rubrics']:
                if item['Period']==symbol:
                    temp_dict[item.get('Code','0')]=float(item.get('Value', '0'))
            
            if metrics:
                self.days_sales_outstanding(temp_dict)
                self.days_payables_outstanding(temp_dict)
                self.inventory_cycle_crude(temp_dict)
                self.inventory_cycle_finished(temp_dict)
                self.margin(temp_dict)

            df = pd.concat([
                df, 
                pd.DataFrame(data=temp_dict, 
                            index=[0])
                            ], ignore_index=True, sort=False)
        
        df.rename(mapper=dct.reversed_dict, axis=1, inplace=True)
        df.sort_values(['StartDate', 'Symbol'], 
                    ascending=[False, True],
                    inplace=True)
        df.set_index('ReferenceNumber', drop=True, inplace=True)
        df.fillna(0, inplace=True)
        return df

    def _period_check(self, temp_dict: dict):
        begin = datetime.strptime(temp_dict.get('StartDate')\
                                .replace('-','/'), "%Y/%m/%d")
        end = datetime.strptime(temp_dict.get('EndDate')\
                                .replace('-','/'), "%Y/%m/%d")

        if (end - begin).days >= 362:
            return True
        else:
            return False

############################# Under review ####################################
    def check_appearance(self, code, to_check):
        """Check string for appearance in list"""
        check = [fnmatch.fnmatchcase(code, i) for i in to_check]
        if sum(check) != 0:
            return True
        else:
            return False
        
    def full_schema_check(self, modeltype):
        if modeltype in ['m02-f', 'm82-f']:
            return True
        else:
            return False

    def days_sales_outstanding(self, temp_dict: dict) -> dict:
        '''
        '''
        if not self._period_check(temp_dict):
            temp_dict['DSO'] = 'Not 365 days'
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

    def days_payables_outstanding(self, temp_dict: dict) -> dict:
        '''
        '''
        if not self._period_check(temp_dict):
            temp_dict['DPO'] = 'Not 365 days'
            return temp_dict
        
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

    def inventory_cycle_finished(self, temp_dict: dict) -> dict:
        '''
        '''
        if not self._period_check(temp_dict):
            temp_dict['DIO_finished'] = 'Not 365 days'
            return temp_dict
        
        if not self.modelType in ['m02-f', 'm82-f']:
            temp_dict['DIO_finished'] = 'Not available for Abbr. or Micro model'
            return temp_dict
        
        construction = self.check_appearance(self.activityCode,
                                           ['41*', '42*','43*'])
        
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
        if construction:
            onroerend_verkoop = temp_dict.get('35', 0)
        else:
            onroerend_verkoop = 0
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

    def inventory_cycle_crude(self, temp_dict: dict) -> dict:
        '''
        '''
        if not self._period_check(temp_dict):
            temp_dict['DIO_crude'] = 'Not 365 days'
            return temp_dict
        
        if not self.modelType in ['m02-f', 'm82-f']:
            temp_dict['DIO_crude'] = 'Not available for Abbr. or Micro model'
            return temp_dict
        
        construction = self.check_appearance(self.activityCode,
                                           ['41*', '42*','43*'])
        
        handelsgoederen_toename = temp_dict.get('60', 0)
        grondstoffen = temp_dict.get('30/31', 0)   
        handelsgoederen = temp_dict.get('34', 0)
        if construction:
            onroerend_verkoop = 0
        else:
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

    def margin(self, temp_dict: dict) -> dict:
        """Calculate gross margin"""
        revenue = temp_dict.get('70', 0)
        if int(revenue) == 0:
            temp_dict['Margin'] = 'No revenue given'
            return temp_dict
        
        profit = (temp_dict.get('9901', 0)
                  - temp_dict.get('76A', 0)
                  + temp_dict.get('66A', 0))
        da = (temp_dict.get('630')
              + temp_dict.get('631/4')
              + temp_dict.get('635/8'))
        other_rev = temp_dict.get('74', 0)
        code740 = temp_dict.get('740', 0)
        code9125 = temp_dict.get('9125', 0)

        denominator = revenue + other_rev + code740
        temp_dict['Gross Margin'] = ((profit + da)*100/denominator)
        temp_dict['Net Margin'] = ((profit + code9125)*100/denominator)
        return temp_dict
        
    def addedValue_ratio(self, temp_dict: dict) -> dict:
        if self.full_schema_check(self.modelType):
            nominator = (temp_dict.get('70', 0) + temp_dict.get('71', 0)
                         + temp_dict.get('72', 0) + temp_dict.get('74', 0))

    # def ebit_da(self, temp_dict: dict) -> pd.DataFrame:
    #     """Calculate EBIT/DA"""
    #     winst_verlies = temp_dict.get('9903', 0)
    #     opbr_fin_activa = temp_dict.get('750', 0)
    #     opbr_vlot_activa = temp_dict.get('751', 0)
    #     andere_fin_opbr = temp_dict.get('752/9', 0)
    #     kosten_schulden = temp_dict.get('650', 0)
    #     andere_fin_kosten = temp_dict.get('652/9', 0)
    #     andere_niet_rec_fin_opbr = temp_dict.get('76B', 0)
    #     andere_niet_rec_fin_kosten = temp_dict.get('66B', 0)
        
    #     da_fixed_activa = temp_dict.get('630', 0)
    #     da_inventory = temp_dict.get('631/4', 0)
    #     da_cur_act_non_inv_non_so = temp_dict.get('651', 0)

    #     ebit = (winst_verlies - opbr_fin_activa - opbr_vlot_activa 
    #             - andere_fin_opbr + kosten_schulden + andere_fin_kosten 
    #             - andere_niet_rec_fin_opbr + andere_niet_rec_fin_kosten)
        
    #     ebitda = ebit + da_fixed_activa + da_inventory + da_cur_act_non_inv_non_so

    #     temp_dict['ebit'] = ebit
    #     temp_dict['ebitda'] = ebitda
    #     return temp_dict

# def excel_export(company_dict, filename, period='N'):
#     """
#     Export to excel. Filename has to provide path.
#     """
#     df = fetch_fin_data(company_dict, period)
#     df1, df2, df3, df4, failed = fetch_quantative_data(company_dict)
#     with pd.ExcelWriter(filename) as writer:
#         df1.to_excel(writer, sheet_name='Company Info')
#         df.to_excel(writer, sheet_name='Fin. Data')
#         df2.to_excel(writer, sheet_name='Admin Data')
#         df3.to_excel(writer, sheet_name='Part. Interest')
#         df4.to_excel(writer, sheet_name='Shareholders')
#     print(failed)