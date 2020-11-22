DEFAULT_AGENCIES = {'police'}

mock_db = [
    {
        "name": "Complaint Response Unit (CRU)",
        "agencies": ["SARS", "FSARS"],
        "country": "Nigeria",
        "region": "ALL",
        "phone": "2348057000001, 2348057000002",
        "sms": "2348057000003",
        "email": None,
        "twitterHandle": "@PoliceNG_PCRRU, @PoliceNG_CRU",
        "whatsApp": "2348057000003",
        "link": None,
        "isDefault": False,
        "uid": "NG_CRU"
    },
    {
        "name": "Force Public Complaint Bureau",
        "agencies": ["POLICE"],
        "country": "Nigeria",
        "region": "ALL",
        "phone": "2347056792065, 2348088450152",
        "sms": None,
        "email": None,
        "twitterHandle": "@PoliceNG_CRU",
        "link": "https://www.npf.gov.ng/complaint",
        "isDefault": True,
        "uid": "NG_POLICE"
    },
    {
        "name": "Complaint Response Unit (CRU)",
        "agencies": ["POLICE"],
        "country": "United States of America",
        "region": "ALL",
        "phone": "(202) 514-3847",
        "email": "civil.feedback@usdoj.gov",
        "twitterHandle": "@TheJusticeDept",
        "link": None,
        "isDefault": True,
        "uid": "US_POLICE"
    },
]
    

class Dao:
    @staticmethod
    def find_agency_by_name(agency_name):
        for office in mock_db:
            if not office['isDefault']:
                agencies = office['agencies']
                for agency in agencies:
                    if agency == agency_name:
                        return office
    
    @staticmethod
    def find_default_agency(agency_name, country):
        print(f'looking for {agency_name} in {country}')
        for office in mock_db:
            if office['isDefault']:
                agencies = office['agencies']
                for agency in agencies:
                    if agency == agency_name and office['country'] == country:
                        return office

