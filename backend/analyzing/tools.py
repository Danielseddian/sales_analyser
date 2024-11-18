import xml.etree.ElementTree as ET
from typing import List, Dict, Union

__all__ = ['parse_xml']

from management.wrappers.safe_execute import safe_execute


@safe_execute(default_value={})
def parse_xml(xml_content: str) -> Dict[str, Union[str, List[Dict[str, Union[int, float, str]]]]]:
    """
    XML parsing and sales data extraction.

    Args:
        xml_content (str): XML content (string) to be parsed.

    Returns:
        Dict[str, Union[str, List[Dict[str, Union[int, float, str]]]]]:
        Dictionary with the following keys:
            - date (str): Reporting date.
            - products (List[Dict]): Product list with the following keys:
                - id (int): ID of the product.
                - name (str): Name of tht product.
                - quantity (int): Quantity of product sold.
                - price (float): Price of the product.
                - category (str): Category of the product.
    """
    try:
        # Parsing XML
        root = ET.fromstring(xml_content)

        # Extracting date
        report_date = root.attrib.get('date')
        if not report_date:
            raise ValueError('Attribute `date` is missing in `sales_data`.')

        # Extracting products
        products = []
        for product in root.findall('.//product'):
            product_data = {
                'id': int(product.find('id').text),
                'name': product.find('name').text,
                'quantity': int(product.find('quantity').text),
                'price': float(product.find('price').text),
                'category': product.find('category').text,
            }
            products.append(product_data)

        return {'date': report_date, 'products': products}

    except ET.ParseError as e:
        raise ValueError(f'Invalid XML format: {e}')
    except AttributeError as e:
        raise ValueError(f'Missing required elements in XML: {e}')
    except (ValueError, TypeError) as e:
        raise ValueError(f'Error parsing product data: {e}')
