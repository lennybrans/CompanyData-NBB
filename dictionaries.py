qualitative_data_dictionary = {
    'Legal Name':'Entity name',
    'Legal Form':'Legal form',
    'Country':'Entity country',
    'City':'Entity city',
    'Postal code':'Entity postal code',
    'Street':'Entity address street',
    'ID':'Entity number',
    'Taal':'Language',
    'Start':'Accounting period start date',
    'End':'Accounting period end date',
    'Approval':'General assembly date'      
    }

bookcodes_dictionary = {
    # VASTE ACTIVA
    'OPRICHTINGSKOSTEN (20)':'20',
    'VASTE ACTIVA (21/28)':'21/28',
    'Immateriële vaste activa (21)':'21',
    'Materiële vaste activa (22/27)':'22/27',
    'Terreinen en gebouwen (22)':'22',
    'Installaties, machines en uitrusting (23)':'23',
    'Meubilair en rollend materieel (24)':'24',
    'Leasing en soortgelijke rechten (25)':'25',
    'Overige materiële vaste activa (26)':'26',
    'Activa in aanbouw en vooruitbetalingen (27)':'27',
    'Financiële vaste activa (28)':'28',
    'Verbonden ondernemingen (280/1)':'280/1',
    'Deelnemingen (280)':'280',
    'Vorderingen (281)':'281',
    'Ondernemingen waarmee een deelnemingsverhouding bestaat '
    '(282/3)':'282/3',
    'Deelnemingen (282)':'282',
    'Vorderingen (283)':'283',
    'Andere financiële vaste activa (284/8)':'284/8',
    'Aandelen (284)':'284',
    'Vorderingen en borgtochten in contanten (285/8)':'285/8',
    # VLOTTENDE ACTIVA
    'VLOTTENDE ACTIVA (29/58)':'29/58',
    'Vorderingen op meer dan één jaar (29)':'29',
    'Handelsvorderingen (290)':'290',
    'Overige vorderingen (291)':'291',
    'Voorraden en bestellingen in uitvoering (3)':'3',
    'Voorraden (30/36)':'30/36',
    'Grond- en hulpstoffen (30/31)':'30/31',
    'Goederen in bewerking (32)':'32',
    'Gereed product (33)':'33',
    'Handelsgoederen (34)':'34',
    'Onroerende goederen bestemd voor verkoop (35)':'35',
    'Vooruitbetalingen (36)':'36',
    'Bestellingen in uitvoering (37)':'37',
    'Vorderingen op ten hoogste één jaar (40/41)':'40/41',
    'Handelsvorderingen (40)':'40',
    'Overige vorderingen (41)':'41',
    'Geldbeleggingen (50/53)':'50/53',
    'Eigen aandelen (50)':'50',
    'Overige beleggingen (52/53)':'51/53',
    'Liquide middelen (54/58)':'54/58',
    'Overlopende rekeningen (490/1)':'490/1',
    'TOTAAL VAN DE ACTIVA (20/58)':'20/58',
    # VASTE PASSIVA / EIGEN VERMOGEN
    'EIGEN VERMOGEN (10/15)':'10/15',
    'Inbreng (10/11)':'10/11',
    'Kapitaal (10)':'10',
    'Geplaatst kapitaal (100)':'100',
    'Niet-opgevraagd kapitaal (101)':'101',
    'Buiten kapitaal (11)':'11',
    'Uitgiftepremies (1100/10)':'1100/10',
    'Andere (1109/19)':'1109/19',
    'Herwaarderingsmeerwaarden (12)':'12',
    'Reserves (13)':'13',
    'Onbeschikbare reserves (130/1)':'130/1',
    'Wettelijke reserve (130)':'130',
    'Statutair onbeschikbare reserves (1311)':'1311',
    'Inkoop eigen aandelen (1312)':'1312',
    'Financiële steunverlening (1313)':'1313',
    'Overige (1319)':'1319',
    'Belastingvrije reserves (132)':'132',
    'Beschikbare reserves (133)':'133',
    'Overgedragen winst (verlies) (14)':'14',
    'Kapitaalsubsidies (15)':'15',
    'Voorschot aan de vennoten op de verdeling van het netto- actief '
    '(19)':'19',
    'VOORZIENINGEN EN UITGESTELDE BELASTINGEN (16)':'16',
    "Voorzieningen voor risico's en kosten (160/5)":'160/5',
    'Pensioenen en soortgelijke verplichtingen (160)':'160',
    'Belastingen (161)':'161',
    'Grote herstellings- en onderhoudswerken (162)':'162',
    'Milieuverplichtingen (163)':'163',
    "Overige risico's en kosten (164/5)":'164/5',
    'Uitgestelde belastingen (168)':'168',
    # VLOTTENDE ACTIVA / SCHULDEN
    'SCHULDEN (17/49)':'17/49',
    'Schulden op meer dan één jaar (17)':'17',
    'Financiële schulden (170/4)':'170/4',
    'Achtergestelde leningen (170)':'170',
    'Niet-achtergestelde obligatieleningen (171)':'171',
    'Leasingschulden en soortgelijke schulden (172)':'172',
    'Kredietinstellingen (173)':'173',
    'Overige leningen (174)':'174',
    'Handelsschulden (175)':'175',
    'Leveranciers (1750)':'1750',
    'Te betalen wissels (1751)':'1751',
    'Vooruitbetalingen op bestellingen (176)':'176',
    'Overige schulden (178/9)':'178/9',
    'Schulden op ten hoogste één jaar (42/48)':'42/48',
    'Schulden op meer dan één jaar die binnen het jaar vervallen (42)':'42',
    'Financiële schulden (43)':'43',
    'Kredietinstellingen (430/8)':'430/8',
    'Overige leningen (439)':'439',
    'Handelsschulden (44)':'44',
    'Leveranciers (440/4)':'440/4',
    'Te betalen wissels (441)':'441',
    'Vooruitbetalingen op bestellingen (46)':'46',
    'Schulden met betrekking tot belastingen, bezoldigingen en sociale '
    'lasten (45)':'45',
    'Belastingen (450/3)':'450/3',
    'Bezoldigingen en sociale lasten (454/9)':'454/9',
    'Overige schulden (47/48)':'47/48',
    'Overlopende rekeningen (492/3)':'492/3',
    'TOTAAL VAN DE PASSIVA (10/49)':'10/49',
    # RESULTATENREKENING
    'Brutomarge (9900)':'9900',
    'Bedrijfsopbrengsten (70/76A)':'70/76A',
    'Omzet (70)':'70',
    'Voorraad goederen in bewerking en gereed product en bestellingen in '
    'uitvoering: toename (afname) (71)':'71',
    'Geproduceerde vaste activa (72)':'72',
    'Andere bedrijfsopbrengsten (74)':'74',
    'Niet-recurrente bedrijfsopbrengsten (76A)':'76A',
    'Bedrijfskosten (60/66A)':'60/66A',
    'Handelsgoederen, grond- en hulpstoffen (60)':'60',
    'Aankopen (600/8)':'600/8',
    'Voorraad: afname (toename) (609)':'609',
    'Diensten en diverse goederen (61)':'61',
    'Bezoldigingen, sociale lasten en pensioenen (62)':'62',
    'Afschrijvingen en waardeverminderingen op oprichtingskosten, op '
    'immateriële en materiële vaste activa (630)':'630',
    'Waardeverminderingen op voorraden, op bestellingen in uitvoering en '
    'op handelsvorderingen: toevoegingen (terugnemingen) (631/4)':'631/4',
    "Voorzieningen voor risico's en kosten: toevoegingen (bestedingen en "
    "terugnemingen) (635/8)":'635/8',
    'Andere bedrijfskosten (640/8)':'640/8',
    'Als herstructureringskosten geactiveerde bedrijfskosten (649)':'649',
    'Niet-recurrente bedrijfskosten (66A)':'66A',
    'Bedrijfswinst (Bedrijfsverlies) (9901)':'9901',
    'Financiële opbrengsten (75/76B)':'75/76B',
    'Recurrente financiële opbrengsten (75)':'75',
    'Opbrengsten uit financiële vaste activa (750)':'750',
    'Opbrengsten uit vlottende activa (751)':'751',
    'Andere financiële opbrengsten (752/9)':'752/9',
    'Niet-recurrente financiële opbrengsten (76B)':'76B',
    'Financiële kosten (65/66B)':'65/66B',
    'Recurrente financiële kosten (65)':'65',
    'Kosten van schulden (650)':'650',
    'Waardeverminderingen op vlottende activa andere dan voorraden, '
    'bestellingen in uitvoering en handelsvorderingen: toevoegingen '
    '(terugnemingen) (651)':'651',
    'Andere financiële kosten (652/9)':'652/9',
    'Niet-recurrente financiële kosten (66B)':'66B',
    'Winst (Verlies) van het boekjaar vóór belasting (9903)':'9903',
    'Onttrekking aan de uitgestelde belastingen (780)':'780',
    'Overboeking naar de uitgestelde belastingen (680)':'680',
    'Belastingen op het resultaat (67/77)':'67/77',
    'Belastingen (670/3)':'670/3',
    'Regularisering van belastingen en terugneming van voorzieningen voor '
    'belastingen (77)':'77',
    'Winst (Verlies) van het boekjaar (9904)':'9904',
    'Onttrekking aan de belastingvrije reserves (789)':'789',
    'Overboeking naar de belastingvrije reserves (689)':'689',
    'Te bestemmen winst (verlies) van het boekjaar (9905)':'9905',
    # RESULTAATVERWERKING
    'Te bestemmen winst (verlies) (9906)':'9906',
    'Te bestemmen winst (verlies) van het boekjaar (9905)':'9905',
    'Overgedragen winst (verlies) van het vorige boekjaar (14P)':'14P',
    'Onttrekking aan het eigen vermogen (791/2)':'791/2',
    'aan de inbreng (791)':'791',
    'aan de reserves (792)':'792',
    'Toevoeging aan het eigen vermogen (691/2)':'691/2',
    'aan de inbreng (691)':'691',
    'aan de wettelijke reserve (6920)':'6920',
    'aan de overige reserves (6921)':'6921',
    'Over te dragen winst (verlies) (14)':'14',
    'Tussenkomst van de vennoten in het verlies (794)':'794',
    'Uit te keren winst (694/7)':'694/7',
    'Vergoeding van de inbreng (694)':'694',
    'Bestuurders of zaakvoerders (695)':'695',
    'Werknemers (696)':'696',
    'Andere rechthebbenden (697)':'697',
    # STAAT VAN IMMATERIELE VASTE ACTIVA
    'IMA Aanschaffingswaarde per einde van het boekjaar (8025P)':'8025P',
    # Mutaties tijdens het boekjaar
    'IMA Aanschaffingen, met inbegrip van de geproduceerde vaste activa '
    '(8022)':'8022',
    'IMA Overdrachten en buitengebruikstellingen (8032)':'8032',
    'IMA Overboekingen van een post naar een andere (8042)':'8042',
    'IMA Aanschaffingswaarde per einde van het boekjaar (8052)':'8052',
    'IMA Afschrijvingen en waardeverminderingen per einde van het boekjaar '
    '(8122P)':'8122P',
    # Mutaties tijdens het boekjaar
    'IMA Geboekt (8072)':'8072',
    'IMA Teruggenomen (8082)':'8082',
    'IMA Verworven van derden (8092)':'8092',
    'IMA Afgeboekt na overdrachten en buitengebruikstellingen '
    '(8102)':'8102',
    'IMA Overgeboekt van een post naar een andere (8112)':'8112',
    'IMA Afschrijvingen en waardeverminderingen per einde van het boekjaar '
    '(8122)':'8122',
    'IMA NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR (211)':'211',
    # GOODWILL
    'GW Aanschaffingswaarde per einde van het boekjaar (8053P)':'8053P',
    # Mutaties tijdens het boekjaar
    'GW Aanschaffingen, met inbegrip van de geproduceerde vaste activa '
    '(8023)':'8023',
    'GW Overdrachten en buitengebruikstellingen (8033)':'8033',
    'GW Overboekingen van een post naar een andere (8043)':'8043',
    'GW Aanschaffingswaarde per einde van het boekjaar (8053)':'8053',
    'GW Afschrijvingen en waardeverminderingen per einde van het boekjaar '
    '(8123P)':'8123P',
    # Mutaties tijdens het boekjaar
    'GW Geboekt (8073)':'8073',
    'GW Teruggenomen (8083)':'8083',
    'GW Verworven van derden (8093)':'8093',
    'GW Afgeboekt na overdrachten en buitengebruikstellingen (8103)':'8103',
    'GW Overgeboekt van een post naar een andere (8113)':'8113',
    'GW Afschrijvingen en waardeverminderingen per einde van het boekjaar '
    '(8123)':'8123',
    'GW NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR (212)':'212',
    # STAAT VAN MATERIELE VASTE ACTIVA
    'MA Aanschaffingswaarde per einde van het boekjaar (8192P)':'8192P',
    # Mutaties tijdens het boekjaar
    'MA Aanschaffingen, met inbegrip van de geproduceerde vaste activa '
    '(8162)':'8162',
    'MA Overdrachten en buitengebruikstellingen (8172)':'8172',
    'MA Overboekingen van een post naar een andere (8182)':'8182',
    'MA Aanschaffingswaarde per einde van het boekjaar (8192)':'8192',
    'MA Meerwaarden per einde van het boekjaar (8252P)':'8252P',
    # Mutaties tijdens het boekjaar
    'MA Geboekt (8212)':'8212',
    'MA Verworven van derden (8222)':'8222',
    'MA Afgeboekt (8232)':'8232',
    'MA Overgeboekt van een post naar een andere (8242)':'8242',
    'MA Meerwaarden per einde van het boekjaar (8252)':'8252',
    'MA Afschrijvingen en waardeverminderingen per einde van het boekjaar '
    '(8322P)':'8322P',
    # Mutaties tijdens het boekjaar
    'MA Geboekt (8272)':'8272',
    'MA Teruggenomen (8282)':'8282',
    'MA Verworven van derden (8292)':'8292',
    'MA Afgeboekt na overdrachten en buitengebruikstellingen (8302)':'8302',
    'MA Overgeboekt van een post naar een andere (8312)':'8312',
    'MA Afschrijvingen en waardeverminderingen per einde van het boekjaar '
    '(8322)':'8322',
    'MA NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR (23)':'23',
    # MEUBILAIR EN ROLLEND MATERIEEL
    'MeuRolMat Aanschaffingswaarde per einde van het boekjaar '
    '(8193P)':'8193P',
    # Mutaties tijdens het boekjaar
    'MeuRolMat Aanschaffingen, met inbegrip van de geproduceerde vaste '
    'activa (8163)':'8163',
    'MeuRolMat Overdrachten en buitengebruikstellingen (8173)':'8173',
    'MeuRolMat Overboekingen van een post naar een andere (8183)':'8183',
    'MeuRolMat Aanschaffingswaarde per einde van het boekjaar '
    '(8193)':'8193',
    'MeuRolMat Meerwaarden per einde van het boekjaar (8253P)':'8253P',
    # Mutaties tijdens het boekjaar
    'MeuRolMat Geboekt (8213)':'8213',
    'MeuRolMat Verworven van derden (8223)':'8223',
    'MeuRolMat Afgeboekt (8233)':'8233',
    'MeuRolMat Overgeboekt van een post naar een andere (8243)':'8243',
    'MeuRolMat Meerwaarden per einde van het boekjaar (8253)':'8253',
    'MeuRolMat Afschrijvingen en waardeverminderingen per einde van het '
    'boekjaar (8323P)':'8323P',
    # Mutaties tijdens het boekjaar
    'MeuRolMat Geboekt (8273)':'8273',
    'MeuRolMat Teruggenomen (8283)':'8283',
    'MeuRolMat Verworven van derden (8293)':'8293',
    'MeuRolMat Afgeboekt na overdrachten en buitengebruikstellingen '
    '(8303)':'8303',
    'MeuRolMat Overgeboekt van een post naar een andere (8313)':'8313',
    'MeuRolMat Afschrijvingen en waardeverminderingen per einde van het '
    'boekjaar (8323)':'8323',
    'MeuRolMat NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR (24)':'24',
    # OVERIGE MATERIELE VASTE ACTIVE
    'OvMat Aanschaffingswaarde per einde van het boekjaar (8195P)':'8195P',
    # Mutaties tijdens het boekjaar
    'OvMat Aanschaffingen, met inbegrip van de geproduceerde vaste activa '
    '(8165)':'8165',
    'OvMat Overdrachten en buitengebruikstellingen (8175)':'8175',
    'OvMat Overboekingen van een post naar een andere (8185)':'8185',
    'OvMat Aanschaffingswaarde per einde van het boekjaar (8195)':'8195',
    'OvMat Meerwaarden per einde van het boekjaar (8255P)':'8255P',
    # Mutaties tijdens het boekjaar
    'OvMat Geboekt (8215)':'8215',
    'OvMat Verworven van derden (8225)':'8225',
    'OvMat Afgeboekt (8235)':'8235',
    'OvMat Overgeboekt van een post naar een andere (8245)':'8245',
    'OvMat Meerwaarden per einde van het boekjaar (8255)':'8255',
    'OvMat Afschrijvingen en waardeverminderingen per einde van het '
    'boekjaar (8325P)':'8325P',
    # Mutaties tijdens het boekjaar
    'OvMat Geboekt (8275)':'8275',
    'OvMat Teruggenomen (8285)':'8285',
    'OvMat Verworven van derden (8295)':'8295',
    'OvMat Afgeboekt na overdrachten en buitengebruikstellingen '
    '(8305)':'8305',
    'OvMat Overgeboekt van een post naar een andere (8315)':'8315',
    'OvMat Afschrijvingen en waardeverminderingen per einde van het '
    'boekjaar (8325)':'8325',
    'OvMat NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR (26)':'26',
    # FINANCIELE VASTE ACTIVA
    # Ondernemingen met deelnemersverhouding - deelnemingen en aandelen
    'FA Aanschaffingswaarde per einde van het boekjaar (8392P)':'8392P',
    # Mutaties tijdens het boekjaar
    'FA Aanschaffingen, met inbegrip van de geproduceerde vaste activa '
    '(8362)':'8362',
    'FA Overdrachten en buitengebruikstellingen (8372)':'8372',
    'FA Overboekingen van een post naar een andere (8382)':'8382',
    'FA Aanschaffingswaarde per einde van het boekjaar (8392)':'8392',
    'FA Meerwaarden per einde van het boekjaar (8452P)':'8452P',
    # Mutaties tijdens het boekjaar
    'FA Geboekt (8412)':'8412',
    'FA Verworven van derden (8422)':'8422',
    'FA Afgeboekt (8432)':'8432',
    'FA Overgeboekt van een post naar een andere (8442)':'8442',
    'FA Meerwaarden per einde van het boekjaar (8452)':'8452',
    'FA Afschrijvingen en waardeverminderingen per einde van het boekjaar '
    '(8522P)':'8522P',
    # Mutaties tijdens het boekjaar
    'FA Geboekt (8472)':'8472',
    'FA Teruggenomen (8482)':'8482',
    'FA Verworven van derden (8492)':'8492',
    'FA Afgeboekt na overdrachten en buitengebruikstellingen (8502)':'8502',
    'FA Overgeboekt van een post naar een andere (8512)':'8512',
    'FA Waardeverminderingen per einde van het boekjaar (8522)':'8522',
    'FA Niet-opgevraagde bedragen per einde van het boekjaar '
    '(8552P)':'8552P',
    'FA Mutaties tijdens het boekjaar (8542)':'8542',
    'FA Niet-opgevraagde bedragen per einde van het boekjaar (8552)':'8552',
    'FA NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR (282)':'282',
    # Ondernemingen met deelnemersverhouding - vorderingen
    'FA NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR (283P)':'283P',
    'FA Toevoegingen (8582)':'8582',
    'FA Terugbetalingen (8592)':'8592',
    'FA Geboekte waardeverminderingen (8602)':'8602',
    'FA Teruggenomen waardeverminderingen (8612)':'8612',
    'FA Wisselkoersverschillen (8622)':'8622',
    'FA Overige mutaties (8632)':'8632',
    'FA NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR (283)':'283',
    'FA GECUMULEERDE WAARDEVERMINDERINGEN OP VORDERINGEN PER EINDE '
    'BOEKJAAR (8652)':'8652',
    # Andere Ondernemingen met deelnemersverhouding - deelnemingen en aandelen
    'FA_andere Aanschaffingswaarde per einde van het boekjaar '
    '(8393P)':'8393P',
    # Mutaties tijdens het boekjaar
    'FA_andere Aanschaffingen, met inbegrip van de geproduceerde vaste '
    'activa (8363)':'8363',
    'FA_andere Overdrachten en buitengebruikstellingen (8373)':'8373',
    'FA_andere Overboekingen van een post naar een andere (8383)':'8383',
    'FA_andere Aanschaffingswaarde per einde van het boekjaar '
    '(8393)':'8393',
    'FA_andere Meerwaarden per einde van het boekjaar (8453P)':'8453P',
    # Mutaties tijdens het boekjaar
    'FA_andere Geboekt (8413)':'8413',
    'FA_andere Verworven van derden (8423)':'8423',
    'FA_andere Afgeboekt (8433)':'8433',
    'FA_andere Overgeboekt van een post naar een andere (8443)':'8443',
    'FA_andere Meerwaarden per einde van het boekjaar (8453)':'8453',
    'FA_andere Afschrijvingen en waardeverminderingen per einde van het '
    'boekjaar (8523P)':'8523P',
    # Mutaties tijdens het boekjaar
    'FA_andere Geboekt (8473)':'8473',
    'FA_andere Teruggenomen (8483)':'8483',
    'FA_andere Verworven van derden (8493)':'8493',
    'FA_andere Afgeboekt na overdrachten en buitengebruikstellingen '
    '(8503)':'8503',
    'FA_andere Overgeboekt van een post naar een andere (8513)':'8513',
    'FA_andere Waardeverminderingen per einde van het boekjaar '
    '(8523)':'8523',
    'FA_andere Niet-opgevraagde bedragen per einde van het boekjaar '
    '(8553P)':'8553P',
    'FA_andere Mutaties tijdens het boekjaar (8543)':'8543',
    'FA_andere Niet-opgevraagde bedragen per einde van het boekjaar '
    '(8553)':'8553',
    'FA_andere NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR (284)':'284',
    # Ondernemingen met deelnemersverhouding - vorderingen
    'FA_andere NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR '
    '(285/8P)':'285/8P',
    'FA_andere Toevoegingen (8583)':'8583',
    'FA_andere Terugbetalingen (8593)':'8593',
    'FA_andere Geboekte waardeverminderingen (8603)':'8603',
    'FA_andere Teruggenomen waardeverminderingen (8613)':'8613',
    'FA_andere Wisselkoersverschillen (8623)':'8623',
    'FA_andere Overige mutaties (8633)':'8633',
    'FA_andere NETTOBOEKWAARDE PER EINDE VAN HET BOEKJAAR (285/8)':'285/8',
    'FA_andere GECUMULEERDE WAARDEVERMINDERINGEN OP VORDERINGEN PER EINDE '
    'BOEKJAAR (8653)':'8653',
    # Geldbeleggingen en overlopende rekeningen
    'Aandelen en geldbeleggingen andere dan vastrentende beleggingen '
    '(51)':'51',
    'Aandelen - Boekwaarde verhoogd met het niet-opgevraagde bedrag '
    '(8681)':'8681',
    'Aandelen - Niet-opgevraagd bedrag (8682)':'8682',
    'Edele metalen en kunstwerken (8683)':'8683',
    'Vastrentende effecten (v)':'52',
    'Vastrentende effecten uitgegeven door kredietinstellingen '
    '(8684)':'8684',
    'Termijnrekeningen bij kredietinstellingen (53)':'53',
    'Met een resterende looptijd of opzegtermijn van hoogstens één maand '
    '(8686)':'8686',
    'Met een resterende looptijd of opzegtermijn van meer dan één maand en '
    'hoogstens één jaar(8687)':'8687',
    'Met een resterende looptijd of opzegtermijn van meer dan één jaar '
    '(8788)':'8788',
    'Hierboven niet-opgenomen overige geldbeleggingen (8689)':'8689',
    # STAAT V/H KAPITAAL EN DE AANDEELHOUDERSTRUCTUUR
    # Kapitaal
    'Geplaatst kapitaal per einde van het boekjaar (100P)':'100P',
    'Geplaatst kapitaal per einde van het boekjaar (100)':'100',
    # 'Wijzigingen tijdens het boekjaar'
    # 'Samenstelling van het kapitaal Soorten aandelen':,
    'Aandelen op naam (8702)': '8702',
    'Gedematerialiseerde aandelen (8703)':'8703',
    # Niet-gestort kapitaal
    'Niet-opgevraagd kapitaal (101)':'101',
    'Opgevraagd, niet-gestort kapitaal Aandeelhouders die nog moeten '
    'volstorten (8712)':'8712',
    # Eigen aandelen
    # Gehouden door de vennootschap zelf
    'Eigen aandelen gehouden door de vennootschap zelf - Kapitaalbedrag '
    '(8721)':'8721',
    'Aantal aandelen (8722)':'8722',
    'Eigen aandelen gehouden door haar dochters - Kapitaalbedrag '
    '(8731)':'8731',
    'Aantal aandelen (8732)':'8732',
    'Verplichtingen tot uitgifte van aandelen als gevolg van de uitoefening'
    'van conversierechten - Bedrag van de lopende converteerbare leningen '
    '(8740)':'8740',
    'Verplichtingen tot uitgifte van aandelen als gevolg van de uitoefening'
    ' van conversierechten - Bedrag van het te plaatsen kapitaal '
    '(8741)':'8741',
    'Verplichtingen tot uitgifte van aandelen als gevolg van de uitoefening'
    ' van conversierechten - Maximum aantal uit te geven aandelen '
    '(8742)':'8742',
    'Verplichtingen tot uitgifte van aandelen als gevolg van de uitoefening'
    ' van inschrijvingsrechten - Aantal inschrijvingsrechten in omloop '
    '(8745)':'8745',
    'Verplichtingen tot uitgifte van aandelen als gevolg van de uitoefening'
    ' van inschrijvingsrechten - Bedrag van het te plaatsen kapitaal '
    '(8746)':'8746',
    'Verplichtingen tot uitgifte van aandelen als gevolg van de uitoefening'
    ' van inschrijvingsrechten - Maximum aantal uit te geven aandelen '
    '(8747)':'8747',
    'Toegestaan, niet-geplaatst kapitaal (8751)':'8751',
    'Aandelen buiten kapitaal - Verdeling - Aantal aandelen (8761)':'8761',
    'Aandelen buiten kapitaal - Verdeling -Daaraan verbonden stemrecht '
    '(8762)':'8762',
    'Uitsplitsing volgens de aandeelhouders - Aantal aandelen gehouden door'
    ' de vennootschap zelf (8771)':'8771',
    'Uitsplitsing volgens de aandeelhouders - Aantal aandelen gehouden door'
    ' haar dochters (8781)':'8781',
    # STAAT VAN SCHULDEN
    # BEDRIJFSRESULTATEN
    # Bedrijfsopbrengsten
    'Andere - exploitatiesubsidies en vanwege de overheid ontvangen '
    'compenserende bedragen (740)':'740',
    # Bedrijfskosten
    'Werknemers waarvoor de vennootschap een DIMONA-verklaring heeft '
    'ingediend of die zijn ingeschreven in het algemeen personeelsregister'
    ' - Totaal aantal op de afsluitingsdatum (9086)':'9086',
    'Gemiddeld personeelsbestand berekend in voltijdse equivalenten '
    '(9087)':'9087',
    'Aantal daadwerkelijk gepresteerde uren (9088)':'9088',
    'Personeelskosten - Bezoldigingen en rechtstreekse sociale voordelen '
    '(620)':'620',
    'Personeelskosten - Werkgeversbijdragen voor sociale verzekeringen '
    '(621)':'621',
    'Personeelskosten - Werkgeverspremies voor bovenwettelijke '
    'verzekeringen (622)':'622',
    'Personeelskosten - Andere personeelskosten (623)':'623',
    'Personeelskosten - Ouderdoms- en overlevingspensioenen (624)':'624',
    'Voorzieningen voor pensioenen en soortgelijke verplichtingen - '
    'Toevoegingen (bestedingen en terugnemingen) (635)':'635',
    'Waardeverminderingen - Op voorraden en bestellingen in uitvoering - '
    'Geboekt (9110)':'9110',
    'Waardeverminderingen - Op voorraden en bestellingen in uitvoering - '
    'Teruggenomen (9111)':'9111',
    'Waardeverminderingen - Op handelsvorderingen - Geboekt (9112)':'9112',
    'Waardeverminderingen - Op handelsvorderingen - Teruggenomen '
    '(9113)':'9113',
    "Voorzieningen voor risico's en kosten - Toevoegingen (9115)":'9115',
    "Voorzieningen voor risico's en kosten - Bestedingen en terugnemingen "
    "(9116)":'9116',
    'Andere bedrijfskosten - Bedrijfsbelastingen en -taksen (640)':'640',
    'Andere bedrijfskosten - Andere (641/8)':'641/8',
    'Uitzendkrachten en ter beschikking van de vennootschap gestelde '
    'personen - Totaal aantal op de afsluitingsdatum (9096)':'9096',
    'Uitzendkrachten en ter beschikking van de vennootschap gestelde '
    'personen - Gemiddeld aantal berekend in voltijdse equivalenten '
    '(9097)':'9097',
    'Uitzendkrachten en ter beschikking van de vennootschap gestelde '
    'personen - Aantal daadwerkelijk gepresteerde uren (9098)':'9098',
    'Uitzendkrachten en ter beschikking van de vennootschap gestelde '
    'personen - Kosten voor de vennootschap (617)':'617',
    # FINANCIËLE RESULTATEN - IN DETAIL
    # Reccurente financiele opbrengsten
    'Door de overheid toegekende subsidies, aangerekend op de '
    'resultatenrekening: Kapitaalsubsidies (9125)': '9125',
    'Door de overheid toegekende subsidies, aangerekend op de '
    'resultatenrekening: Interestsubsidies (9126)': '9126',
    'Uitsplitsing van de overige financiële opbrengsten - Gerealiseerde '
    'wisselkoersverschillen (754)': '754',
    # Reccurente financiele kosten
    'Afschrijving van kosten bij uitgifte van leningen (6501)': '6501',
    'Geactiveerde interesten (6502)': '6502',
    'Waardeverminderingen op vlottende activa - geboekt (6510)': '6510',
    'Waardeverminderingen op vlottende activa - geboekt (6511)': '6511',
    'Andere FK - Bedrag van het disconto ten laste van de vennootschap bij de '
    'verhandeling van vorderingen (653)': '653',
    'Voorzieningen met fin. karakter - toevoegingen (6560)': '6560',
    'Voorzieningen met fin. karakter - bestedingen en terugnemingen '
    '(6561)': '6561',
    'Uitsplitsing van overige fin. kosten - gerealiseerde wisselkoerswinsten '
    '(654)': '654',
    'Uitsplitsing van overige fin. kosten - resultaten uit de omrekening van '
    'vreemde valuta (655)': '655',
    # Niet-reccurente opbrengsten
    'Terugneming van afschrijvingen en van waardeverminderingen op immateriële '
    'en materiële vaste activa (760)': '760',
    "Terugneming van voorzieningen voor niet-recurrente bedrijfsrisico's en - "
    "kosten (7620)": "7620",
    'Meerwaarden bij de realisatie van immateriële en materiële vaste activa '
    '(7630)': '7630',
    'Andere niet-recurrente bedrijfsopbrengsten (764/8)': '764/8',
    'Terugneming van waardeverminderingen op financiële vaste activa '
    '(761)': '761',
    "Terugneming van voorzieningen voor niet-recurrente financiële risico's en "
    "kosten (7621)": "7621",
    'Meerwaarden bij de realisatie van financiële vaste activa (7631)': '7631',
    'Andere niet-recurrente financiële opbrengsten (769)': '769',
    # Niet-reccurente kosten
    'Niet-recurrente afschrijvingen en waardeverminderingen op '
    'oprichtingskosten, op immateriële en materiële vaste activa (660)':'660',
    "Voorzieningen voor niet-recurrente bedrijfsrisico's en -kosten: "
    "toevoegingen (bestedingen) (6620)": "6620",
    'Minderwaarden bij de realisatie van immateriële en materiële vaste activa '
    '(6630)': '6630',
    'Andere niet-recurrente bedrijfskosten (664/7)': '664/7',
    'Als herstructureringskosten geactiveerde niet-recurrente bedrijfskosten '
    '(6690)': '6690',
    'Waardeverminderingen op financiële vaste activa (661)': '661',
    "Voorzieningen voor niet-recurrente financiële risico's en kosten: "
    "toevoegingen (bestedingen) (6621)": "6621",
    'Minderwaarden bij de realisatie van financiële vaste activa '
    '(6631)': '6631',
    'Andere niet-recurrente financiële kosten (668)': '668',
    'Als herstructureringskosten geactiveerde niet-recurrente financiële kosten'
    ' (6691)': '6691',
    # OPBRENGSTEN EN KOSTEN VAN UITZONDERLIJKE OMVANG OF UITZONDERLIJKE 
    # MATE VAN VOORKOMEN
    #' ()':'',
    # BELASTINGEN EN TAKSEN
    # Belastingen op het resultaat
    'Belastingen op het resultaat van het boekjaar (9134)': '9134',
    'Belastingen op het resultaat vorige boekjaren (9138)': '9138',
    'Bronnen van belastingslatenties - actieve (9141)': '9141',
    'Bronnen van belastingslatenties - passieve (9144)': '9144',
    # Belastingen op de toegevoegde waarde en belastingen ten laste van derden
    'In rekening gebrachte belasting op de toegevoegde waarde - aan '
    'vennootschap (9145)': '9145',
    'In rekening gebrachte belasting op de toegevoegde waarde - door '
    'vennootschap (9146)': '9146',
    'Ingehouden bedragen ten laste van derden bij wijze van - '
    'bedrijfsvoorheffing (9147)': '9147',
    'Ingehouden bedragen ten laste van derden bij wijze van - '
    'roerende voorheffing (9148)': '9148',
    # NIET IN DE BALANS OPGENOMEN RECHTEN EN VERPLICHTINGEN
    'Door de vennootschap gestelde of onherroepelijk beloofde persoonlijke '
    'zekerheden als waarborg voor schulden of verplichtingen van derden '
    '(9149)': '9149',
    'Door de vennootschap geëndosseerde handelseffecten in omloop '
    '(9150)': '9150',
    'Door de vennootschap getrokken of voor aval getekende handelseffecten '
    '(9151)': '9151',
    'Maximumbedrag ten belope waarvan andere verplichtingen van derden door de '
    'vennootschap zijn gewaarborgd (9153)': '9153',
    # Zakelijke zekerheden
    # ' ()':'',
    # SOCIALE BALANS
    'Gemiddeld aantal werknemers - Voltijds (1001)':'1001',
    'Gemiddeld aantal werknemers - Deeltijds (1002)':'1002',
    'Gemiddeld aantal werknemers - Totaal VTE (1003)':'1003',
    'Aantal daadwerkelijk gepresteerde uren - Voltijds (1011)':'1011',
    'Aantal daadwerkelijk gepresteerde uren - Deeltijds (1012)':'1012',
    'Aantal daadwerkelijk gepresteerde uren - Totaal (1013)':'1013',
    'Personeelskosten - Voltijds (1021)':'1021',
    'Personeelskosten - Deeltijds (1022)':'1022',
    'Personeelskosten - Totaal (1023)':'1023',
    'Bedrag van de voordelen bovenop het loon (1033)':'1033',
    'Aantal werknemers (105)':'105',
    'Overeenkomst voor een onbepaalde tijd':'110',
    'Overeenkomst voor een bepaalde tijd':'111',
    'Overeenkomst voor een duidelijk omschreven werk':'112',
    'Vervangingsovereenkomst':'113',
    'Mannen':'120',
    'Mannen - lager onderwijs':'1200',
    'Mannen - secundair onderwijs':'1201',
    'Mannen - hoger niet-universitair onderwijs':'1202',
    'Mannen - universitair onderwijs':'1203',
    'Vrouwen':'121',
    'Vrouwen - lager onderwijs':'1210',
    'Vrouwen - secundair onderwijs':'1211',
    'Vrouwen - hoger niet-universitair onderwijs':'1212',
    'Vrouwen - universitair onderwijs':'1213',
    'Directiepersoneel':'130',
    'Bedienden':'134',
    'Arbeiders':'132',
    'Andere':'133',
    'Uitzendkrachten -  Gemiddeld aantal tewerkgestelde personen ()':'150',
    'Uitzendkrachten -  Aantal daadwerkelijk gepresteerde uren ()':'151',
    'Uitzendkrachten -  Kosten voor de vennootschap ()':'152',
    }

csv_qual_dict = {
    'Legal Name':'Entity name',
    'Legal Form':'Legal form',
    'Country':'Entity country',
    'City':'Entity city',
    'Postal code':'Entity postal code',
    'Street':'Entity address street',
    'ID':'Entity number',
    'Taal':'Language',
    'Start':'Accounting period start date',
    'End':'Accounting period end date',
    'Approval':'General assembly date',
    }