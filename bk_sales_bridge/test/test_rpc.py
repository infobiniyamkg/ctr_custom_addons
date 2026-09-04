import requests
import random
from datetime import datetime, timedelta


ODOO_URL = "http://localhost:8019/"
ODOO_DB = "marki_test_odoo"
#_08152026"

# TEST ONLY
ODOO_API_KEY = "f5b3c807e9412e0e9cd7ba40d3909654652c10ea"#"81f4144e12ca31ebfe80ce5d204890d0ffdf50f3"

HEADERS = {
    "Authorization": f"bearer {ODOO_API_KEY}",
    "X-Odoo-Database": ODOO_DB,
    "Content-Type": "application/json",
    "User-Agent": "external-pos-load-test/1.0",
}

NUMBER_OF_TRANSACTIONS = 1#800

# Each transaction will contain between these many lines.
MIN_LINES_PER_TRANSACTION = 1
MAX_LINES_PER_TRANSACTION = 5

# USD -> ETB exchange rate range.
#
# Example:
# 1 USD = 155 ETB
# 1 USD = 188 ETB
#
MIN_USD_ETB_RATE = 155.0
MAX_USD_ETB_RATE = 188.0

# Currency stored in bk.sales.transaction
TRANSACTION_CURRENCY = "USD"

# Starting date for generated POS transactions.
START_DATE = datetime(2026, 8, 28, 9, 0, 0)

# Random seed makes the test repeatable.
#
# Change this number if you want a different set of
# transactions/lines.
RANDOM_SEED = 20260828

random.seed(RANDOM_SEED)


# ============================================================
# 3. ACTUAL PRODUCT DATA
# ============================================================
#
# These are products taken from the product list you supplied.
#
# Format:
#
# {
#     "name": Odoo product name,
#     "code": POS/product external code,
#     "price_birr": current/displayed price in Birr
# }
#
# We intentionally keep the exact external name/code for most
# records.
#
# Some codes will later be intentionally modified by the test
# generator to simulate POS code problems.
#
# ============================================================



