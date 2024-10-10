## What is it?

**CompanyData-NBB** is designed as a class to make an API call to the webservices of the National Bank of Belgium and to retrieve financial statements from Belgian companies and all others who are obligated to submit their results. As input it needs a KBO-number.

The script can only retrieve information from those companies that are subjected to make their financial information publically available and is, for the moment, limited to handle JSONXBRL files only. Later it should be able to handle the XBRL information that can be returned from the NBB. Though XBRL data does not seem to be as easy to convert in a workable way (let me know if you do know).<br>
De facto this means only the last two tax returns can be retrieved (I believe starting 2022) but up to three years of data (since a tax return depicts data of the current (N) and last year (NM1)).

In order to work, one has to apply for an [API key from the NBB](nbb-link).
The key is hidden as a `.env` file under the variable `NBB_CBSO_sub_key`.

[nbb-link]: https://www.nbb.be/en/central-balance-sheet-office/consultation-data/webservices


**Addition**: An upcoming extension will be to work-in data from the 'Kruispuntdatabank voor Ondernemingen' and look for similar companies.
Though additional data needs to be downloaded [here][kbo-link].

[kbo-link]: https://economie.fgov.be/nl/themas/ondernemingen/kruispuntbank-van/diensten-voor-iedereen/hergebruik-van-publieke/kruispuntbank-van-0

## Table of Contents

- [Main Features](#main-features)
- [Where to get it](#where-to-get-it)
- [License](#license)
- [Discussion and Development](#discussion-and-development)

## Main Features
There are basicly two stages: reference and data. In the reference stage we request a reference list containing all submissions of one particular company. Since we can only retrieve normal submission and no 'geconsolideerde jaarrekening', we use the URL provided in the reference list to call upon individual statements.

In the data stage, and still under construction, we will pull apart the returned dictionary into categories that make sense.

## Where to get it
Here on Github

## License
Currently none because it is not clear to me how to license a product I want to make publicly available. But by all means, I want this script to remain open source and any attempt to commercialise this or make profit from it, will be regarded as "unwanted and not allowed".

All intentions are to license this as open source, if needed.

## Discussion and Development
It still needs some refactoring in terms of general usage, as it is derived from a specific project.
Upcoming:
- Various functions for each category on a financial statement, i.e. Address, Rubrics, Shareholders etc.
- Common metrics, such as: Net Working Capital, Cash Conversion Cycle etc.
