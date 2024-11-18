import pytest
from analyzing.tools import parse_xml


VALID_XML = """
<sales_data date="2024-01-01">
    <products>
        <product>
            <id>1</id>
            <name>Product A</name>
            <quantity>100</quantity>
            <price>1500.00</price>
            <category>Electronics</category>
        </product>
        <product>
            <id>2</id>
            <name>Product B</name>
            <quantity>50</quantity>
            <price>300.00</price>
            <category>Books</category>
        </product>
    </products>
</sales_data>
"""

INVALID_XML_NO_DATE = """
<sales_data>
    <products>
        <product>
            <id>1</id>
            <name>Product A</name>
            <quantity>100</quantity>
            <price>1500.00</price>
            <category>Electronics</category>
        </product>
    </products>
</sales_data>
"""

INVALID_XML_MISSING_ELEMENT = """
<sales_data date="2024-01-01">
    <products>
        <product>
            <name>Product A</name>
            <quantity>100</quantity>
            <price>1500.00</price>
            <category>Electronics</category>
        </product>
    </products>
</sales_data>
"""

INVALID_XML_FORMAT = """
<sales_data date="2024-01-01">
    <products>
        <product>
            <id>1</id>
            <name>Product A</name>
            <quantity>100</quantity>
            <price>1500.00</price>
            <category>Electronics</category>
        <!-- Incorrectly closed tag -->
</sales_data>
"""


def test_parse_valid_xml():
    result = parse_xml(VALID_XML)
    assert result['date'] == "2024-01-01"
    assert len(result['products']) == 2
    assert result['products'][0] == {
        'id': 1,
        'name': "Product A",
        'quantity': 100,
        'price': 1500.00,
        'category': "Electronics"
    }


def test_parse_invalid_xml_no_date():
    with pytest.raises(ValueError, match="Attribute `date` is missing in `sales_data`."):
        parse_xml(INVALID_XML_NO_DATE)


def test_parse_invalid_xml_missing_element():
    with pytest.raises(ValueError, match="Missing required elements in XML"):
        parse_xml(INVALID_XML_MISSING_ELEMENT)


def test_parse_invalid_xml_format():
    with pytest.raises(ValueError, match="Invalid XML format"):
        parse_xml(INVALID_XML_FORMAT)


def test_parse_empty_string():
    with pytest.raises(ValueError, match="Invalid XML format"):
        parse_xml("")