PRODUCTS = [

    {
        "name": "FS After Eight Classic 12/200gr",
        "code": "5000189363069",
        "price_birr": 676.22,
    },

    {
        "name": "FS After Eight Classic 12/400gr",
        "code": "7613034938459",
        "price_birr": 1571.77,
    },

    {
        "name": "FS After Eight Mix Mini Snack Bag 20/150gr",
        "code": "7613033110504",
        "price_birr": 1161.41,
    },

    {
        "name": "FS Al Suwissria Kunafa Hazelnut - 100gms - 1x48 pcs",
        "code": "7210410864236",
        "price_birr": 600.29,
    },

    {
        "name": "FS Al Suwissria Kunafa Hazelnut - 200gms 1x25pcs",
        "code": "7822454681207",
        "price_birr": 1000.48,
    },

    {
        "name": "FS Al Suwissria Kunafa Pistachio - 100gms - 1x48pcs",
        "code": "7208942368001",
        "price_birr": 600.29,
    },

    {
        "name": "FS Al Suwissria Kunafa Pistachio - 200gms - 1x25pcs",
        "code": "795847982380",
        "price_birr": 1000.48,
    },

    {
        "name": "FS Arabian Camel 100g Dark chocolate with kunafa and pistachio filling 100 grams",
        "code": "6210019198443",
        "price_birr": 890.12,
    },

    {
        "name": "FS Arabian Camel 100g Milk chocolate with kunafa and pistachio filling 100 grams",
        "code": "6210019198412",
        "price_birr": 890.12,
    },

    {
        "name": "FS Arabian Camel 200g Dark chocolate with kunafa and pistachio filling 200 grams",
        "code": "6210019198450",
        "price_birr": 791.22,
    },

    {
        "name": "FS Arabian Camel 200g Milk chocolate with kunafa and pistachio filling 200 grams",
        "code": "6210019198429",
        "price_birr": 1285.74,
    },

    {
        "name": "FS Arabian Camel 50g Dark chocolate with kunafa and pistachio filling 50 grams",
        "code": "6210019198436",
        "price_birr": 395.62,
    },

    {
        "name": "FS Arabian Camel 50g Milk chocolate with kunafa and pistachio filling 50 grams",
        "code": "6210019198405",
        "price_birr": 395.62,
    },

    {
        "name": "FS Arabian Delights Chocodate Assorted 33g Box Packing : 33g x 12 x 6",
        "code": "6291011050717",
        "price_birr": 1962.10,
    },

    {
        "name": "FS Arabian Delights Chocodate Assorted 90g Pouch Packing : 90g x 24",
        "code": "6291011050182",
        "price_birr": 357.67,
    },

    {
        "name": "FS Arabian Delights Chocodate Dark 90g Pouch Packing : 90g x 24",
        "code": "6291011055897",
        "price_birr": 357.67,
    },

    {
        "name": "FS Arabian Delights Chocodate Milk 90g Pouch Packing : 90g x 24",
        "code": "6291011055873",
        "price_birr": 357.67,
    },

    {
        "name": "FS Arabian Delights Value Pack B2G1 3x150g",
        "code": "6291011051059",
        "price_birr": 4342.27,
    },

    {
        "name": "FS BAYARA AJWAH AL MADINAH 400*10",
        "code": "6291106447507",
        "price_birr": 844.38,
    },

    {
        "name": "FS BAYARA ALMONDS SHELLED 400GR",
        "code": "TEST-NOTFOUND-3434410005275",
        "price_birr": 914.89,
    },

    {
        "name": "FS BAYARA APRICO DRIED 400GR",
        "code": "2961570554004",
        "price_birr": 915.29,
    },

    {
        "name": "FS BAYARA CASHEWS KERNEL 400GR",
        "code": "3434410005299",
        "price_birr": 930.53,
    },

    {
        "name": "FS BAYARA CASHEWS ORGANIC 200G",
        "code": "6291107613642",
        "price_birr": 354.80,
    },

    {
        "name": "FS BAYARA DELIXE MIXED NUTS 400GR",
        "code": "3434410005800",
        "price_birr": 534.52,
    },

    {
        "name": "FS BAYARA FIGS DRIED JUMBO 400GR",
        "code": "2961570554042",
        "price_birr": 1259.73,
    },

    {
        "name": "FS BAYARA MABROOM DATES 400G ZIPPER POUCH",
        "code": "6291106441727",
        "price_birr": 711.19,
    },

    {
        "name": "FS BAYARA MIXED DRIED JUMBO 400GR",
        "code": "3434410057762",
        "price_birr": 368.08,
    },

    {
        "name": "FS BAYARA PISTACHIOS KERNEL 400GR",
        "code": "3434410057069",
        "price_birr": 1173.00,
    },

    {
        "name": "FS BAYARA PISTACHIOS W/S 400GR",
        "code": "3434410005794",
        "price_birr": 298.44,
    },

    {
        "name": "FS BAYARA PRUNES DRIED 400GR",
        "code": "2961570554011",
        "price_birr": 353.74,
    },

    {
        "name": "FS BAYARA RAISINS GOLDEN 400GR",
        "code": "3434410057809",
        "price_birr": 803.44,
    },

    {
        "name": "FS BAYARA RASISINS BROWN ORGANIC 200G",
        "code": "6291107613628",
        "price_birr": 192.87,
    },

    {
        "name": "FS BAYARA SAFAWI DATES 400G ZIPPER POUCH",
        "code": "6291106441710",
        "price_birr": 743.56,
    },

    {
        "name": "FS BAYARA SAGAI DATES 400G*10 ZIPPER POUNCH",
        "code": "6291106441758",
        "price_birr": 932.32,
    },

    {
        "name": "FS BAYARA WALNUTS HALVES 400GR",
        "code": "3434410057823",
        "price_birr": 596.82,
    },

    {
        "name": "FS BAYARA WALNUTS ORGANIC 200G",
        "code": "6291107613666",
        "price_birr": 395.77,
    },

    {
        "name": "FS BOUNTY Milk Single 57g 12x24",
        "code": "5000159558280",
        "price_birr": 228.97,
    },

    {
        "name": "FS Barebells Bar Caramel Choco 12/55gr",
        "code": "7340001804546",
        "price_birr": 524.54,
    },

    {
        "name": "FS Barebells Bar Marshmallow 12/55gr",
        "code": "7340001804447",
        "price_birr": 523.00,
    },

    {
        "name": "FS Be-Kind Bar Caramel Almond and Sea Salt 72/40gr",
        "code": "TEST-NOTFOUND-602652257780",
        "price_birr": 169.55,
    },

    {
        "name": "FS Be-Kind Bar Dark Chocolate and Sea salt 72/40g",
        "code": "5000159528481",
        "price_birr": 168.47,
    },

    {
        "name": "FS Be-Kind Protein Bar Dark Chocolate 72/50g",
        "code": "5000159527118",
        "price_birr": 181.18,
    },

    {
        "name": "FS Bounty Minis Bag 24/333g",
        "code": "5000159557597",
        "price_birr": 1074.28,
    },

    {
        "name": "FS Bounty Minis Pouch 10/220g",
        "code": "5000159557528",
        "price_birr": 745.95,
    },

    {
        "name": "FS Bounty Mono Pouch 15/500g",
        "code": "5000159558082",
        "price_birr": 1480.96,
    },

    {
        "name": "FS Butlers Assorted Mini Chocolate Bag 430G*18",
        "code": "5099466166028",
        "price_birr": 1497.30,
    },

    {
        "name": "FS Butlers Choco MlkTrufle Twist wrap 300g",
        "code": "5099466213111",
        "price_birr": 579.87,
    },

    {
        "name": "FS Butlers Mini Dark Chocolate Bag 430G",
        "code": "5099466166035",
        "price_birr": 884.34,
    },

    {
        "name": "FS CADBURY FAMILY MILK 300G*13",
        "code": "7622300844486",
        "price_birr": 1033.06,
    },

    {
        "name": "FS CHOCOLADE MARABOU MILK ROLL",
        "code": "7622210255136",
        "price_birr": 90.75,
    },

    {
        "name": "FS CHOCOLATE MARABOU MILK 74*2",
        "code": "7310510002122",
        "price_birr": 397.62,
    },

    {
        "name": "FS CHUPA CHPUS COOLFRIEND 192G",
        "code": "8410031972382",
        "price_birr": 2092.90,
    },

    {
        "name": "FS CHUPA CHUPS BAG BEST OF 24*300",
        "code": "8410031977646",
        "price_birr": 721.80,
    },

    {
        "name": "FS CHUPA CHUPS THE BEST 300G*24",
        "code": "8410031970821",
        "price_birr": 361.48,
    },

    {
        "name": "FS Cadbury Dairy Milk 180Gm Tablet*17",
        "code": "7622201783365",
        "price_birr": 539.37,
    },

    {
        "name": "FS Cadbury Dairy Milk CaraChunks300Gm Pouch",
        "code": "7622201789275",
        "price_birr": 474.74,
    },

    {
        "name": "FS Cadbury Dairy Milk Caramel 180g*17",
        "code": "680121-770433",
        "price_birr": 557.66,
    },

    {
        "name": "FS Cadbury Dairy Milk Chocolate Pouch 498G*14",
        "code": "7622201752767",
        "price_birr": 1353.20,
    },

    {
        "name": "FS Cadbury Dairy Milk Chunk Pouch 300gm",
        "code": "7622201788735",
        "price_birr": 771.45,
    },

    {
        "name": "FS Cadbury Dairy Milk Fruit and Nut 12/280gr",
        "code": "7622202272875",
        "price_birr": 1091.41,
    },

    {
        "name": "FS Cadbury Dairy Milk Fruit and Nut Tablet 12/300gr",
        "code": "7622300844479",
        "price_birr": 1005.93,
    },

    {
        "name": "FS Cadbury Dairy Milk Fruit&Nut Tablet 12/300gm",
        "code": "7622201783297",
        "price_birr": 904.59,
    },

    {
        "name": "FS Cadbury Dairy Milk Fruit&Nut Tablet 15/180gm",
        "code": "7622201783297-",
        "price_birr": 711.37,
    },

    {
        "name": "FS Cadbury Dairy Milk Whole Nut 45gm",
        "code": "96133262",
        "price_birr": 71.66,
    },

    {
        "name": "FS Cadbury Dairy Milk Whole Nut Pouch 120GM",
        "code": "7622201788759",
        "price_birr": 484.28,
    },

    {
        "name": "FS Cadbury Dairy Milk Whole nut 300Gm Pouch",
        "code": "TEST-NOTFOUND-7622201788087",
        "price_birr": 785.42,
    },

    {
        "name": "FS Cadbury Dairy Milk WholeNut 180Gm Tablet*14",
        "code": "7622201783396",
        "price_birr": 555.07,
    },

    {
        "name": "FS Cadbury Dairy Milk fruit&nut Bar 49gm",
        "code": "50312610",
        "price_birr": 71.11,
    },

    {
        "name": "FS Cadbury Dairy Whole Nut Bar 300gm*12",
        "code": "7622210239570",
        "price_birr": 1115.60,
    },

    {
        "name": "FS Cadbury DairyMilk Chunk 120g Bag*20",
        "code": "7622201788520",
        "price_birr": 461.72,
    },

    {
        "name": "FS Cadbury DairyMilk Standrd Bars 45gm",
        "code": "7622300743574",
        "price_birr": 100.09,
    },

    {
        "name": "FS Cadbury Heroes Pouch 275gm",
        "code": "7622201788650",
        "price_birr": 771.45,
    },

    {
        "name": "FS Cadbury Milk Oreo 13/300gr",
        "code": "7622210615176",
        "price_birr": 1133.11,
    },

    {
        "name": "FS Cadbury Nibbly Finger Bag 320gm",
        "code": "7622210598042",
        "price_birr": 636.16,
    },

    {
        "name": "FS Cadbury Roundies Pouch 360gm",
        "code": "7622210598066",
        "price_birr": 627.13,
    },

    {
        "name": "FS Celebration sparkling 320g",
        "code": "5000159432504",
        "price_birr": 714.90,
    },

    {
        "name": "FS Celebrations Bottle 12/320g-296g",
        "code": "5000159565134",
        "price_birr": 1557.76,
    },

    {
        "name": "FS Celebrations Pouch 10/240g",
        "code": "5000159440622",
        "price_birr": 1115.49,
    },

    {
        "name": "FS Celebrations Pouch 15/450g",
        "code": "5000159415316",
        "price_birr": 2943.33,
    },

    {
        "name": "FS Celebrations Tin 10/165g",
        "code": "5000159527712",
        "price_birr": 1494.35,
    },

    {
        "name": "FS Chocodate Assorted 12x220g Pouch",
        "code": "6291011054562",
        "price_birr": 896.26,
    },

    {
        "name": "FS Chocodate Dark 12x220g Pouch",
        "code": "6291011051684",
        "price_birr": 1276.42,
    },

    {
        "name": "FS Chocodate Exclusive Real Assorted 100g Pouch V2 Packing : 100g x 24",
        "code": "6291011051974",
        "price_birr": 408.77,
    },

    {
        "name": "FS Chocodate Exclusive Real Dark 100g Pouch V2 Packing : 100g x 24",
        "code": "6291011053954",
        "price_birr": 408.77,
    },

    {
        "name": "FS Chocodate Exclusive Real Milk 100g Pouch V2 Packing : 100g x 24",
        "code": "6291011053947",
        "price_birr": 408.77,
    },

    {
        "name": "FS Chocodate Matcha 12x220g Pouch",
        "code": "TEST-NOTFOUND-6291011065711",
        "price_birr": 984.93,
    },

    {
        "name": "FS Chocodate Milk 12x220g Pouch",
        "code": "6291011051677",
        "price_birr": 941.16,
    },

    {
        "name": "FS Chocodate Pistachio Kunafa 12x220g Pouch",
        "code": "6291011064295",
        "price_birr": 1122.15,
    },

    {
        "name": "FS Chocodate Pistachio Kunafa 24x100g pouch",
        "code": "6291011064264",
        "price_birr": 1053.31,
    },

    {
        "name": "FS Chocodate with Matcha Pouch 24 x 100g Packing : 100gX24",
        "code": "6291011065704",
        "price_birr": 445.56,
    },

    {
        "name": "FS Chupa Chups Colourkit 4/48x12gr",
        "code": "8410031977318",
        "price_birr": 712.84,
    },

    {
        "name": "FS Chupa Chups Crazy Plane 12GM",
        "code": "8410031946956",
        "price_birr": 478.37,
    },

    {
        "name": "SM 107 Anniversary Nicaragua Robusto 20s",
        "code": "7465603135741",
        "price_birr": 10801.88,
    },

    {
        "name": "SM 115 Anniversary Grand Toro 20s",
        "code": "7465603128392",
        "price_birr": 15014.40,
    },

    {
        "name": "SM 1880 Claro Robusto",
        "code": "7501609514330",
        "price_birr": 13402.56,
    },

    {
        "name": "SM 1880 Double Claro Double Robusto",
        "code": "7501609514194",
        "price_birr": 10089.93,
    },

    {
        "name": "SM 1880 Double Maduro Robusto",
        "code": "7501609515290",
        "price_birr": 13946.13,
    },

    {
        "name": "SM 1880 Maduro Robusto",
        "code": "7501609515672",
        "price_birr": 13946.13,
    },

    {
        "name": "SM 1880 Oscuro Double Robusto",
        "code": "7501609514132",
        "price_birr": 15757.07,
    },

    {
        "name": "SM 1880 Rosado Robusto",
        "code": "7501609515276",
        "price_birr": 13946.13,
    },

    {
        "name": "SM AGIO CIG MEHARIS JAVA 10S",
        "code": "8710622514800",
        "price_birr": 167.65,
    },

    {
        "name": "SM AGIO CIGAR MEHARIS RED ORIE",
        "code": "8710622517801",
        "price_birr": 167.65,
    },

    {
        "name": "SM AJ Fernandez Enclave habano toro",
        "code": "851350001458",
        "price_birr": 25320.41,
    },

    {
        "name": "SM AJ Fernandez dias de goloria robusto",
        "code": "7426824785115",
        "price_birr": 32866.21,
    },

    {
        "name": "SM AJ fernandez blend 15 toro",
        "code": "7426824785412",
        "price_birr": 9494.85,
    },

    {
        "name": "SM AJ fernandez new world dorado gordito",
        "code": "TEST-NOTFOUND-7426824785795",
        "price_birr": 22397.71,
    },

    {
        "name": "SM AJF BELLAS ARTES MADURO ROBUSTO 20S",
        "code": "7429457791775",
        "price_birr": 30456.02,
    },

    {
        "name": "SM AJF CIGAR SAMPLE TORO 5S",
        "code": "5404021001926",
        "price_birr": 6817.69,
    },

    {
        "name": "SM AJF LAST CALL HABONO CORICAS 25S",
        "code": "7429457990994",
        "price_birr": 22150.30,
    },

    {
        "name": "SM AJF NEW WORLD OSCURO NAVEGANTE ROBUSTO 21S",
        "code": "851350000987",
        "price_birr": 19280.43,
    },

    {
        "name": "SM AJF NEW WORLD SAMPLER 5S",
        "code": "7426824785832",
        "price_birr": 4869.45,
    },

    {
        "name": "SM AJF PREMIUM SAMPLER ROBUSTO 5S",
        "code": "851350000116",
        "price_birr": 6224.71,
    },

    {
        "name": "SM AL FAKHER 8K",
        "code": "5061021229028-5061016929605",
        "price_birr": 13430.98,
    },

    {
        "name": "SM AL FAKHER HOOKA MOLASSES",
        "code": "6291108160015",
        "price_birr": 5783.27,
    },

    {
        "name": "SM ALISHA FANTASY ROYAL JELIU*50",
        "code": "4719579947215",
        "price_birr": 1750.98,
    },

    {
        "name": "SM ALISHAN ACE HARD*50",
        "code": "4719579946829",
        "price_birr": 197.27,
    },

    {
        "name": "SM ALISHAN BAODAO TIN PACK*25",
        "code": "4719579946461",
        "price_birr": 1242.25,
    },

    {
        "name": "SM ALISHAN JING DIAN LAN*50",
        "code": "4719579946317",
        "price_birr": 1313.23,
    },

    {
        "name": "SM ALISHAN KAI YUAN HARD*50",
        "code": "4719579940018",
        "price_birr": 1472.95,
    },

    {
        "name": "SM ALISHAN SLIM BLUE BERRY*50",
        "code": "4719579948328",
        "price_birr": 554.58,
    },

    {
        "name": "SM ALISHAN TIAN YAN HARD*50",
        "code": "4719579946348",
        "price_birr": 1426.82,
    },

    {
        "name": "SM ASHIMA FILTER HARD PACK*50",
        "code": "6901028315289",
        "price_birr": 674.79,
    },

    {
        "name": "SM ASHIMA GOLD1*50",
        "code": "4897028980997",
        "price_birr": 787.81,
    },

    {
        "name": "SM ASHIMA INTERNATIONA RED*50",
        "code": "6901028053020",
        "price_birr": 766.05,
    },

    {
        "name": "SM ASHIMA SUPER SLIMS LOVE*50",
        "code": "4897028984063",
        "price_birr": 753.10,
    },

    {
        "name": "SM ASHINA INTER.GOLD HP*50",
        "code": "TEST-NOTFOUND-6901028054836",
        "price_birr": 440.13,
    },

    {
        "name": "SM Aging room quattro maestro",
        "code": "811438024830",
        "price_birr": 33111.31,
    },

    {
        "name": "SM Amber Leaf INT 24/5x50gr TTT",
        "code": "5000143555097",
        "price_birr": 849.86,
    },

    {
        "name": "SM Aristocrat Natural(Glass Tube)",
        "code": "311043/210044",
        "price_birr": 2350.44,
    },

    {
        "name": "SM B&H SILVER*50",
        "code": "4031300126578",
        "price_birr": 847.78,
    },

    {
        "name": "SM BAISH HARMONIZTION",
        "code": "6901028197595",
        "price_birr": 4801.90,
    },

    {
        "name": "SM BALMORAL CIG COLLECTION TUB",
        "code": "8710622494621",
        "price_birr": 3188.05,
    },

    {
        "name": "SM BALMORAL CIG CORONA TUBE 5S",
        "code": "8710622792468",
        "price_birr": 4832.85,
    },

    {
        "name": "SM BENSON AND HEDGES INT SF KSF 6M/600*10",
        "code": "8888075054133",
        "price_birr": 6705.44,
    },

    {
        "name": "SM BENSON&HEDGES SPECIAL FILTER",
        "code": "5000219020207",
        "price_birr": 922.70,
    },

    {
        "name": "SM BH Sampler Box Red",
        "code": "076622258105",
        "price_birr": 804.97,
    },

    {
        "name": "SM BLACK STONE VANILLA CIG 20S",
        "code": "025900215279",
        "price_birr": 136.46,
    },

    {
        "name": "SM BUNDLE SELE.BY CUSANO SHORT",
        "code": "7623500246476",
        "price_birr": 148.21,
    },

    {
        "name": "SM BUNDLE SELECTION BY CUSANO",
        "code": "7623500545920",
        "price_birr": 140.13,
    },

    {
        "name": "SM Backwoods Honey 40/8x5",
        "code": "71610993990",
        "price_birr": 366.79,
    },

    {
        "name": "SM Backwoods Honey Berry 40/8x5",
        "code": "71610994003",
        "price_birr": 363.39,
    },

    {
        "name": "SM Backwoods Sweet Aromatic 40/8x5",
        "code": "71610300415",
        "price_birr": 383.99,
    },

    {
        "name": "SM Backwoods Vanilla 40/BxS 8000 Sticks = 200 Cellophane = 5 Case",
        "code": "071610299788",
        "price_birr": 480.18,
    },

    {
        "name": "SM Benson & Hedges INT Blue Gold 10M/200",
        "code": "8888075062367",
        "price_birr": 2181.49,
    },

    {
        "name": "SM Benson & Hedges INT Blue Gold 6M/400",
        "code": "8888075067232",
        "price_birr": 4314.12,
    },

    {
        "name": "SM Benson & Hedges INT SF KSF 10M/200",
        "code": "TEST-NOTFOUND-8888075053853",
        "price_birr": 2542.89,
    },

    {
        "name": "SM Benson & Hedges INT SF KSF 6M/400",
        "code": "8888075054119",
        "price_birr": 4605.29,
    },

    {
        "name": "SM CAFE CREME RED",
        "code": "8720400481941",
        "price_birr": 178.66,
    },

    {
        "name": "SM CAO CIGAR CHAPION SAMPLER",
        "code": "689674099666",
        "price_birr": 6823.23,
    },

    {
        "name": "SM CAO CIGAR PILON ROBUSTO 20S",
        "code": "689674077855",
        "price_birr": 11111.43,
    },

    {
        "name": "SM CAO CIGAR WORLD SAMPLER5",
        "code": "689674127482",
        "price_birr": 3119.00,
    },

    {
        "name": "SM CAPTAIN BIANCK CLASSIC*30",
        "code": "7460402100167",
        "price_birr": 2110.11,
    },

    {
        "name": "SM CAPTAIN BLACK CHERISE*30",
        "code": "7460402100129",
        "price_birr": 1728.52,
    },

    {
        "name": "SM CAPTAIN BLACK GRAPE*30",
        "code": "7460402100204",
        "price_birr": 803.88,
    },

    {
        "name": "SM CAPTAIN MORGAN DARK CREMA*30",
        "code": "7460402100143",
        "price_birr": 944.87,
    },

    {
        "name": "SM CHUNGHWA 5000*50",
        "code": "6901028073349/6901028075572",
        "price_birr": 235.13,
    },

    {
        "name": "SM CHUNGHWA FILTER RED 20'S ENG Small HW",
        "code": "6901028076623",
        "price_birr": 2604.39,
    },

    {
        "name": "SM CHUNGHWA HARD*50",
        "code": "6901028075572/73349",
        "price_birr": 1614.29,
    },

    {
        "name": "SM CHUNGHWA SOFT 200S BIG HW",
        "code": "6901028074308",
        "price_birr": 9457.81,
    },

    {
        "name": "SM CHUNGHWA SUPER SLIM*50",
        "code": "6901028074148/6901028212465",
        "price_birr": 6331.87,
    },

    {
        "name": "SM COHIBA INT CLUB 20/5*20",
        "code": "8500001541233",
        "price_birr": 5578.42,
    },

    {
        "name": "SM COHIBA INT MINI 20/5*20",
        "code": "8500001541226-8500001544104",
        "price_birr": 1891.19,
    },

    {
        "name": "SM COHIBA INT MINI WHITE 20/5*20",
        "code": "8500001543565",
        "price_birr": 3554.51,
    },

    {
        "name": "SM Camel INT Activate Double 10M/200",
        "code": "4032900112718",
        "price_birr": 2254.14,
    },

    {
        "name": "SM Camel INT Blue 10M/200 TTT*50",
        "code": "4032900112701",
        "price_birr": 2200.22,
    },

    {
        "name": "SM Camel INT Blue 12M/400 TTT",
        "code": "TEST-NOTFOUND-4032900113234",
        "price_birr": 3754.20,
    },

    {
        "name": "SM Camel INT Blue 6M/600 TTT*10",
        "code": "4032900113241-4032900113258",
        "price_birr": 5805.16,
    },

    {
        "name": "SM Camel INT Yellow 12M/400 TTT*30",
        "code": "4032900113227",
        "price_birr": 3770.91,
    },

    {
        "name": "SM Camel INT Yellow Filter 10M/200 TTT*50",
        "code": "4032900112695",
        "price_birr": 2189.32,
    },

    {
        "name": "SM Camel INT Yellow Filter 6M/600 TTT",
        "code": "0325-3258",
        "price_birr": 3674.18,
    },

    {
        "name": "SM Camel INT yellow filter 6M /600*10",
        "code": "4032900113258",
        "price_birr": 6091.68,
    },

    {
        "name": "SM Cameo Tins(Cigarillos)",
        "code": "076622200005",
        "price_birr": 572.29,
    },

    {
        "name": "CO  P/WHITE B SPRAY-ICYMINT8 SML  PEARLIE",
        "code": "071031251105",
        "price_birr": 559.70,
    },

    {
        "name": "CO  Parfums de Marly Pegasus",
        "code": "3700578502919",
        "price_birr": 13101.59,
    },

    {
        "name": "CO  SEZAN Mathael EDP",
        "code": "6294831648607",
        "price_birr": 2513.68,
    },

    {
        "name": "CO  SUPREMACY NOT ONLY INTENSE 150ML EDP",
        "code": "6290171072775",
        "price_birr": 3174.30,
    },

    {
        "name": "CO  montale Bubble Forever 100ML",
        "code": "3760260458894",
        "price_birr": 9310.12,
    },

    {
        "name": "CO 12 PCS MAKEUP BRUSH SET",
        "code": "952654126695",
        "price_birr": 5260.59,
    },

    {
        "name": "CO 12 PCS NAIL POLISH SET MIX",
        "code": "NB0086",
        "price_birr": 1202.60,
    },

    {
        "name": "CO 12 PCS NAIL POLISH STAR BEJA  MIX",
        "code": "NB0085",
        "price_birr": 497.04,
    },

    {
        "name": "CO 2 IN 1 LIPGLOSS 1299 24 PCS L  CHEAR",
        "code": "DQ1273/972533960790",
        "price_birr": 103.22,
    },

    {
        "name": "CO 2 IN 1 LIPGLOSS 2225 24 PCS",
        "code": "6923055529309",
        "price_birr": 206.67,
    },

    {
        "name": "CO 2 IN 1 PINK KEY CLIPPER & SCISSORS   PT17",
        "code": "921099219859/6921099219835",
        "price_birr": 150.34,
    },

    {
        "name": "CO 212  VIP ROSE 80ML",
        "code": "8411061777176",
        "price_birr": 8896.73,
    },

    {
        "name": "CO 238  12 PCS MAKEUP BRUSH SET",
        "code": "915868980088",
        "price_birr": 3307.72,
    },

    {
        "name": "CO 24HR MOIST SOFT CREAM 200ML 2+  JOHNSON & J",
        "code": "TEST-NOTFOUND-3574601298830",
        "price_birr": 1259.09,
    },

    {
        "name": "CO 281  5 PCS MAKEUP BRUSH SET",
        "code": "6926641002811",
        "price_birr": 210.12,
    },

    {
        "name": "CO 2LADY SPEED ST O/BLOSSOM 20%    MENNEN",
        "code": "6281001813828",
        "price_birr": 1415.69,
    },

    {
        "name": "CO 2PC ORGANIC CARE KIDS ASSORT  NATURES OR",
        "code": "8310692214817",
        "price_birr": 1204.45,
    },

    {
        "name": "CO 3249 ( 2 IN 1 ) EYE LINE MASCARA",
        "code": "923055526698",
        "price_birr": 275.34,
    },

    {
        "name": "CO 3274 ( 2 IN 1 ) EYE LINE MASCARA 12 PCS",
        "code": "923055530909",
        "price_birr": 275.65,
    },

    {
        "name": "CO 33021 LIP LINER 12 EACH",
        "code": "6982022000296",
        "price_birr": 479.58,
    },

    {
        "name": "CO 4076 L'CHEAR CONCEALER 24 HR LONGLASTING 24 PCS",
        "code": "923055525707",
        "price_birr": 125.18,
    },

    {
        "name": "CO 6 PCS NAIL POLISH SET  MIX",
        "code": "NB0084",
        "price_birr": 660.32,
    },

    {
        "name": "CO 6019 : 10 BOX     6027 : 10 BOX   EYE LASH",
        "code": "6922030060271",
        "price_birr": 1202.07,
    },

    {
        "name": "CO 7012 EYE PENCIL",
        "code": "920982846134",
        "price_birr": 296.03,
    },

    {
        "name": "CO 7070 BEAUTY MAKE UP KIT 24 PCS",
        "code": "923055532019",
        "price_birr": 275.41,
    },

    {
        "name": "CO 7169 LIP LINER 12 EACH",
        "code": "972533960790",
        "price_birr": 479.95,
    },

    {
        "name": "CO 9 AM EDP 100ML",
        "code": "6290171002345",
        "price_birr": 2935.72,
    },

    {
        "name": "CO ?Faiz Niche Zoe Extrait De Parfum 100 ML",
        "code": "0653871094687",
        "price_birr": 9309.43,
    },

    {
        "name": "CO A.DI PARMA ARANCIA DI CAPRI Edt 150ml",
        "code": "8028713570025",
        "price_birr": 3307.62,
    },

    {
        "name": "CO A.DI PARMA BERGAMOTTO Edt 150ml",
        "code": "8028713570100",
        "price_birr": 3375.75,
    },

    {
        "name": "CO A.DI PARMA COLONIA C.L.U.B. Edc 180ml",
        "code": "8028713150036",
        "price_birr": 3748.59,
    },

    {
        "name": "CO A.DI PARMA SIGNATURE SAKURA Edp 100ml",
        "code": "8028713810312",
        "price_birr": 3167.48,
    },

    {
        "name": "CO A?UAFRESH T/BRUSHFLEX SOFT",
        "code": "680569954184",
        "price_birr": 1735.10,
    },

    {
        "name": "CO AB BLUE SEDUCTION W 100ML EDT",
        "code": "TEST-NOTFOUND-8411061784273",
        "price_birr": 3062.11,
    },

    {
        "name": "CO AB KING OF SEDUCTION ABSOLUTE M 100ML EDT",
        "code": "8411061813973",
        "price_birr": 1071.15,
    },

    {
        "name": "CO AB KING OF SEDUCTION M 100ML EDT",
        "code": "8411061082935",
        "price_birr": 2621.41,
    },

    {
        "name": "CO AB POWER OF SEDUCTION M 100ML EDT",
        "code": "8411061913024",
        "price_birr": 1160.41,
    },

    {
        "name": "CO AB POWER OF SEDUCTION M 200ML EDT",
        "code": "8411061945568",
        "price_birr": 1473.85,
    },

    {
        "name": "CO AB QUEEN OF SEDUCTION LIVELY MUSE W 80ML EDT",
        "code": "8411061011195",
        "price_birr": 1210.29,
    },

    {
        "name": "CO AB THE GOLDEN SECRET M 100ML EDT",
        "code": "8411061722756",
        "price_birr": 2715.43,
    },

    {
        "name": "CO AB THE GOLDEN SECRET M 100ML EDT TST",
        "code": "8411061080740",
        "price_birr": 375.40,
    },

    {
        "name": "CO AB THE GOLDEN SECRET M 200ML EDT",
        "code": "8411061791691",
        "price_birr": 1160.41,
    },

    {
        "name": "CO AB THE SECRET TEMPTATION M 100ML EDT",
        "code": "8411061860502",
        "price_birr": 1169.21,
    },

    {
        "name": "CO ABSOLUTE APHRODISIAC EDP 90ML",
        "code": "3701415901346",
        "price_birr": 15141.50,
    },

    {
        "name": "CO ACCEESSORY STAND    (",
        "code": "DISPLAY",
        "price_birr": 896.34,
    },

    {
        "name": "CO ACQUE DI PARMA COLONIA INT1",
        "code": "8028713210020",
        "price_birr": 4410.52,
    },

    {
        "name": "CO ADIDAS SHOWER GEL 400M",
        "code": "3607340717185",
        "price_birr": 465.30,
    },

    {
        "name": "CO AHMAD TEA BEAUTY TEA B 20X1.5  AHMAD TEA",
        "code": "054881020398",
        "price_birr": 884.68,
    },

    {
        "name": "CO AHMAD TEA DIGEST TEA B 20X2G  AHMAD TEA",
        "code": "054881020374",
        "price_birr": 884.68,
    },

    {
        "name": "CO AHMAD TEA IMMUNE TEA 20X1.5G  AHMAD TEA",
        "code": "054881020343",
        "price_birr": 804.80,
    },

    {
        "name": "CO AHMAD TEA SUM GRN TEA 20X1.5G  AHMAD TEA",
        "code": "054881020350",
        "price_birr": 709.23,
    },

    {
        "name": "CO ALIEN GODDESS MUGLER EDP 90ml  ALIEN",
        "code": "3614273673402",
        "price_birr": 15113.90,
    },

    {
        "name": "CO ALL SAINTS RAVAGED ROSE",
        "code": "810023677246",
        "price_birr": 12332.39,
    },

    {
        "name": "CO ALL SAINTS SHOREDITCH LEATHER",
        "code": "TEST-NOTFOUND-810023677222",
        "price_birr": 12327.65,
    },

    {
        "name": "CO ALL SAINTS SUNSET RIOT INTENSE",
        "code": "810023677239",
        "price_birr": 12337.14,
    },

    {
        "name": "CO ALLURE CHANNEL",
        "code": "3145891125306",
        "price_birr": 11844.17,
    },

    {
        "name": "CO ALM VIRGIN OLIVE OIL 250ML  AL-MARAI",
        "code": "6281007055741",
        "price_birr": 879.66,
    },

    {
        "name": "CO ALOKOZAY BLACK TEA BAG 200s  ALOKOZAY",
        "code": "6290360351513",
        "price_birr": 1058.17,
    },

    {
        "name": "CO ALW ULT LW 24x7SP FC01 DIAMOND",
        "code": "8001090921345",
        "price_birr": 857.79,
    },

    {
        "name": "CO ALWAYS COMF AND PRO FRESH 20  ALWAYS LINE",
        "code": "8001090542403",
        "price_birr": 1108.96,
    },

    {
        "name": "CO ALWAYS MULTIFORMM 20S  ALWAYS LINE",
        "code": "8001090542625",
        "price_birr": 741.92,
    },

    {
        "name": "CO AMORE CAFFÈ 120ML",
        "code": "3760265194582",
        "price_birr": 11248.95,
    },

    {
        "name": "CO AMOUAGE GUIDANCE W EDP 100ML  AMOUAGE",
        "code": "701666410454",
        "price_birr": 45094.61,
    },

    {
        "name": "CO AMOUAGE INTERLUDE 53 M EDP 100ML  AMOUAGE",
        "code": "701666410737",
        "price_birr": 25768.18,
    },

    {
        "name": "CO AMOUAGE INTERLUDE BLACK IRIS NEW PAKING M EDP 100ML  AMOUAGE",
        "code": "701666410218",
        "price_birr": 29414.81,
    },

    {
        "name": "CO AMOUAGE OPUS V WOODS SYMPHONY EDP 100ML  AMOUAGE",
        "code": "701666410515",
        "price_birr": 29682.60,
    },

    {
        "name": "CO AMOUAGE OPUS XIV ROYAL TOBACCO EDP 100ML  AMOUAGE",
        "code": "701666410577",
        "price_birr": 29570.35,
    },

    {
        "name": "CO AMOUAGE OPUS XV KING BLEU M EDP 100ml  AMOUAGE",
        "code": "701666410584",
        "price_birr": 41873.30,
    },

    {
        "name": "CO AMOUAGE PURPOSE EDP 100ML  AMOUAGE",
        "code": "701666410430",
        "price_birr": 42678.58,
    },

    {
        "name": "CO AMOUAGE REFLECTION 45 M EDP 100ML  AMOUAGE",
        "code": "701666410706",
        "price_birr": 45899.84,
    },

    {
        "name": "CO AMOUAGE SEARCH EDP 100ML  AMOUAGE",
        "code": "701666410447",
        "price_birr": 31554.22,
    },

    {
        "name": "CO AOUD VANILLE 120 ml",
        "code": "3760265190287",
        "price_birr": 12872.54,
    },

    {
        "name": "CO ARMANI AQUA G10 100ML",
        "code": "3360372058878",
        "price_birr": 10905.47,
    },

    {
        "name": "CO ARMANI BECAUSE ITS YOU (W) EDP 100ml  TOMFORD",
        "code": "TEST-NOTFOUND-3605522041486",
        "price_birr": 10935.05,
    },

    {
        "name": "CO ARMANI CODE (M) EDT 125ml  TOMFORD",
        "code": "3614273604932",
        "price_birr": 11887.93,
    },

    {
        "name": "CO ARMANI SI (W) EDP 100ML",
        "code": "3605521816658",
        "price_birr": 14991.01,
    },

    {
        "name": "CO ARMANI STRONGER WITH U ABSOLUTELY EDP 100ML  TOMFORD",
        "code": "3614273336383",
        "price_birr": 12663.38,
    },

    {
        "name": "CO ARMANI STRONGER WITH U INTENSELY (M) EDP 100ml",
        "code": "3614272225718",
        "price_birr": 11559.87,
    },

    {
        "name": "CO ATELIER COLOGNE SANTAL CARMIN ABSOLUE EDP 200ml  ATELIER",
        "code": "3614273638722",
        "price_birr": 23508.17,
    },

    {
        "name": "CO ATELIER CUIR SACRE DES ORS (U) EDP 100ml  TOMFORD",
        "code": "3760027140031",
        "price_birr": 17921.31,
    },

    {
        "name": "CO SMART WATCH WS-23  TOMFORD",
        "code": "WS-23",
        "price_birr": 3150.26,
    },

    {
        "name": "EL 2693 JRM-SL352 Cable",
        "code": "6956116774691",
        "price_birr": 343.73,
    },

    {
        "name": "EL 3425 JRS-1230G4 3IN1 BLK CBL",
        "code": "6941237145925",
        "price_birr": 881.36,
    },

    {
        "name": "EL 3425 JRS-1230G4 3IN1 BLK CBL-1",
        "code": "6941237145925-",
        "price_birr": 542.38,
    },

    {
        "name": "EL 3425 JRS-1230G4 3IN1 GRN CBL",
        "code": "6941237145949",
        "price_birr": 881.36,
    },

    {
        "name": "EL 3425 JRS-1230G4 3IN1 GRN CBL-1",
        "code": "6941237145949-",
        "price_birr": 881.36,
    },

    {
        "name": "EL 3516-SYA02 LIGHTING AUX 1M",
        "code": "6941237136725",
        "price_birr": 1518.15,
    },

    {
        "name": "EL 3533-JOYROOM M13 1M CABLE PINK",
        "code": "6941237170453",
        "price_birr": 482.55,
    },

    {
        "name": "EL 3533-JOYROOM M13 1M CABLE PURPLE(3AM)",
        "code": "6941237170408",
        "price_birr": 482.55,
    },

    {
        "name": "EL 3534 JR-M13 TC 1M PINK CABLE",
        "code": "6941237170378",
        "price_birr": 482.55,
    },

    {
        "name": "EL 3534 JR-M13 TC 1M PURPLE CABLE",
        "code": "6941237170408-",
        "price_birr": 482.55,
    },

    {
        "name": "EL 3727-JR-QP193 22.5W 30000mAh PB",
        "code": "6941237185136",
        "price_birr": 3980.04,
    },

    {
        "name": "EL 3732-JR-FT5 SMART WATCH BLACK",
        "code": "6956116717872",
        "price_birr": 6043.17,
    },

    {
        "name": "EL 3732-JR-FT5 SMART WATCH BLACK-1",
        "code": "TEST-NOTFOUND-6956116717872-",
        "price_birr": 6557.32,
    },

    {
        "name": "EL 3738 JRS-CL020A9 1M TC-IP BLACK CABLE",
        "code": "6956116735425",
        "price_birr": 550.85,
    },

    {
        "name": "EL 3738 JRS-CL020A9 1M TC-IP BLACK CABLE-1",
        "code": "6956116735425-",
        "price_birr": 550.85,
    },

    {
        "name": "EL 3738 JRS-CL020A9 1M TC-IP WHITE CABLE",
        "code": "6956116735418",
        "price_birr": 550.85,
    },

    {
        "name": "EL 3738 JRS-CL020A9 1M TC-IP WHITE CABLE-1",
        "code": "6956116735418-",
        "price_birr": 550.85,
    },

    {
        "name": "EL 3739 JRS-UL012A9 BK 1M USB-IP",
        "code": "6956116735043",
        "price_birr": 330.51,
    },

    {
        "name": "EL 3739 JRS-UL012A9 WT 1M USB-IP",
        "code": "6956116735098",
        "price_birr": 330.53,
    },

    {
        "name": "EL 3741 JR-Y105 AUDIO CONVERTER",
        "code": "6941237176950",
        "price_birr": 3305.09,
    },

    {
        "name": "EL 3746 JRS-1224K7 1.2M USB-IP",
        "code": "6941237187604",
        "price_birr": 965.08,
    },

    {
        "name": "EL 3757 JR-FC2 CLASSIC SM WATCH",
        "code": "6956116743833",
        "price_birr": 7932.24,
    },

    {
        "name": "EL 3757 JR-FC2 CLASSIC SM WATCH GOLD",
        "code": "6941237129840",
        "price_birr": 4881.38,
    },

    {
        "name": "EL 3757 JR-FC2 CLASSIC SM WATCH GOLD-1",
        "code": "6941237129840-",
        "price_birr": 7932.24,
    },

    {
        "name": "EL 3767 JR-FT6 SMART WATCH",
        "code": "6956116756291",
        "price_birr": 7932.24,
    },

    {
        "name": "EL 3782 JRS-CC060A9 BLK 60W TC",
        "code": "6956116733711",
        "price_birr": 330.53,
    },

    {
        "name": "EL 3782 JRS-CC060A9 WHT 60W TC",
        "code": "6956116733704",
        "price_birr": 330.53,
    },

    {
        "name": "EL 3788 JRS-AL012A16 2.4A USB-IP",
        "code": "6956116750633",
        "price_birr": 689.66,
    },

    {
        "name": "EL 3789 JRS-CL020A16 20W TC-IP",
        "code": "6956116750626",
        "price_birr": 1101.70,
    },

    {
        "name": "EL 3789 JRS-CL020A16 20W TC-IP-1",
        "code": "6956116750626-",
        "price_birr": 1172.21,
    },

    {
        "name": "EL 3842 JRS-1230N16 IP LED 1.2M CBL",
        "code": "6941237166135",
        "price_birr": 965.08,
    },

    {
        "name": "EL 3843 JRS-1230N16 TC LED 1.2M CBL",
        "code": "6941237166128",
        "price_birr": 881.36,
    },

    {
        "name": "EL 4109 JR-W050 20W MG WRLS PB 10000 BLK",
        "code": "TEST-NOTFOUND-6956116735203",
        "price_birr": 4693.23,
    },

    {
        "name": "EL 4112 US-CC179 20W UNIVERSAL TRVL ADP BLK",
        "code": "6958444904641",
        "price_birr": 2899.64,
    },

    {
        "name": "EL 4122 JR-EC06 TC WIRED EP BLK",
        "code": "6956116770150",
        "price_birr": 1035.61,
    },

    {
        "name": "EL 4123 JR-EW02 WIRED EP BLK",
        "code": "6956116769840",
        "price_birr": 689.66,
    },

    {
        "name": "EL 4129 JR-DS1 2IN1 MAG TWS HP WT",
        "code": "6956116737221",
        "price_birr": 4556.63,
    },

    {
        "name": "EL 4130 JRS-IW004 TC-IP WATCH CHG",
        "code": "6941237178688",
        "price_birr": 1520.35,
    },

    {
        "name": "EL 4166 JRS-AC066A16 66W USB-C 1.2M",
        "code": "6956116750619",
        "price_birr": 1015.31,
    },

    {
        "name": "EL 4190 JR-OH1 WLS HEADPHONE",
        "code": "6956116759285",
        "price_birr": 3106.80,
    },

    {
        "name": "EL 4190 JR-OH1 WLS HEADPHONE-1",
        "code": "6956116759285-",
        "price_birr": 3106.80,
    },

    {
        "name": "EL 4262-JRSY-A06 1.2M LIGHTINING AUX CBL",
        "code": "6956116773762",
        "price_birr": 881.36,
    },

    {
        "name": "EL 4263-JRSY-A07 1.2M TYPC UAX CBL",
        "code": "6956116773786",
        "price_birr": 542.38,
    },

    {
        "name": "EL 4289 JR-A26 TC-TC 60W 1M CBL BLK",
        "code": "6941237107992",
        "price_birr": 482.55,
    },

    {
        "name": "EL 4292 JR-TCW01 17W 4 PORT UNI TRVL ADP",
        "code": "6956116701963",
        "price_birr": 3521.04,
    },

    {
        "name": "EL 4296-JR-ZS368 MAG CABLE ORGANAIZER",
        "code": "6941237103680",
        "price_birr": 757.96,
    },

    {
        "name": "EL 4355 JR-FT3S SMART WATCH SPACE GREY",
        "code": "6956116723064",
        "price_birr": 5728.84,
    },

    {
        "name": "EL 4355 JR-FT3S SMART WATCH SPACE WHITE",
        "code": "6956116723101",
        "price_birr": 5728.84,
    },

    {
        "name": "EL 4355 JR-FT3S SMART WATCH SPACE WHITE-1",
        "code": "6956116723101-",
        "price_birr": 5728.84,
    },

    {
        "name": "EL 4367 JR-FT5 PLUS SMART WATCH BLK",
        "code": "6956116708474",
        "price_birr": 7110.36,
    },

    {
        "name": "EL 4369 JR-W020 MINI 5000MAH 20W POWER BANK",
        "code": "6956116713300",
        "price_birr": 3866.97,
    },

    {
        "name": "EL 4375 JR-PBM08 20W WLS POWERBANK 5000MAH-GREY",
        "code": "6956116713294",
        "price_birr": 4693.23,
    },

    {
        "name": "EL 4381 JR-L012 10000MAH 22.5W MINI PB PRPL",
        "code": "TEST-NOTFOUND-6956116701758",
        "price_birr": 4325.24,
    },

    {
        "name": "EL 4381 JR-L012 10000MAH 22.5W MINI PB WHT",
        "code": "6956116701741",
        "price_birr": 4325.24,
    },

    {
        "name": "EL 4382 JR-PBM01 10000MAH 20W WLS PB BLK",
        "code": "6941237114372",
        "price_birr": 4900.35,
    },

    {
        "name": "EL 4382 JR-PBM01 10000MAH 20W WLS PB BLK-1",
        "code": "6941237114372-",
        "price_birr": 4900.35,
    },

    {
        "name": "EL 4382 JR-PBM01 10000MAH 20W WLS PB WHITE",
        "code": "6941237112545",
        "price_birr": 4900.36,
    },

    {
        "name": "EL 4382 JR-PBM01 10000MAH 20W WLS PB WHITE-1",
        "code": "6941237112545-",
        "price_birr": 4900.35,
    },

    {
        "name": "EL 4396 JR-ZS413 MAGNETIC TRAVEL PHONE HOLDER BLK",
        "code": "6956116717827",
        "price_birr": 2899.66,
    },

    {
        "name": "EL 4398 JR-FC2 PRO SMART WATCH SILVER",
        "code": "6956116723040",
        "price_birr": 7458.52,
    },

    {
        "name": "EL 4398 JR-FC2 PRO SMART WATCH SPACE GREY",
        "code": "6956116723033",
        "price_birr": 7458.52,
    },

    {
        "name": "EL 4408 JR-TCG13UK GAN 45W USB-C CHARGER",
        "code": "6956116729332",
        "price_birr": 2899.66,
    },

    {
        "name": "EL 4483 JR-FC1 PRO BLACK",
        "code": "6956116729257",
        "price_birr": 3620.35,
    },

    {
        "name": "EL 4483 JR-FC1 PRO BLACK-1",
        "code": "6956116729257-1",
        "price_birr": 5867.64,
    },

    {
        "name": "EL 4493 JRS-IW012 2IN1 IP WATCH CHARGER",
        "code": "6956116771348",
        "price_birr": 2831.36,
    },

    {
        "name": "EL 4493 JRS-IW012 2IN1 IP WATCH CHARGER-1",
        "code": "6956116771348-",
        "price_birr": 2831.36,
    },

    {
        "name": "EL 4507 JRS-A28 1M 3A A-TC CABLE-WHT",
        "code": "6956116798284",
        "price_birr": 550.85,
    },

    {
        "name": "EL 4531 JR-PB3 TRUE WLS EARBUDS BEIGE",
        "code": "6941237101976",
        "price_birr": 2924.10,
    },

    {
        "name": "EL 4541 JRS-A53 3A 1.2M A-C FAST CHARGING CABLE-WHT",
        "code": "6956116730482",
        "price_birr": 1035.61,
    },

    {
        "name": "EL 4551 JR PR1 10000MAH 22.5W ELVA SERIES MINI PB BLK",
        "code": "6956116765002",
        "price_birr": 5314.61,
    },

    {
        "name": "EL 4552 JR-TCG17UK45W 2C SUPER FSAST CHARGER",
        "code": "6941237127365",
        "price_birr": 3117.02,
    },

    {
        "name": "EL 4553JRS-A16 PRO 30W C-IP 1.2M DIGITAL CABLE",
        "code": "6956116721374",
        "price_birr": 1311.04,
    },

    {
        "name": "EL 4557 JR-TCL06 67W GAN CHARGER WITHRETRACTABLECABL",
        "code": "TEST-NOTFOUND-6956116771157",
        "price_birr": 6143.09,
    },

    {
        "name": "EL 4558 JR-FV2 VENTURE SERIES SMART WATCH",
        "code": "6956116798345",
        "price_birr": 9904.28,
    },

    {
        "name": "EL 4559 JR-OE3 OPEN EAR TRUE WLS EARBUDS-gry",
        "code": "6956116723606",
        "price_birr": 7932.24,
    },

    {
        "name": "EL 4586 JR-PBF27 10000MAH 22.5W MINI POWER BANK- BLACK",
        "code": "6956116745127",
        "price_birr": 4005.78,
    },

    {
        "name": "EL 4592 JR-JH1 HYBRID ANC WLS HEADPHONES",
        "code": "6956116723781",
        "price_birr": 8145.97,
    },

    {
        "name": "EL 4594 JR-W12 FOLDABLE WLS WATCH CHARGER",
        "code": "6956116725051",
        "price_birr": 1932.39,
    },

    {
        "name": "EL 4597 JR-W17 3IN 1 WIRELESS CHARGER",
        "code": "6941237127082",
        "price_birr": 5799.35,
    },

    {
        "name": "8850",
        "code": "8849",
        "price_birr": 2412.84,
    },

    {
        "name": "93-gl] JW Stud Earring   RED TREES  AUG-1.15",
        "code": "888687",
        "price_birr": 339.30,
    },

    {
        "name": "JW 4426 NEW",
        "code": "4426 NEW STEEL-1",
        "price_birr": 2104.70,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME - AC-BERBERRY     0BE2334",
        "code": "8056597640596",
        "price_birr": 10415.53,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME - AC-G-ARMANI     0AR7074",
        "code": "8056597427739",
        "price_birr": 17999.38,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME - AC-PERSOL     0PO3092V",
        "code": "8053672294507",
        "price_birr": 18708.24,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME - AC-PERSOL     0PO3275V",
        "code": "8056597808002",
        "price_birr": 19888.73,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME - AC-POLO RALPH LAUREN     0PP8520",
        "code": "8053672095418",
        "price_birr": 8463.35,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME - AC-POLO RALPH LAUREN     0PP8541",
        "code": "8056597424288",
        "price_birr": 8315.46,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME - AC-POLO RALPH LAUREN     0PP8541-",
        "code": "8056597424318",
        "price_birr": 8315.46,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME - AC-POLO RALPH LAUREN     0PP8543U",
        "code": "8056597596756",
        "price_birr": 7247.24,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME - AC-VOGUE     0VO5326",
        "code": "8056597644105",
        "price_birr": 8380.32,
    },

    {
        "name": "JW ACETATE MAN OPTICAL-VOGUE     0VO5434",
        "code": "8056597601214",
        "price_birr": 8234.01,
    },

    {
        "name": "JW ACETATE UNISEX OPTICAL FRAME - AC-PERSOL     0PO3218V",
        "code": "TEST-NOTFOUND-8056597056977",
        "price_birr": 19888.70,
    },

    {
        "name": "JW ACETATE UNISEX OPTICAL FRAME - AC-PERSOL     0PO3263V",
        "code": "8056597807951",
        "price_birr": 20372.14,
    },

    {
        "name": "JW ACETATE UNISEX OPTICAL FRAME - AC-PERSOL     0PO3292V",
        "code": "8056597808132",
        "price_birr": 22425.65,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC- Burberry     0BE2255Q",
        "code": "8053672762013",
        "price_birr": 20479.81,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-BURBERRY     0BE2345",
        "code": "8056597490528",
        "price_birr": 16925.23,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-BURBERRY     0BE2365",
        "code": "8056597719124",
        "price_birr": 18700.42,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-Burberry     0BE2205",
        "code": "8053672417753",
        "price_birr": 17772.04,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-Burberry     0BE2363",
        "code": "8056597727174",
        "price_birr": 20478.08,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-MIU MIU     0MU 01VV",
        "code": "8056597784566",
        "price_birr": 26231.40,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-MIU MIU     0MU 03UV",
        "code": "8056597668545",
        "price_birr": 22845.98,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-MIU MIU     0MU 03UV-",
        "code": "8056597668507",
        "price_birr": 14062.01,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-MIU MIU     0MU 04UV",
        "code": "8056597669016",
        "price_birr": 26231.40,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-MIU MIU     0MU 04UV-",
        "code": "8056597669047",
        "price_birr": 26229.19,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-VERSACE     0VE3274B",
        "code": "8056597412858",
        "price_birr": 19749.83,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-VERSACE     0VE3304",
        "code": "8056597535908",
        "price_birr": 16318.65,
    },

    {
        "name": "JW ACETATE WOMAN OPTICAL FRAME - AC-VERSACE     0VE3309",
        "code": "8056597533355",
        "price_birr": 15996.25,
    },

    {
        "name": "JW ARMANI  AR11635",
        "code": "4064092292541",
        "price_birr": 34262.55,
    },

    {
        "name": "JW ARMANI  AR11664",
        "code": "4064092324778",
        "price_birr": 29982.58,
    },

    {
        "name": "JW ARMANI  AR60085",
        "code": "4064092324761",
        "price_birr": 50157.11,
    },

    {
        "name": "JW ARMANI AR11484",
        "code": "4064092141931",
        "price_birr": 32283.85,
    },

    {
        "name": "JW ARMANI AR1925",
        "code": "TEST-NOTFOUND-4053858564015",
        "price_birr": 39315.99,
    },

    {
        "name": "JW ARMANI AR1926",
        "code": "4053858564022",
        "price_birr": 46581.80,
    },

    {
        "name": "JW ARMANI EXCHANGE   AX1951",
        "code": "4064092228045-4051432723254",
        "price_birr": 21344.38,
    },

    {
        "name": "JW ARMANI EXCHANGE   AX2164",
        "code": "4053858444959-4051432959998",
        "price_birr": 21344.38,
    },

    {
        "name": "JW ARMANI EXCHANGE   AX2611",
        "code": "4053858898080-4053858190917",
        "price_birr": 21344.38,
    },

    {
        "name": "JW ARMANI EXCHANGE   AX2871",
        "code": "4064092227383-4053858519572",
        "price_birr": 13629.86,
    },

    {
        "name": "JW ARMANI EXCHANGE   AX7138SET",
        "code": "4064092139808-4064092132700",
        "price_birr": 17058.55,
    },

    {
        "name": "JW ARMANI EXCHANGE   AX7148SET",
        "code": "4064092226461-4064092140279",
        "price_birr": 23915.88,
    },

    {
        "name": "JW ARMANI EXCHANGE   AX7151SET",
        "code": "4064092240276-4051432943508",
        "price_birr": 23915.88,
    },

    {
        "name": "JW ARMANI EXCHANGE AX1277",
        "code": "AX1277-4048803188064",
        "price_birr": 10529.10,
    },

    {
        "name": "JW ARMANI EXCHANGE AX1326",
        "code": "4053858632127",
        "price_birr": 9889.32,
    },

    {
        "name": "JW ARMANI EXCHANGE AX1723",
        "code": "AX1723-4064092270891",
        "price_birr": 9648.02,
    },

    {
        "name": "JW ARMANI EXCHANGE AX1730",
        "code": "AX1730",
        "price_birr": 22963.17,
    },

    {
        "name": "JW ARMANI EXCHANGE AX1731",
        "code": "AX1731",
        "price_birr": 23923.93,
    },

    {
        "name": "JW ARMANI EXCHANGE AX1752",
        "code": "AX1752",
        "price_birr": 23923.93,
    },

    {
        "name": "JW ARMANI EXCHANGE AX1767",
        "code": "4064092328356",
        "price_birr": 24464.31,
    },

    {
        "name": "JW ARMANI EXCHANGE AX1865",
        "code": "AX1865",
        "price_birr": 21041.57,
    },

    {
        "name": "JW ARMANI EXCHANGE AX1870",
        "code": "AX1870",
        "price_birr": 19119.94,
    },

    {
        "name": "JW ARMANI EXCHANGE AX1874",
        "code": "AX1874",
        "price_birr": 21041.57,
    },

    {
        "name": "JW ARMANI EXCHANGE AX2098",
        "code": "AX2098",
        "price_birr": 22963.17,
    },

    {
        "name": "JW ARMANI EXCHANGE AX2104",
        "code": "TEST-NOTFOUND-AX2104",
        "price_birr": 21041.57,
    },

    {
        "name": "JW ARMANI EXCHANGE AX2133",
        "code": "4053858190917",
        "price_birr": 19549.40,
    },

    {
        "name": "JW ARMANI EXCHANGE AX2862",
        "code": "4064092328394",
        "price_birr": 26698.44,
    },

    {
        "name": "JW ARMANI EXCHANGE AX2863",
        "code": "4064092328400",
        "price_birr": 25832.77,
    },

    {
        "name": "JW ARMANI EXCHANGE AX2864",
        "code": "4064092328417",
        "price_birr": 27815.54,
    },

    {
        "name": "JW ARMANI EXCHANGE AX2865",
        "code": "4064092328424",
        "price_birr": 24299.39,
    },

    {
        "name": "JW ARMANI EXCHANGE AX4161",
        "code": "4064092270143",
        "price_birr": 16070.15,
    },

    {
        "name": "JW ARMANI EXCHANGE AX4167",
        "code": "4064092328325",
        "price_birr": 16165.77,
    },

    {
        "name": "JW ARMANI EXCHANGE AX4168",
        "code": "4064092328431",
        "price_birr": 16495.69,
    },

    {
        "name": "JW ARMANI EXCHANGE AX4331",
        "code": "4053858632349",
        "price_birr": 24795.30,
    },

    {
        "name": "JW ARMANI EXCHANGE AX5170",
        "code": "4064092294248",
        "price_birr": 12305.22,
    },

    {
        "name": "JW ARMANI EXCHANGE AX5172",
        "code": "4064092294262",
        "price_birr": 22230.14,
    },

    {
        "name": "JW ARMANI EXCHANGE AX5264",
        "code": "4064092064827",
        "price_birr": 9648.02,
    },

    {
        "name": "JW ARMANI EXCHANGE AX5912",
        "code": "AX5912",
        "price_birr": 21041.57,
    },

    {
        "name": "JW ARMANI EXCHANGE AX5916",
        "code": "4064092328370",
        "price_birr": 21123.58,
    },

    {
        "name": "JW ARMANI EXCHANGE AX7105",
        "code": "4053858938120",
        "price_birr": 19102.21,
    },

    {
        "name": "JW ARMANI EXCHANGE AX7121",
        "code": "4064092012903",
        "price_birr": 22266.01,
    },

    {
        "name": "JW ARMANI EXCHANGE AX7145SET",
        "code": "4064092184198",
        "price_birr": 22134.28,
    },

    {
        "name": "JW ARMANI EXCHANGE AX7156SET",
        "code": "4064092270266",
        "price_birr": 22134.28,
    },

    {
        "name": "JW ARMANI EXCHANGE AX7165SET",
        "code": "4064092329506",
        "price_birr": 23144.97,
    },

    {
        "name": "JW Acetate Frame CR39 lenses Sun Glass RT2034",
        "code": "TEST-NOTFOUND-RT2034",
        "price_birr": 5213.09,
    },

    {
        "name": "JW Acetate Frame Polarized lenses Sun Glass 1439T",
        "code": "1439T",
        "price_birr": 4531.42,
    },

    {
        "name": "JW Acetate Frame Polarized lenses Sun Glass 1727S",
        "code": "17275",
        "price_birr": 4987.50,
    },

    {
        "name": "JW Acetate Frame Polarized lenses Sun Glass 17775",
        "code": "17775",
        "price_birr": 4376.94,
    },

    {
        "name": "JW Acetate Frame Polarized lenses Sun Glass 1943",
        "code": "1943",
        "price_birr": 4376.94,
    },

    {
        "name": "JW Acetate Frame Polarized lenses Sun Glass 1943S-1",
        "code": "19435-1",
        "price_birr": 4531.42,
    },

    {
        "name": "JW Acetate Frame Polarized lenses Sun Glass 22SA007",
        "code": "225A007",
        "price_birr": 5595.62,
    },

    {
        "name": "SP  ABSOLUT VANILA 1LIT",
        "code": "50124-60108",
        "price_birr": 1989.90,
    },

    {
        "name": "SP  BELVEDERE RF SMOGORY 1LI*6",
        "code": "081753829575",
        "price_birr": 1852.24,
    },

    {
        "name": "SP  BOLS CACAO WHITE70CL",
        "code": "8716000964960",
        "price_birr": 808.35,
    },

    {
        "name": "SP  GLEN MORAY CLASSIC 40 70CL X 6",
        "code": "5010494508307",
        "price_birr": 1640.05,
    },

    {
        "name": "SP  SMIRNOFF BLUE 75CL*12",
        "code": "5410316694216",
        "price_birr": 589.85,
    },

    {
        "name": "SP  ST VIVANT ARM VSOP40 70X6 ET",
        "code": "3147690083306",
        "price_birr": 4608.58,
    },

    {
        "name": "SP 0PY90 CH SOCIANDO MALLET 21",
        "code": "3428430000921",
        "price_birr": 2914.05,
    },

    {
        "name": "SP 0TB20 CUVEEJ CH JAU ROSE BIO 24X6",
        "code": "3119460004941",
        "price_birr": 963.70,
    },

    {
        "name": "SP 0TB30 CUVEEJ CH JAU BLANC BIO 24X6",
        "code": "3119460005603",
        "price_birr": 963.70,
    },

    {
        "name": "SP 1792 Small Batch Bourbon 6*75cl*46.85%",
        "code": "080660001203",
        "price_birr": 3381.40,
    },

    {
        "name": "SP 19 CRIMES CALI RED",
        "code": "9310297036479",
        "price_birr": 1721.41,
    },

    {
        "name": "SP 4TH STREET NATURAL SWEET RED 75CL",
        "code": "6001108059178",
        "price_birr": 433.56,
    },

    {
        "name": "SP 4TH STREET NATURAL SWEET RED 75CL*6",
        "code": "6001108049582",
        "price_birr": 512.21,
    },

    {
        "name": "SP 4TH STREET NATURAL SWEET ROSE 75CL",
        "code": "TEST-NOTFOUND-6001108049605",
        "price_birr": 395.76,
    },

    {
        "name": "SP 4TH STREET NATURAL SWEET WHITE  75CL",
        "code": "6001108049599",
        "price_birr": 514.25,
    },

    {
        "name": "SP ABSOLUT APEACH 12*1LIT",
        "code": "7312040070107",
        "price_birr": 717.98,
    },

    {
        "name": "SP ABSOLUT CITRON 1LIT*12",
        "code": "7312040090105",
        "price_birr": 689.85,
    },

    {
        "name": "SP ABSOLUT ELYX 1LT*6",
        "code": "7312040211012",
        "price_birr": 1536.29,
    },

    {
        "name": "SP ABSOLUT ELYX 6 X 70CL RF WO/GB COPPER CRAFTED VODKA 42.",
        "code": "7312040217014",
        "price_birr": 2559.76,
    },

    {
        "name": "SP ABSOLUT GRAPE FRUIT 1LI*12",
        "code": "7312040552177",
        "price_birr": 642.85,
    },

    {
        "name": "SP ABSOLUT MANDRIN 1LTR*12",
        "code": "7312040050109",
        "price_birr": 710.67,
    },

    {
        "name": "SP ABSOLUT MANGO 1LIT*12",
        "code": "7312040181001",
        "price_birr": 652.43,
    },

    {
        "name": "SP ABSOLUT RASBERRY 1LI *12",
        "code": "7312040350070",
        "price_birr": 697.28,
    },

    {
        "name": "SP ABSOLUT VODKA VOICES 12*1LI",
        "code": "7312040552832",
        "price_birr": 353.10,
    },

    {
        "name": "SP ABSOLUTE BLUE 40%VOL 1LTR*12",
        "code": "7312040017034",
        "price_birr": 1442.29,
    },

    {
        "name": "SP ACHAVAL FERRER MALBEC MENDOZA",
        "code": "7798091111929",
        "price_birr": 2835.26,
    },

    {
        "name": "SP AMARETTO DI SARONNO 12X100 CL RF W/O GB 28%",
        "code": "8001110016341",
        "price_birr": 1716.52,
    },

    {
        "name": "SP AMARULA 75cl*6",
        "code": "6001495062508",
        "price_birr": 775.15,
    },

    {
        "name": "SP AMARULA Cream Liquor 6*1Liter",
        "code": "6001495062669-6001108105295",
        "price_birr": 1440.53,
    },

    {
        "name": "SP AMARULLA CREAM LIQUER 12X37.5 CL RF WO/GB 17%",
        "code": "6001495062478",
        "price_birr": 641.36,
    },

    {
        "name": "SP AMARULLA VANILLA SPICE 6X100CL RF WO/GB 15.5%",
        "code": "6001108105998-6001108093783",
        "price_birr": 1772.43,
    },

    {
        "name": "SP APPEROL APERITIVO 1LI",
        "code": "8002230000012/721059002387",
        "price_birr": 1735.88,
    },

    {
        "name": "SP ARGENTO PINOT GRIGIO(75CL)",
        "code": "7798159560157",
        "price_birr": 1054.01,
    },

    {
        "name": "SP ARGENTO SAUVIGNON BLANC -75CL",
        "code": "TEST-NOTFOUND-7798159560171",
        "price_birr": 1164.33,
    },

    {
        "name": "SP ARM ST.VIVANT6*703147690083207",
        "code": "3147690083207",
        "price_birr": 4895.48,
    },

    {
        "name": "SP ARMAGAC ST VIVANT X0 40% 70CLX6",
        "code": "3147690019602",
        "price_birr": 7744.57,
    },

    {
        "name": "SP ARMAGNAC NAP.ROI GASC.40 70X12",
        "code": "3347590000261",
        "price_birr": 2675.58,
    },

    {
        "name": "SP ARMAGNAC XXX LMZ 40 70X6",
        "code": "3147690045908",
        "price_birr": 3497.23,
    },

    {
        "name": "SP ARMAND DE BRIGNAC BRUT GOLD + GB 75 CL",
        "code": "193ADB",
        "price_birr": 59058.26,
    },

    {
        "name": "SP AULTMORE 12YO 70CL",
        "code": "5000277000265",
        "price_birr": 6842.60,
    },

    {
        "name": "SP AULTMORE 21YO WHISKY -70CL",
        "code": "5000277000364",
        "price_birr": 28929.99,
    },

    {
        "name": "SP Absolut Vodka Triple Pack 4X3*100cl*40%",
        "code": "4295853401234",
        "price_birr": 3549.61,
    },

    {
        "name": "SP Absolut Vodka Twin Pack W/37,5cl Raspberry 6*2*100cl*40% RF",
        "code": "7312040551040",
        "price_birr": 1346.33,
    },

    {
        "name": "SP Akashi Red Oak Whisky 6 x 50cl Bottles",
        "code": "4969265773134",
        "price_birr": 1145.30,
    },

    {
        "name": "SP Amaro Montenegro 6*100cl*23%",
        "code": "8000330001175",
        "price_birr": 2370.60,
    },

    {
        "name": "SP Aperol Bi-Pack APRL3*100cl+PRCO3*75cl*11%",
        "code": "8000040011389",
        "price_birr": 3616.72,
    },

    {
        "name": "SP Auchentoshan American Oak Reserve 12*100cl*40$",
        "code": "5010496005378",
        "price_birr": 4104.53,
    },

    {
        "name": "SP B&G 1725 AOP BORDEAUX ROUGE  75CL*12 RFW/OGB 1296",
        "code": "3035131008103",
        "price_birr": 1139.85,
    },

    {
        "name": "SP B&G AOP BEAUJOLAISVILLAGES  1ZX75CLCORKW/OGB J3.5%",
        "code": "3035130202106-3336490051145",
        "price_birr": 1742.79,
    },

    {
        "name": "SP B&G AOP COTES DU RHONE 75CL*12 1ZM75CLCORKW/OGB145B",
        "code": "3035130401103",
        "price_birr": 1104.67,
    },

    {
        "name": "SP B&G AOP MARGAUX 2021  75CL CORKW/OGB 13%",
        "code": "3035130013108",
        "price_birr": 3636.54,
    },

    {
        "name": "SP B&G BARRAILLAUSSAC BORDEAUX  ROUGE 6X75CLCORKW/OG",
        "code": "3035134123100",
        "price_birr": 1133.21,
    },

    {
        "name": "SP B&G COTES DU ROUSSILION VILLAGES 12X75CL",
        "code": "3035131125701",
        "price_birr": 1018.75,
    },

    {
        "name": "SP B&G M DE MAGNOL 2020  AOP HAUT MEDOC 12X75CL",
        "code": "TEST-NOTFOUND-816685011244",
        "price_birr": 1637.34,
    },

    {
        "name": "SP B&G MUSCADETSEVRE ET MAINE  J2X75CLCORKW/OGB 11.5°",
        "code": "3035130511109",
        "price_birr": 874.71,
    },

    {
        "name": "SP BACARDI BLACK 6 X 75CL RF W/O GB 40%",
        "code": "5010677038935",
        "price_birr": 1056.64,
    },

    {
        "name": "SP BACARDI CARTA BLANCA 12 X 100CL RF W/O GB 40%",
        "code": "5010677012850",
        "price_birr": 1169.13,
    },

    {
        "name": "SP BACARDI GOLD 12 X 100CL RF W/OGB 40%",
        "code": "5010677025812",
        "price_birr": 1404.35,
    },

    {
        "name": "SP BACARDI RON CARTA BLANCA 1L*12",
        "code": "5010677015738",
        "price_birr": 1378.55,
    },

    {
        "name": "SP BAILEYS IRISH CREAM 12 X 75CL RF W/O GB 17%",
        "code": "5011013100132",
        "price_birr": 127.44,
    },

    {
        "name": "SP BALLANTINES 12 X 100CL NRF W/OGB 40%",
        "code": "5010106111956",
        "price_birr": 1449.41,
    },

    {
        "name": "SP BALLANTINES 12 X 75CL NRF W/O GB 40%",
        "code": "5010106111451",
        "price_birr": 1230.90,
    },

    {
        "name": "SP BALLANTINES FINEST WHISKY37",
        "code": "5010106112250",
        "price_birr": 768.01,
    },

    {
        "name": "SP BALLEYS SALTED CARAMEL 1LI*12",
        "code": "5011013931293",
        "price_birr": 580.06,
    },

    {
        "name": "SP BANFI ROSSO DI MONTALC",
        "code": "8015674840960",
        "price_birr": 2767.75,
    },

    {
        "name": "SP BARBERA D'ALBA DOC 2020 BATTAGLIONE MG 1.5 LTR",
        "code": "8029358025215",
        "price_birr": 5521.62,
    },

    {
        "name": "SP BARBERA D'ASTI DOCG 2020 BATTAGLIONE 75CL",
        "code": "8029358005118",
        "price_birr": 2160.72,
    },

    {
        "name": "SP BARDENET XO FINEST 1LI*12",
        "code": "3012993045361",
        "price_birr": 422.73,
    },

    {
        "name": "SP BARDINET BDY VSOP36 1LX12",
        "code": "3012993024298",
        "price_birr": 2008.83,
    },

    {
        "name": "SP BARDNET XO 6YEARS OLD 70*6",
        "code": "3012993041615",
        "price_birr": 358.38,
    },

    {
        "name": "SP BATASIOLO BAROLO",
        "code": "8002820005304",
        "price_birr": 3645.33,
    },

    {
        "name": "SP BATASIOLO BLACK GAVI",
        "code": "8002820000781",
        "price_birr": 1468.26,
    },

    {
        "name": "SP BATASIOLO GAVI DI GAVI",
        "code": "8002820001184",
        "price_birr": 1620.15,
    },

    {
        "name": "SP BEACH BUM GOLD (70CL)",
        "code": "TEST-NOTFOUND-6091318140025",
        "price_birr": 2360.81,
    },

    {
        "name": "SP BEEFEATER BLACKBERRY GIN 12 X 100CL RF W/O GB 37.50%",
        "code": "5000299618578",
        "price_birr": 650.90,
    },

    {
        "name": "SP BEEFEATER PREMIUM 2470CL*6",
        "code": "5000299605004",
        "price_birr": 1134.80,
    },

    {
        "name": "SP BEEFETAER*12",
        "code": "5000329002292",
        "price_birr": 662.54,
    },

    {
        "name": "SP BEEHIVE VSOP 35ML*12",
        "code": "3012993048881",
        "price_birr": 151.15,
    },

    {
        "name": "SP BELLINGHAM HOMESTEAD SHIRAZ 6X750ML RF",
        "code": "6001506908771",
        "price_birr": 1001.88,
    },

    {
        "name": "SP BELVEDER 70CL*6",
        "code": "5901041003454",
        "price_birr": 1532.38,
    },

    {
        "name": "ET 1 kg Roasted Coffee",
        "code": "1100",
        "price_birr": 1380.56,
    },

    {
        "name": "ET Acacia Medium Sweet Red",
        "code": "9126091770118",
        "price_birr": 1127.78,
    },

    {
        "name": "ET Acacia Medium Sweet White",
        "code": "24493",
        "price_birr": 1356.52,
    },

    {
        "name": "ET Ambar Coffee 1kg",
        "code": "8052141960028",
        "price_birr": 1292.65,
    },

    {
        "name": "ET Bauli II Panettone Moro Con Gocce Di Cioccolato 900g",
        "code": "8001720427179",
        "price_birr": 6782.61,
    },

    {
        "name": "ET Biscuits",
        "code": "6922719145336",
        "price_birr": 494.00,
    },

    {
        "name": "ET Biscuits (Big)",
        "code": "6919892312105",
        "price_birr": 617.50,
    },

    {
        "name": "ET Black Cumin-Fatty Oil-100ml",
        "code": "002",
        "price_birr": 1571.31,
    },

    {
        "name": "ET Black Cumin-Fatty Oil-20ml",
        "code": "001",
        "price_birr": 666.95,
    },

    {
        "name": "ET CHITO Rosted Coffee 0.25kg",
        "code": "C45 - C50",
        "price_birr": 576.99,
    },

    {
        "name": "ET CHITO Rosted Coffee 0.5kg",
        "code": "C44 - C51",
        "price_birr": 1031.64,
    },

    {
        "name": "ET COFFEA COFEE 0.25kg",
        "code": "C20",
        "price_birr": 460.16,
    },

    {
        "name": "ET COFFEA COFEE 0.5kg",
        "code": "C21",
        "price_birr": 807.30,
    },

    {
        "name": "ET COFFEA COFEE 1Kg",
        "code": "TEST-NOTFOUND-C22",
        "price_birr": 1375.35,
    },

    {
        "name": "ET Castor-Fatty Oil-100ml",
        "code": "018",
        "price_birr": 1989.56,
    },

    {
        "name": "ET Castor-Fatty Oil-20ml",
        "code": "017",
        "price_birr": 644.35,
    },

    {
        "name": "ET Chaka Coffee Been 0.25kg",
        "code": "ET Chaka Coffee Been 0.25kg",
        "price_birr": 466.58,
    },

    {
        "name": "ET Chaka Coffee Been 0.5Kg",
        "code": "ET Chaka Coffee Been 0.5Kg",
        "price_birr": 743.82,
    },

    {
        "name": "ET Chaka Coffee Been 1kg",
        "code": "cHAKA-cOFFEE-1-kg",
        "price_birr": 1681.33,
    },

    {
        "name": "ET Chaka Coffee Ground 0.25kg",
        "code": "chaka coffee 0.25 kg",
        "price_birr": 496.44,
    },

    {
        "name": "ET Chaka Coffee Ground 0.5kg",
        "code": "cHAKA-cOFFEE-1/2-kg",
        "price_birr": 818.88,
    },

    {
        "name": "ET Chaka Coffee Ground 1kg",
        "code": "1kg",
        "price_birr": 1681.33,
    },

    {
        "name": "ET Champion Coffee 75cl",
        "code": "2519662727715",
        "price_birr": 2470.18,
    },

    {
        "name": "ET Champion Dry GIN 75cl",
        "code": "2519662727678",
        "price_birr": 1320.00,
    },

    {
        "name": "ET Champion Vodka 75cl",
        "code": "2519662727739",
        "price_birr": 2108.61,
    },

    {
        "name": "ET ET GROVE COFFEE 250G",
        "code": "C40",
        "price_birr": 701.58,
    },

    {
        "name": "ET ET GROVE COFFEE 500G",
        "code": "C41",
        "price_birr": 1354.60,
    },

    {
        "name": "ET Etete Coffee Anaerbic Beans",
        "code": "100",
        "price_birr": 926.95,
    },

    {
        "name": "ET Etete Coffee Anaerbic Ground",
        "code": "etete",
        "price_birr": 926.95,
    },

    {
        "name": "ET Etete Coffee Premium House Ground",
        "code": "Ground",
        "price_birr": 723.48,
    },

    {
        "name": "ET Etete Coffee Special House Blend Beans",
        "code": "200",
        "price_birr": 520.00,
    },

    {
        "name": "ET Etete Premium House Blend Bean",
        "code": "101",
        "price_birr": 723.48,
    },

    {
        "name": "ET FS Choco Zen Rose Chocolate Nutella Knafeh100g",
        "code": "7972",
        "price_birr": 2502.24,
    },

    {
        "name": "ET FS La Lushe Chocolate 100g",
        "code": "TEST-NOTFOUND-4929",
        "price_birr": 2502.24,
    },

    {
        "name": "ET FS La Lushe Chocolate Nutella Knafeh100g",
        "code": "4943",
        "price_birr": 2502.24,
    },

    {
        "name": "ET FS La Lushe Chocolate Peanuts Caramel Knafeh100g",
        "code": "4950",
        "price_birr": 2502.24,
    },

    {
        "name": "ET FS La Lushe Chocolate White Cho Pistacho Knafeh100 g",
        "code": "4905",
        "price_birr": 2502.24,
    },

    {
        "name": "ET Fruit Juice",
        "code": "6920459954997",
        "price_birr": 390.00,
    },

    {
        "name": "ET Fruit Juice.",
        "code": "6921168500956",
        "price_birr": 435.41,
    },

    {
        "name": "ET Functional Drink",
        "code": "6921168504015",
        "price_birr": 436.53,
    },

    {
        "name": "ET GERA COFFEE 0.5kg",
        "code": "C17",
        "price_birr": 92.70,
    },

    {
        "name": "ET GERA COFFEE 1Kg",
        "code": "C10",
        "price_birr": 169.57,
    },

    {
        "name": "ET Green Gold  Packed Coffee (powder) 0.25kg",
        "code": "C38",
        "price_birr": 305.21,
    },

    {
        "name": "ET Green Gold  Packed Coffee (powder) 0.5kg",
        "code": "C37",
        "price_birr": 354.78,
    },

    {
        "name": "ET Green Gold  Packed Coffee (powder) 1Kg",
        "code": "C36",
        "price_birr": 1096.52,
    },

    {
        "name": "ET Ground Coffee 1kg",
        "code": "ET Ground Coffee 1kg",
        "price_birr": 1683.50,
    },

    {
        "name": "ET Ground Coffee 250g",
        "code": "ET Ground Coffee 250g",
        "price_birr": 564.20,
    },

    {
        "name": "ET Ground Coffee 500g",
        "code": "ET Ground Coffee 500g",
        "price_birr": 1246.70,
    },

    {
        "name": "ET HADERO COFFEE 0.5kg",
        "code": "C26",
        "price_birr": 452.17,
    },

    {
        "name": "ET HADERO COFFEE 1KG",
        "code": "C25",
        "price_birr": 881.74,
    },

    {
        "name": "ET Hibiscus-Herbal Tea-50gr",
        "code": "070",
        "price_birr": 644.35,
    },

    {
        "name": "ET Honey Valley Jelly Tea",
        "code": "6938888882118",
        "price_birr": 436.75,
    },

    {
        "name": "ET Jiadubao Chinese Herbtea (Large)",
        "code": "4891599366808",
        "price_birr": 520.00,
    },

    {
        "name": "ET Katikala -KAT 75cl",
        "code": "TEST-NOTFOUND-2519662727692",
        "price_birr": 2017.99,
    },

    {
        "name": "ET Kosseret-Herbal Tea-50kg",
        "code": "079",
        "price_birr": 293.92,
    },

    {
        "name": "ET Leef coffee 0.25kg",
        "code": "C52",
        "price_birr": 1493.75,
    },

    {
        "name": "ET Leef coffee 0.5kg",
        "code": "C51",
        "price_birr": 2471.83,
    },

    {
        "name": "ET Leef coffee 1kg",
        "code": "C50",
        "price_birr": 3510.00,
    },

    {
        "name": "ET Lemongrass-Essential Oil-100ml",
        "code": "036",
        "price_birr": 2317.39,
    },

    {
        "name": "ET Lemongrass-Essential Oil-10ml",
        "code": "035",
        "price_birr": 644.35,
    },

    {
        "name": "ET MINERAL WATER 0.6 ML",
        "code": "AQ04",
        "price_birr": 14.98,
    },

    {
        "name": "ET MINERAL WATER 300ML",
        "code": "AQ02",
        "price_birr": 8.40,
    },

    {
        "name": "ET MINERAL WATER 500ML",
        "code": "AQ01",
        "price_birr": 23.27,
    },

    {
        "name": "ET MOYEE COFFEE 0.25kg",
        "code": "C7",
        "price_birr": 263.30,
    },

    {
        "name": "ET MOYEE COFFEE 0.5kg",
        "code": "C6",
        "price_birr": 735.16,
    },

    {
        "name": "ET MOYEE COFFEE 1Kg",
        "code": "C5",
        "price_birr": 1380.56,
    },

    {
        "name": "ET Moringa-Fatty Oil-100ml",
        "code": "009",
        "price_birr": 3481.74,
    },

    {
        "name": "ET Moringa-Fatty Oil-20ml",
        "code": "008",
        "price_birr": 972.18,
    },

    {
        "name": "ET Moringa-Herbal Tea-50gr",
        "code": "073",
        "price_birr": 293.92,
    },

    {
        "name": "ET ORIGIN COFFEE 0.25kg",
        "code": "C30",
        "price_birr": 455.00,
    },

    {
        "name": "ET ORIGIN COFFEE 0.5kg",
        "code": "C31",
        "price_birr": 585.00,
    },

    {
        "name": "ET ORIGIN COFFEE 1kG",
        "code": "C29",
        "price_birr": 975.00,
    },

    {
        "name": "91085671NSZ",
        "code": "910B5671NSZ",
        "price_birr": 8945.85,
    },

    {
        "name": "LU  Fashion  Ride-on  Luggage-Race  Car",
        "code": "TEST-NOTFOUND-665556053575",
        "price_birr": 5011.55,
    },

    {
        "name": "LU  Travel  Tots  18”  Luggage  with  Backpack-Panda",
        "code": "665556024124",
        "price_birr": 5369.53,
    },

    {
        "name": "LU 2X1taa   Midnigh   Green",
        "code": "665556045273",
        "price_birr": 7159.36,
    },

    {
        "name": "LU 6 PANEL STRETCH HAT EMBOSSED 912208-465",
        "code": "193517347277",
        "price_birr": 3624.00,
    },

    {
        "name": "LU 6 PANEL STRETCH METALLIC HAT 912209-7AN",
        "code": "193517677794",
        "price_birr": 3624.00,
    },

    {
        "name": "LU ABEARICAN EXPRESS DLXR BACKPACK",
        "code": "910B5075NSZ",
        "price_birr": 7268.49,
    },

    {
        "name": "LU ADELASIA LARGE 2 IN 1 TOTE",
        "code": "190231958673",
        "price_birr": 17044.74,
    },

    {
        "name": "LU ADELASIA LARGE 2 IN 1 TOTE-2",
        "code": "190231958659",
        "price_birr": 18843.38,
    },

    {
        "name": "LU ADELASIA MULTI COMP SATCHEL",
        "code": "190231965039",
        "price_birr": 18843.40,
    },

    {
        "name": "LU ALDINA GIRLFRIEND SATCHEL",
        "code": "190231963257",
        "price_birr": 18843.40,
    },

    {
        "name": "LU ALDINA NOEL TOTE",
        "code": "190231963417",
        "price_birr": 11595.93,
    },

    {
        "name": "LU ALIEN WRITERS DLX BACKPACK",
        "code": "910B6442NSZ",
        "price_birr": 8945.85,
    },

    {
        "name": "LU CAMO SPLASH DLXSV BACKPACK",
        "code": "910B7624NSZ",
        "price_birr": 8945.85,
    },

    {
        "name": "LU CAMO SPLASH MESSENGER SLING",
        "code": "910B7865NSZ",
        "price_birr": 6709.39,
    },

    {
        "name": "LU COTTON CANDY DREAMS DLXR BACKPACK",
        "code": "910b6721NSZ",
        "price_birr": 7268.49,
    },

    {
        "name": "LU DELSEY PARIS 00162211572RG",
        "code": "3219110543490",
        "price_birr": 10748.26,
    },

    {
        "name": "LU DELSEY PARIS 00202061172RG",
        "code": "3219110513974",
        "price_birr": 11405.56,
    },

    {
        "name": "LU DELSEY PARIS 00384580309MR",
        "code": "3219110533163",
        "price_birr": 19201.06,
    },

    {
        "name": "LU DELSEY PARIS 162111509",
        "code": "3219110505801",
        "price_birr": 10741.55,
    },

    {
        "name": "LU DELSEY PARIS 162141002",
        "code": "3219110512922",
        "price_birr": 20690.70,
    },

    {
        "name": "LU DELSEY PARIS 162141009",
        "code": "TEST-NOTFOUND-3219110520675",
        "price_birr": 21238.59,
    },

    {
        "name": "LU DELSEY PARIS 162141017",
        "code": "3219110512915",
        "price_birr": 21237.20,
    },

    {
        "name": "LU DELSEY PARIS 162141022",
        "code": "3219110512939",
        "price_birr": 20690.70,
    },

    {
        "name": "LU DELSEY PARIS 162141034",
        "code": "3219110512960",
        "price_birr": 22845.02,
    },

    {
        "name": "LU DELSEY PARIS 162211500",
        "code": "3219110540642",
        "price_birr": 10078.93,
    },

    {
        "name": "LU DELSEY PARIS 162211534",
        "code": "3219110540673",
        "price_birr": 11026.00,
    },

    {
        "name": "LU DELSEY PARIS 163262002",
        "code": "3219110534085",
        "price_birr": 17650.63,
    },

    {
        "name": "LU DELSEY PARIS 163262013",
        "code": "3219110534122",
        "price_birr": 19006.62,
    },

    {
        "name": "LU DELSEY PARIS 167611506",
        "code": "3219110507171",
        "price_birr": 15845.73,
    },

    {
        "name": "LU DELSEY PARIS 167611515",
        "code": "3219110505900",
        "price_birr": 14730.51,
    },

    {
        "name": "LU DELSEY PARIS 167640206",
        "code": "3219110508130",
        "price_birr": 6238.46,
    },

    {
        "name": "LU DELSEY PARIS 167660322",
        "code": "3219110536751",
        "price_birr": 19830.23,
    },

    {
        "name": "LU DELSEY PARIS 167680106",
        "code": "3219110503692",
        "price_birr": 45264.57,
    },

    {
        "name": "LU DELSEY PARIS 167680115",
        "code": "3219110503708",
        "price_birr": 46460.14,
    },

    {
        "name": "LU DELSEY PARIS 202061002",
        "code": "3219110486131",
        "price_birr": 11807.87,
    },

    {
        "name": "LU DELSEY PARIS 202061004",
        "code": "3219110486339",
        "price_birr": 13005.47,
    },

    {
        "name": "LU DELSEY PARIS 202061013",
        "code": "3219110486469",
        "price_birr": 11737.49,
    },

    {
        "name": "LU DELSEY PARIS 202061015",
        "code": "3219110486322",
        "price_birr": 11737.51,
    },

    {
        "name": "LU DELSEY PARIS 218180113",
        "code": "3219110523560",
        "price_birr": 29194.62,
    },

    {
        "name": "LU DELSEY PARIS 218180121",
        "code": "3219110523577",
        "price_birr": 29788.55,
    },

    {
        "name": "LU DELSEY PARIS 218180125",
        "code": "TEST-NOTFOUND-3219110523553",
        "price_birr": 29788.55,
    },

    {
        "name": "LU DELSEY PARIS 287845100",
        "code": "3219110533095",
        "price_birr": 22220.50,
    },

    {
        "name": "LU DELSEY PARIS 287845103",
        "code": "3219110533101",
        "price_birr": 24534.12,
    },

    {
        "name": "LU DELSEY PARIS 287845114",
        "code": "3219110533118",
        "price_birr": 24541.05,
    },

    {
        "name": "LU DELSEY PARIS 287880203",
        "code": "3219110531077",
        "price_birr": 27072.16,
    },

    {
        "name": "LU DELSEY PARIS 287880214",
        "code": "3219110531084",
        "price_birr": 27787.24,
    },

    {
        "name": "LU DELSEY PARIS 287880403",
        "code": "3219110531039",
        "price_birr": 27072.16,
    },

    {
        "name": "LU DELSEY PARIS 333540300",
        "code": "3219110510416",
        "price_birr": 6209.19,
    },

    {
        "name": "LU DELSEY PARIS 333540500",
        "code": "3219110510867",
        "price_birr": 8066.68,
    },

    {
        "name": "LU DELSEY PARIS 333540702",
        "code": "3219110510126",
        "price_birr": 11278.32,
    },

    {
        "name": "LU DELSEY PARIS 335411100",
        "code": "3219110436198",
        "price_birr": 3064.73,
    },

    {
        "name": "LU DELSEY PARIS 335411300",
        "code": "3219110436556",
        "price_birr": 5409.48,
    },

    {
        "name": "LU DELSEY PARIS 343015000",
        "code": "3219110527971",
        "price_birr": 2905.08,
    },

    {
        "name": "LU DELSEY PARIS 343015003",
        "code": "3219110527988",
        "price_birr": 2905.28,
    },

    {
        "name": "LU DELSEY PARIS 343015004",
        "code": "3219110527964",
        "price_birr": 3128.28,
    },

    {
        "name": "LU DELSEY PARIS 343031000",
        "code": "3219110528213",
        "price_birr": 5928.75,
    },

    {
        "name": "LU DELSEY PARIS 343031004",
        "code": "3219110528206",
        "price_birr": 5929.14,
    },

    {
        "name": "LU DELSEY PARIS 343061000",
        "code": "3219110535686",
        "price_birr": 7706.05,
    },

    {
        "name": "LU DELSEY PARIS 381322001",
        "code": "3219110504606",
        "price_birr": 16529.25,
    },

    {
        "name": "LU DELSEY PARIS 381341000",
        "code": "3219110524536",
        "price_birr": 10394.88,
    },

    {
        "name": "LU DELSEY PARIS 381341001",
        "code": "TEST-NOTFOUND-3219110504668",
        "price_birr": 10394.88,
    },

    {
        "name": "LU DELSEY PARIS 381341002",
        "code": "3219110504675",
        "price_birr": 10394.88,
    },

    {
        "name": "LU DELSEY PARIS 381341004",
        "code": "3219110504682",
        "price_birr": 11489.11,
    },

    {
        "name": "LU DELSEY PARIS 391061010",
        "code": "3219110502015",
        "price_birr": 4765.46,
    },

    {
        "name": "LU DELSEY PARIS 394416100",
        "code": "3219110420418",
        "price_birr": 7410.46,
    },

    {
        "name": "LU DELSEY PARIS 394465911",
        "code": "3219110490022",
        "price_birr": 17867.12,
    },

    {
        "name": "LU DOSE OF CHECK DEUX DLXS BACKPACK",
        "code": "910B7666NSZ",
        "price_birr": 10064.08,
    },

    {
        "name": "LU DOSE OF CHECK DEUX MONTE CARLO",
        "code": "910B8014NSZ",
        "price_birr": 13977.87,
    },

    {
        "name": "LU DRIPPY GRAFFITI FLORAL DLXR BACKPACK",
        "code": "91087701NSZ",
        "price_birr": 7268.49,
    },

    {
        "name": "LU ECO MIETTA SML SOCIE-BLA",
        "code": "190231872665",
        "price_birr": 18147.87,
    },

    {
        "name": "LU EMINENT PS TROLLEY20 KF16",
        "code": "LU10",
        "price_birr": 3326.74,
    },

    {
        "name": "LU EVERLEE NOEL TOTE",
        "code": "190231966746",
        "price_birr": 18843.38,
    },

    {
        "name": "LU EVERLEE NOEL TOTE-2",
        "code": "190231966753",
        "price_birr": 18843.38,
    },

    {
        "name": "LU EVIL EYE DRIP CHECK DLSXV BACKPACK",
        "code": "910B7700NSZ",
        "price_birr": 8945.85,
    },

    {
        "name": "LU Eco  Tex  4pc  C‹xnpressiblo  Pacing  Cube  SeI-Gr£'en  Moss-",
        "code": "665556056996",
        "price_birr": 4295.63,
    },

    {
        "name": "LU Eco Tex  4pc Comprassible  Packing CcJbo  Set-Black  Onyx-O/S",
        "code": "665556056972",
        "price_birr": 4295.63,
    },

    {
        "name": "LU FASHION KITTY LITARR DLXSV BACKPACK",
        "code": "910B7757NSZ",
        "price_birr": 8945.85,
    },

    {
        "name": "LU FLY KNIT MOUTH MESSENGER SLING",
        "code": "910B8026NSZ",
        "price_birr": 7827.62,
    },

    {
        "name": "LU Fashion  Rectangle  Shape  Luggage  &  Mini  C/aso-Gray  (RT- ST-GY02-22AR)-O/S",
        "code": "665556049370",
        "price_birr": 6264.45,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME SUNGLASS- AC",
        "code": "8053672879155",
        "price_birr": 20617.64,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME SUNGLASS- AC-1",
        "code": "TEST-NOTFOUND-8056597725156",
        "price_birr": 18155.14,
    },

    {
        "name": "JW ACETATE MAN OPTICAL FRAME SUNGLASS- AC-PERSOL     0PO3007VM",
        "code": "8056597057486",
        "price_birr": 19963.01,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS  -AC-IMPERIO ARMANI     0EA4186",
        "code": "8056597765183",
        "price_birr": 14603.04,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS  -AC-POLO RALPH LAUREN     0PP9504U",
        "code": "8056597597029",
        "price_birr": 8664.46,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC",
        "code": "8053672303216",
        "price_birr": 21181.81,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-1",
        "code": "8056262240908",
        "price_birr": 25014.78,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-2",
        "code": "8056597949958",
        "price_birr": 27220.62,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-3",
        "code": "8056597821056",
        "price_birr": 16801.62,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-4",
        "code": "8053672400106",
        "price_birr": 20128.54,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-PERSOL     0PO0649",
        "code": "713132003558",
        "price_birr": 22862.81,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-PERSOL     0PO0714",
        "code": "713132439968",
        "price_birr": 20799.62,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-PERSOL     0PO3048S",
        "code": "8053672054804",
        "price_birr": 20616.60,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-PERSOL     0PO3152S",
        "code": "8056597149006",
        "price_birr": 21420.79,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-PERSOL     0PO9649S",
        "code": "8053672129397",
        "price_birr": 23325.56,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-VOGUE     0VO5327S",
        "code": "8056597450461",
        "price_birr": 10375.99,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS - AC-VOGUR     0VO5328S",
        "code": "8056597209236",
        "price_birr": 10171.86,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS AC",
        "code": "8053672895575",
        "price_birr": 27315.03,
    },

    {
        "name": "JW ACETATE MAN SUNGLASS AC-1",
        "code": "8056597450492/8056597450461",
        "price_birr": 10448.05,
    },

    {
        "name": "JW ACETATE UNISEX SUNGLASS  - AC-PERSOL     0PO3292S",
        "code": "8056597808231",
        "price_birr": 29991.35,
    },

    {
        "name": "JW ACETATE UNISEX SUNGLASS  - AC-PERSOL     0PO3302S",
        "code": "8056597745239",
        "price_birr": 29988.57,
    },

    {
        "name": "JW ACETATE UNISEX SUNGLASS  - AC-PERSOL     0PO3306S",
        "code": "TEST-NOTFOUND-8056597744980",
        "price_birr": 23323.60,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC",
        "code": "8056597344814",
        "price_birr": 20126.11,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-- MIU MIU     0MU 09WS",
        "code": "8056597671927",
        "price_birr": 33317.04,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-1",
        "code": "8056597787222",
        "price_birr": 19167.26,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-10",
        "code": "8056262555248",
        "price_birr": 25206.06,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-11",
        "code": "8056597371889",
        "price_birr": 21181.81,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-12",
        "code": "8056262195215",
        "price_birr": 22043.80,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-13",
        "code": "8056597875837",
        "price_birr": 22043.80,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-14",
        "code": "8056597755610",
        "price_birr": 30191.58,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-15",
        "code": "8056262675403",
        "price_birr": 23193.95,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-16",
        "code": "8056597952934",
        "price_birr": 16041.89,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-17",
        "code": "8056597844529",
        "price_birr": 23193.94,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-18",
        "code": "8056262721810/8056262721827/8056597844642/8056597844659",
        "price_birr": 23193.94,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-19",
        "code": "8056262664360/8056262664377",
        "price_birr": 54400.05,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-2",
        "code": "8056597597203",
        "price_birr": 21181.81,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-20",
        "code": "8056597819619",
        "price_birr": 15804.04,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-21",
        "code": "8056597819626",
        "price_birr": 15804.04,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-22",
        "code": "8056262714928",
        "price_birr": 18900.91,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-23",
        "code": "8056262714942",
        "price_birr": 18900.91,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-24",
        "code": "8056262407974",
        "price_birr": 33545.12,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-25",
        "code": "TEST-NOTFOUND-8056262407967",
        "price_birr": 33545.12,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-26",
        "code": "8056262407943",
        "price_birr": 33545.12,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-27",
        "code": "8056262407950",
        "price_birr": 33545.12,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-28",
        "code": "8056262660560",
        "price_birr": 37380.51,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-29",
        "code": "8056262660409",
        "price_birr": 37378.09,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-3",
        "code": "8056597597210",
        "price_birr": 21181.81,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-30",
        "code": "8056262660423",
        "price_birr": 37378.09,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-31",
        "code": "8056262660416",
        "price_birr": 37380.51,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-32",
        "code": "8056597764193",
        "price_birr": 25206.06,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-33",
        "code": "8056262420942",
        "price_birr": 21181.81,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-34",
        "code": "8056262551790",
        "price_birr": 14273.19,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-35",
        "code": "8053672918557",
        "price_birr": 10448.06,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-36",
        "code": "805289351344",
        "price_birr": 10448.05,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-4",
        "code": "8056597924085",
        "price_birr": 25206.06,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-5",
        "code": "8056597924092",
        "price_birr": 25206.06,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-6",
        "code": "8056597924115",
        "price_birr": 25206.06,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-7",
        "code": "8056597923996/8056597924009",
        "price_birr": 35269.10,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-8",
        "code": "8056262555279",
        "price_birr": 25206.06,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-9",
        "code": "8056262555262/8056262555255",
        "price_birr": 25206.06,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-BURBERRY     0BE4160",
        "code": "8053672163469",
        "price_birr": 18324.53,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-BURBERRY     0BE4216",
        "code": "TEST-NOTFOUND-8053672556858",
        "price_birr": 19240.17,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-BURBERRY     0BE4344",
        "code": "8056597488556",
        "price_birr": 23035.51,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-MIU MIU     0MU 01YS",
        "code": "8056597782418",
        "price_birr": 33314.25,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-MIU MIU     0MU 09WS",
        "code": "8056597671934",
        "price_birr": 33314.25,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-VERSACE     0VE4437U",
        "code": "8056597708296",
        "price_birr": 24840.61,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-VOGUE     0VO5338S",
        "code": "8056597215879",
        "price_birr": 10375.99,
    },

    {
        "name": "JW ACETATE WOMAN SUNGLASS - AC-VOGUE     0VO5409S",
        "code": "8056597519496",
        "price_birr": 10376.77,
    },

    {
        "name": "JW ADIDAS SPORT DISPLAY 4PC  ADIDAS  ASP20PDISP4PC-FC",
        "code": "SUNGLASS DISPLAY",
        "price_birr": 2364.23,
    },

    {
        "name": "JW ADIDAS SPORT LOGOPLAQUE  ADIDAS  ASP20PPLAQUE0-FC",
        "code": "SUNGLASS DISPLAY",
        "price_birr": 3152.29,
    },

    {
        "name": "JW BURBERRY m-OBE4308F-SUNGLASS",
        "code": "8056597422512",
        "price_birr": 19169.68,
    },

    {
        "name": "JW INJECTED MAN OPTICAL FRAME  SUNGLASS- PT-ARNETTI      0AN7219",
        "code": "7895653243699",
        "price_birr": 3239.17,
    },

    {
        "name": "JW INJECTED MAN OPTICAL FRAME SUNGLASS- PT",
        "code": "888392577276",
        "price_birr": 14213.23,
    },

    {
        "name": "JW INJECTED MAN SUNGLASS",
        "code": "888392584502",
        "price_birr": 7527.92,
    },

    {
        "name": "JW INJECTED MAN SUNGLASS- PT",
        "code": "7895653231443",
        "price_birr": 9402.03,
    },

    {
        "name": "JW INJECTED MAN SUNGLASS- PT- IMPERIO ARMANI     0EA4160",
        "code": "8056597445375",
        "price_birr": 16687.54,
    },

    {
        "name": "JW INJECTED MAN SUNGLASS- PT-1",
        "code": "7895653261365",
        "price_birr": 11402.05,
    },

    {
        "name": "JW INJECTED MAN SUNGLASS- PT-10",
        "code": "8056597659086",
        "price_birr": 15804.04,
    },

    {
        "name": "JW INJECTED MAN SUNGLASS- PT-11",
        "code": "8056597207812",
        "price_birr": 25206.06,
    },

    {
        "name": "JW INJECTED MAN SUNGLASS- PT-12",
        "code": "8056597949613",
        "price_birr": 30191.58,
    },

    {
        "name": "CO SPIDERMAN EDT SET",
        "code": "8411114097114",
        "price_birr": 3150.34,
    },

    {
        "name": "TO 1000-Piece Africa Puzzle",
        "code": "TEST-NOTFOUND-6001651197020",
        "price_birr": 13775.05,
    },

    {
        "name": "TO 5PCS Die Cast Car",
        "code": "BBZ6296667136273",
        "price_birr": 3595.94,
    },

    {
        "name": "TO 6 INCH VALUE FIGURE 3-PACK",
        "code": "5010993777419",
        "price_birr": 2094.66,
    },

    {
        "name": "TO 8 PACK - NEON COLORS",
        "code": "5010993560196/5010993560189",
        "price_birr": 1605.68,
    },

    {
        "name": "TO AFRICA Trivia Card Game",
        "code": "6001651172379",
        "price_birr": 5247.63,
    },

    {
        "name": "TO AIRPLANE EXPLORER STARTER SET",
        "code": "5010996201423",
        "price_birr": 2555.90,
    },

    {
        "name": "TO AURORA BLACK TIP SHARK 15\"35017",
        "code": "5034566350175",
        "price_birr": 1689.06,
    },

    {
        "name": "TO AURORA BT21 CHIMMY K",
        "code": "5034566613331",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA BT21 CHIMMY PALM PAL 5IN",
        "code": "5034566615045",
        "price_birr": 1064.47,
    },

    {
        "name": "TO AURORA BT21 CHIMMY PLUSH SM",
        "code": "5034566614574",
        "price_birr": 1770.12,
    },

    {
        "name": "TO AURORA BT21 COOKY BABY 5IN",
        "code": "5034566614796",
        "price_birr": 1008.35,
    },

    {
        "name": "TO AURORA BT21 COOKY K",
        "code": "5034566613348",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA BT21 COOKY PALM PAL 5IN",
        "code": "5034566615106",
        "price_birr": 1770.12,
    },

    {
        "name": "TO AURORA BT21 COOKY PLUSH SM",
        "code": "5034566614581",
        "price_birr": 1770.12,
    },

    {
        "name": "TO AURORA BT21 INSIDE MANG PLUSH SM",
        "code": "5034566615755",
        "price_birr": 1638.57,
    },

    {
        "name": "TO AURORA BT21 KOYA BABY 5IN",
        "code": "5034566614840",
        "price_birr": 1638.57,
    },

    {
        "name": "TO AURORA BT21 KOYA K",
        "code": "5034566613362",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA BT21 KOYA PALM PAL 5IN",
        "code": "5034566615076",
        "price_birr": 1064.47,
    },

    {
        "name": "TO AURORA BT21 KOYA PLUSH SM",
        "code": "5034566614604",
        "price_birr": 1770.12,
    },

    {
        "name": "TO AURORA BT21 MANG K",
        "code": "5034566613386",
        "price_birr": 1064.47,
    },

    {
        "name": "TO AURORA BT21 MANG PALM PAL 5IN",
        "code": "TEST-NOTFOUND-5034566615083",
        "price_birr": 1064.47,
    },

    {
        "name": "TO AURORA BT21 MANG PLUSH SM",
        "code": "5034566614611",
        "price_birr": 1770.12,
    },

    {
        "name": "TO AURORA BT21 RJ BABY 5IN",
        "code": "5034566614802",
        "price_birr": 1638.57,
    },

    {
        "name": "TO AURORA BT21 RJ K",
        "code": "5034566613324",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA BT21 RJ PALM PAL 5IN",
        "code": "5034566615052",
        "price_birr": 1064.47,
    },

    {
        "name": "TO AURORA BT21 RJ PLUSH SM",
        "code": "5034566614567",
        "price_birr": 1770.12,
    },

    {
        "name": "TO AURORA BT21 SHOOKY BABY 5IN",
        "code": "5034566614826",
        "price_birr": 1638.57,
    },

    {
        "name": "TO AURORA BT21 SHOOKY K",
        "code": "5034566613379",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA BT21 SHOOKY PALM PAL 5IN",
        "code": "5034566615090",
        "price_birr": 1770.12,
    },

    {
        "name": "TO AURORA BT21 SHOOKY PLUSH SM",
        "code": "5034566614628",
        "price_birr": 1638.57,
    },

    {
        "name": "TO AURORA BT21 TATA BABY 5IN",
        "code": "5034566614819",
        "price_birr": 1008.35,
    },

    {
        "name": "TO AURORA BT21 TATA K",
        "code": "5034566613355",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA BT21 TATA PALM PAL 5IN",
        "code": "5034566615069",
        "price_birr": 1064.47,
    },

    {
        "name": "TO AURORA BT21 TATA PLUSH SM",
        "code": "5034566614598",
        "price_birr": 1770.12,
    },

    {
        "name": "TO AURORA BT21 VAN K",
        "code": "5034566613393",
        "price_birr": 1064.47,
    },

    {
        "name": "TO AURORA BT21 VAN PALM PAL 5IN",
        "code": "5034566615113",
        "price_birr": 1064.47,
    },

    {
        "name": "TO AURORA BT21 VAN PLUSH SM",
        "code": "5034566614635",
        "price_birr": 1770.12,
    },

    {
        "name": "TO AURORA DESTINATION NATION GY PENGUIN 11IN",
        "code": "5034566192737",
        "price_birr": 1889.67,
    },

    {
        "name": "TO AURORA DN AFRICAN PENGUIN 12IN",
        "code": "5034566806733",
        "price_birr": 1419.09,
    },

    {
        "name": "TO AURORA ECO NATION CAMEL 12L",
        "code": "5034566615373",
        "price_birr": 1494.10,
    },

    {
        "name": "TO AURORA ECO NATION DESTINATION NATION PANDA 11IN",
        "code": "TEST-NOTFOUND-5034566192638",
        "price_birr": 1889.67,
    },

    {
        "name": "TO AURORA ECO NATION DISPLAY STAND (DISPLAY)",
        "code": "DISPLAY",
        "price_birr": 2487.60,
    },

    {
        "name": "TO AURORA ECO NATION DOLPHIN 15IN",
        "code": "5034566350205",
        "price_birr": 1535.07,
    },

    {
        "name": "TO AURORA ECO NATION HIPPOPOTAMUS 10.5IN",
        "code": "5034566350342",
        "price_birr": 1889.67,
    },

    {
        "name": "TO AURORA ECO NATION LLAMA TAN 11IN",
        "code": "5034566350380",
        "price_birr": 2165.53,
    },

    {
        "name": "TO AURORA ECO NATION POLAR BEAR 9.5IN",
        "code": "5034566350304",
        "price_birr": 2144.70,
    },

    {
        "name": "TO AURORA ECO NATION REXTER T-REX 8IN",
        "code": "5034566350557",
        "price_birr": 1889.65,
    },

    {
        "name": "TO AURORA ECO NATION RHINOCEROS 9.5IN",
        "code": "5034566350236",
        "price_birr": 2107.46,
    },

    {
        "name": "TO AURORA ECO NATION STEGGY STEGOSAURUS 8IN",
        "code": "5034566350588",
        "price_birr": 1889.67,
    },

    {
        "name": "TO AURORA ECO NATION TEDDY BEAR 9IN",
        "code": "5034566615120",
        "price_birr": 1572.84,
    },

    {
        "name": "TO AURORA ECO NATION TRIX TRICERATOPS 8IN",
        "code": "5034566350571",
        "price_birr": 1162.87,
    },

    {
        "name": "TO AURORA HAPEE RED PANDA 6IN",
        "code": "5034566611030",
        "price_birr": 1201.75,
    },

    {
        "name": "TO AURORA HEART EYES SMILEY PALM PALS 5IN",
        "code": "5034566443037",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA MANGO FLAMINGO 6IN",
        "code": "5034566611115",
        "price_birr": 1099.23,
    },

    {
        "name": "TO AURORA MF MINI CAMEL 8IN",
        "code": "5034566317260",
        "price_birr": 988.06,
    },

    {
        "name": "TO AURORA MF MINI EMPEROR PENGUIN 8IN",
        "code": "5034566311947",
        "price_birr": 897.33,
    },

    {
        "name": "TO AURORA PLUSH ECO NATION SEAL 12IN",
        "code": "5034566350144",
        "price_birr": 1889.67,
    },

    {
        "name": "TO AURORA PLUSH ECO NATION STINGRAY 12IN",
        "code": "5034566350199",
        "price_birr": 1889.65,
    },

    {
        "name": "TO AURORA PP ALICE SAPPHIRE 5IN",
        "code": "5034566338425",
        "price_birr": 1267.64,
    },

    {
        "name": "TO AURORA PP AUBREY EGGPLANT 5IN",
        "code": "5034566337855",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP BARTLETT PEAR 5IN",
        "code": "TEST-NOTFOUND-5034566339125",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP CHEERFUL CARROT 5IN",
        "code": "5034566820548",
        "price_birr": 1258.80,
    },

    {
        "name": "TO AURORA PP DILLIAN CUCUMBER 5IN",
        "code": "5034566337916",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP FLAPJACK STINGRAY 5IN",
        "code": "5034566337237",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP LIL SPOTS LADYBIRD 5IN",
        "code": "5034566820593",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP MELLOW PEACH 5IN",
        "code": "5034566335707",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP OLIVER OCTOPUS 5IN",
        "code": "5034566336810",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP PAUL PIANO 5IN",
        "code": "5034566615984",
        "price_birr": 1249.90,
    },

    {
        "name": "TO AURORA PP PEPPA PIZZA SLICE 5IN",
        "code": "5034566336889",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP PERKY PINEAPPLE 5IN",
        "code": "5034566335714",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP PINK DIAMOND 5IN",
        "code": "5034566616035",
        "price_birr": 803.08,
    },

    {
        "name": "TO AURORA PP RIBBITS FROG 5IN",
        "code": "5034566337206",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP ROMAN RULER 5IN",
        "code": "5034566616004",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP SCALES ALLIGATOR 5IN",
        "code": "5034566336865",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP STRIKER FOOTBALL 5IN",
        "code": "5034566338692",
        "price_birr": 1738.61,
    },

    {
        "name": "TO AURORA PP SUHIRO SALMON SUSHI 5IN",
        "code": "5034566615953",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP SUMMER CLOUD 5IN",
        "code": "5034566335769",
        "price_birr": 1208.00,
    },

    {
        "name": "TO AURORA PP TENNIS ACE 5IN",
        "code": "5034566338685",
        "price_birr": 801.32,
    },

    {
        "name": "TO AURORA PP TIKE PENCIL 5IN",
        "code": "5034566338913",
        "price_birr": 1290.52,
    }

]

