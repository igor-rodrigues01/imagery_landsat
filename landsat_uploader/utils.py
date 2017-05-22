
def get_data_from_landsat_image_name(image_name):

    from datetime import datetime

    """
    LXSS_LLLL_PPPRRR_YYYYMMDD_yyyymmdd_CC_TX
    L = Landsat (LC08, LE07...)
    X = Sensor = ("C", "O", "T", "E", "M")
    SS = Sattelite(05, 07, 08)
    LLLL = Processing correction level (L1TP/LIGT/L1GS)
    PPP = WRS path
    RRR = WRS row
    YYYYMMDD = Acquisition date
    yyyymmdd = Processiong date
    CC = Collection number (01, 02...)
    TX = Collection category ("RT", "T1", "T2")
    """
    list_image_name = image_name.split("_")
    
    landsat_sensor_sat = list_image_name[0]
    correction_level = list_image_name[1]
    path = list_image_name[2][:3]
    row = list_image_name[2][3:]
    acq_date = datetime.strptime(list_image_name[3],"%Y%m%d")
    prc_date = datetime.strptime(list_image_name[4],"%Y%m%d")
    c_number = list_image_name[5]
    c_category = list_image_name[6]

    return {
        "path": path,
        "row": row,
        "sat": landsat_sensor_sat,
        "date": acq_date,
        "name": image_name,
    }
