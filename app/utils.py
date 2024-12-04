import xml.etree.ElementTree as Et

def parse_xml_data(body):
    """Convierte las medidas en XML en un diccionario."""
    try:
        data = Et.fromstring(body.decode('utf-8'))

        record_data = {
            "temperature": float(data.findtext('record/temperature', 0)),
            "humidity_air": float(data.findtext('record/humidity_air', 0)),
            "brightness": float(data.findtext('record/brightness', 0)),
            "ph": float(data.findtext('record/ph', 0)),
            "tds": float(data.findtext('record/tds', 0)),
            "humidity_soil": float(data.findtext('record/humidity_soil', 0)),
            "crop_id": data.findtext('crop', ''),
            "token": data.findtext('token', '')
        }

        return record_data
    except Et.ParseError as e:
        raise ValueError(f"Error parsing XML: {str(e)}")