# ============================================================
# 4. TEST HELPERS
# ============================================================

def generate_external_code(product, transaction_number, line_number):
    """
    Usually return the REAL product code.

    Occasionally return a deliberately modified code.

    This allows you to test:
        - exact product-code matches
        - unknown product codes
        - POS data anomalies
    """

    original_code = product["code"]

    # 80% exact real code
    if random.random() < 0.80:
        return original_code

    # 20% deliberately modified code
    #
    # Keep the product name correct while changing the code.
    # This is useful for testing product resolution.
    return f"TEST-{transaction_number:03d}-{line_number:02d}-{original_code}"


def generate_quantity():
    """
    Mostly sell 1 item, occasionally 2-5.
    """

    return random.choices(
        [1, 2, 3, 4, 5],
        weights=[55, 25, 10, 7, 3],
        k=1,
    )[0]


def generate_sale_price_usd(price_birr, exchange_rate):
    """
    Convert Birr price to USD.

    Example:

        15,000 Birr / 170 = 88.24 USD
    """

    price_usd = price_birr / exchange_rate

    return round(price_usd, 2)


# ============================================================
# 5. CREATE TRANSACTION
# ============================================================

def create_transaction(transaction_data):

    url = (
        f"{ODOO_URL}"
        f"/json/2/bk.sales.transaction/create"
    )

    response = requests.post(
        url,
        headers=HEADERS,
        json={
            "vals_list": [
                transaction_data
            ]
        },
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    # Odoo JSON-2 create normally returns IDs.
    #
    # Depending on your endpoint response, it may be:
    #
    # [123]
    #
    # or:
    #
    # 123
    #

    if isinstance(result, list):

        if not result:
            raise Exception(
                "Odoo returned an empty ID list."
            )

        return result[0]

    return result


# ============================================================
# 6. CREATE SALES LINE
# ============================================================

def create_sales_line(transaction_id, line_data):

    url = (
        f"{ODOO_URL}"
        f"/json/2/bk.sales.order.line/create"
    )

    values = dict(line_data)

    # IMPORTANT:
    #
    # This connects the line to the transaction.
    #
    values["transaction_id"] = transaction_id

    response = requests.post(
        url,
        headers=HEADERS,
        json={
            "vals_list": [
                values
            ]
        },
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if isinstance(result, list):

        if not result:
            raise Exception(
                "Odoo returned an empty sales-line ID list."
            )

        return result[0]

    return result


# ============================================================
# 7. BUILD ONE TRANSACTION
# ============================================================

def build_transaction(transaction_number):

    transaction_ref = (
        f"POS-LOAD-{transaction_number:06d}"
    )

    # Each transaction gets a random exchange rate.
    exchange_rate = round(
        random.uniform(
            MIN_USD_ETB_RATE,
            MAX_USD_ETB_RATE,
        ),
        2,
    )

    issued_datetime = (
        START_DATE
        + timedelta(
            minutes=transaction_number * 3
        )
    )

    sale_date = issued_datetime.strftime(
        "%Y-%m-%d"
    )

    issued_string = issued_datetime.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Number of lines for THIS transaction.
    number_of_lines = random.randint(
        MIN_LINES_PER_TRANSACTION,
        MAX_LINES_PER_TRANSACTION,
    )

    # Make sure we do not select the same product twice
    # inside one transaction.
    selected_products = random.sample(
        PRODUCTS,
        number_of_lines,
    )

    lines = []

    subtotal = 0.0

    # --------------------------------------------------------
    # Build individual lines first.
    # --------------------------------------------------------

    for line_number, product in enumerate(
        selected_products,
        start=1,
    ):

        quantity = generate_quantity()

        external_code = generate_external_code(
            product,
            transaction_number,
            line_number,
        )

        unit_price_usd = generate_sale_price_usd(
            product["price_birr"],
            exchange_rate,
        )

        line_total = (
            unit_price_usd
            * quantity
        )

        subtotal += line_total

        lines.append(
            {
                "external_code": external_code,
                "external_name": product["name"],
                "date": sale_date,

                "sold_qty": quantity,

                "unit_price": unit_price_usd,

            }
        )

    tax_total = round(
        subtotal * 0.15,
        2,
    )

    grand_total = round(
        subtotal + tax_total,
        2,
    )

    transaction = {

        "external_ref": transaction_ref,
        "pos_source_id": 3,
        "device_name": (
            f"POS-{random.randint(1, 10):02d}"
        ),

        "fs_number": (
            f"FS-{transaction_number:06d}"
        ),

        "shift_number": (
            f"SHIFT-{random.randint(1, 20):03d}"
        ),

        # "issued_datetime": issued_string,

        "user_name": random.choice(
            [
                "John",
                "Sarah",
                "Michael",
                "Helen",
                "Daniel",
                "Abel",
            ]
        ),

        "customer_name": random.choice(
            [
                "Walk-in Customer",
                "Test Customer",
                "Customer A",
                "Customer B",
                "Retail Customer",
            ]
        ),

        "date": sale_date,

        "subtotal": round(
            subtotal,
            2,
        ),

        "tax_total": tax_total,

        "grand_total": grand_total,

        # ----------------------------------------------------
        # IMPORTANT CURRENCY INFORMATION
        # ----------------------------------------------------

        "currency_code": TRANSACTION_CURRENCY,

        "base_currency_rate": exchange_rate,

        # sales / return / void
        #
        # Most are sales.
        # A small percentage are returns.
        # We do not generate void here by default.
        "sales_type": random.choices(
            [
                "sales",
                "return",
            ],
            weights=[
                95,
                5,
            ],
            k=1,
        )[0],

        "imported": True,
    }

    return transaction, lines, exchange_rate


# ============================================================
# 8. CREATE ONE COMPLETE TRANSACTION
# ============================================================

def create_complete_transaction(transaction_number):

    transaction_data, lines_data, exchange_rate = (
        build_transaction(
            transaction_number
        )
    )

    print()
    print("=" * 80)
    print(
        f"TRANSACTION {transaction_number}/{NUMBER_OF_TRANSACTIONS}"
    )
    print("=" * 80)

    print(
        "Reference      :",
        transaction_data["external_ref"],
    )

    print(
        "Currency       :",
        transaction_data["currency_code"],
    )

    print(
        "USD -> ETB     :",
        transaction_data["base_currency_rate"],
    )

    print(
        "Sales Type     :",
        transaction_data["sales_type"],
    )

    print(
        "Number of lines:",
        len(lines_data),
    )

    # --------------------------------------------------------
    # STEP 1
    # Create header
    # --------------------------------------------------------

    print()
    print("Creating transaction header...")

    transaction_id = create_transaction(
        transaction_data
    )

    print(
        "Transaction ID :",
        transaction_id,
    )

    # --------------------------------------------------------
    # STEP 2
    # Create lines belonging to this transaction
    # --------------------------------------------------------

    created_line_ids = []

    for line_number, line_data in enumerate(
        lines_data,
        start=1,
    ):

        print(
            f"  Creating line "
            f"{line_number}/{len(lines_data)}: "
            f"{line_data['external_name']}"
        )

        line_id = create_sales_line(
            transaction_id,
            line_data,
        )

        created_line_ids.append(
            line_id
        )

    print()
    print(
        "Created line IDs:",
        created_line_ids,
    )

    return {
        "transaction_id": transaction_id,
        "transaction_ref": transaction_data[
            "external_ref"
        ],
        "expected_lines": len(lines_data),
        "line_ids": created_line_ids,
        "exchange_rate": exchange_rate,
        "sales_type": transaction_data[
            "sales_type"
        ],
    }


# ============================================================
# 9. READ TRANSACTION
# ============================================================

def read_transaction(transaction_id):

    url = (
        f"{ODOO_URL}"
        f"/json/2/bk.sales.transaction/read"
    )

    response = requests.post(
        url,
        headers=HEADERS,
        json={
            "ids": [
                transaction_id
            ],

            "fields": [
                "id",
                "name",
                "external_ref",
                "currency_code",
                "base_currency_rate",
                "sales_type",
                "line_ids",
                "line_count",
            ],
        },
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if not result:
        return None

    if isinstance(result, list):
        return result[0]

    return result


# ============================================================
# 10. VERIFY ONE TRANSACTION
# ============================================================

def verify_transaction(transaction_id):

    transaction = read_transaction(
        transaction_id
    )

    if not transaction:

        return {
            "ok": False,
            "reason": "Transaction could not be read",
        }

    line_ids = transaction.get(
        "line_ids",
        [],
    )

    line_count = transaction.get(
        "line_count",
        0,
    )

    return {
        "ok": True,
        "transaction_id": transaction_id,
        "external_ref": transaction.get(
            "external_ref"
        ),
        "currency_code": transaction.get(
            "currency_code"
        ),
        "base_currency_rate": transaction.get(
            "base_currency_rate"
        ),
        "sales_type": transaction.get(
            "sales_type"
        ),
        "line_ids": line_ids,
        "line_count": line_count,
    }


# ============================================================
# 11. MAIN LOAD TEST
# ============================================================

def main():

    print()
    print("=" * 80)
    print("ODOO POS LOAD TEST")
    print("=" * 80)

    print(
        "Odoo URL       :",
        ODOO_URL,
    )

    print(
        "Database       :",
        ODOO_DB,
    )

    print(
        "Transactions   :",
        NUMBER_OF_TRANSACTIONS,
    )

    print(
        "Lines/transaction:",
        MIN_LINES_PER_TRANSACTION,
        "to",
        MAX_LINES_PER_TRANSACTION,
    )

    print(
        "Currency       :",
        TRANSACTION_CURRENCY,
    )

    print(
        "USD -> ETB     :",
        MIN_USD_ETB_RATE,
        "to",
        MAX_USD_ETB_RATE,
    )

    print(
        "Products       :",
        len(PRODUCTS),
    )

    print()
    print(
        "Starting test..."
    )

    successful_transactions = 0
    failed_transactions = 0

    total_lines_created = 0

    results = []

    # --------------------------------------------------------
    # CREATE 100 DIFFERENT TRANSACTIONS
    # --------------------------------------------------------

    for transaction_number in range(
        1,
        NUMBER_OF_TRANSACTIONS + 1,
    ):

        try:

            result = create_complete_transaction(
                transaction_number
            )

            results.append(
                result
            )

            successful_transactions += 1

            total_lines_created += len(
                result["line_ids"]
            )

            # ------------------------------------------------
            # Verify immediately.
            # ------------------------------------------------

            verification = verify_transaction(
                result["transaction_id"]
            )

            print()
            print(
                "VERIFICATION"
            )

            print(
                "  Transaction ID:",
                verification.get(
                    "transaction_id"
                ),
            )

            print(
                "  Reference     :",
                verification.get(
                    "external_ref"
                ),
            )

            print(
                "  Currency      :",
                verification.get(
                    "currency_code"
                ),
            )

            print(
                "  Exchange rate :",
                verification.get(
                    "base_currency_rate"
                ),
            )

            print(
                "  Sales type    :",
                verification.get(
                    "sales_type"
                ),
            )

            print(
                "  line_count    :",
                verification.get(
                    "line_count"
                ),
            )

            print(
                "  line_ids      :",
                verification.get(
                    "line_ids"
                ),
            )

        except Exception as error:

            failed_transactions += 1

            print()
            print(
                "!" * 80
            )

            print(
                f"FAILED TRANSACTION "
                f"{transaction_number}"
            )

            print(
                "Error type:",
                type(error).__name__,
            )

            print(
                "Error:",
                error,
            )

            print(
                "!" * 80
            )

            # Continue to next transaction.
            continue

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print()
    print("=" * 80)
    print("FINAL LOAD TEST SUMMARY")
    print("=" * 80)

    print()
    print(
        "Requested transactions :",
        NUMBER_OF_TRANSACTIONS,
    )

    print(
        "Successful transactions:",
        successful_transactions,
    )

    print(
        "Failed transactions    :",
        failed_transactions,
    )

    print(
        "Total sales lines      :",
        total_lines_created,
    )

    if successful_transactions:

        average_lines = (
            total_lines_created
            / successful_transactions
        )

        print(
            "Average lines/transaction:",
            round(
                average_lines,
                2,
            ),
        )

    print()

    print(
        "Transaction structure:"
    )

    print(
        "  Transaction 1 -> multiple possible lines"
    )

    print(
        "  Transaction 2 -> multiple possible lines"
    )

    print(
        "  Transaction 3 -> multiple possible lines"
    )

    print(
        "  ..."
    )

    print(
        f"  Transaction {NUMBER_OF_TRANSACTIONS}"
        " -> multiple possible lines"
    )

    print()

    if (
        successful_transactions
        == NUMBER_OF_TRANSACTIONS
    ):

        print(
            "SUCCESS: All 100 transactions were created."
        )

        print(
            "Each transaction has its own sales-order-line records."
        )

    elif successful_transactions > 0:

        print(
            "PARTIAL SUCCESS:"
        )

        print(
            "Some transactions were created successfully."
        )

    else:

        print(
            "FAILED:"
        )

        print(
            "No transactions were successfully created."
        )

    print()
    print("=" * 80)


# ============================================================
# 12. PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except requests.exceptions.ConnectionError as error:

        print()
        print("=" * 80)
        print("CONNECTION ERROR")
        print("=" * 80)

        print(error)

    except requests.exceptions.Timeout as error:

        print()
        print("=" * 80)
        print("TIMEOUT ERROR")
        print("=" * 80)

        print(error)

    except requests.exceptions.HTTPError as error:

        print()
        print("=" * 80)
        print("ODOO HTTP ERROR")
        print("=" * 80)

        print(error)

    except KeyboardInterrupt:

        print()
        print()
        print(
            "Test interrupted by user."
        )

    except Exception as error:

        print()
        print("=" * 80)
        print("UNEXPECTED ERROR")
        print("=" * 80)

        print(
            "Error Type:",
            type(error).__name__,
        )

        print(
            "Error:",
            error,
        )
