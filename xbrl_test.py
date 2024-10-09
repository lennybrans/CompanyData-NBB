import CompanyData as cd

string = "0473.416.418"

telenet = cd.CompanyData(string)

references = telenet.fetch_references()

data = telenet.fetch_xbrl(references)

# data is now a string containing all information, convert to xml.
# Download taxonomy ZIP-file at: https://www.nbb.be/nl/balanscentrale/opmaken-en-neerleggen/technische-info-en-taxonomie/definitieve-taxonomie