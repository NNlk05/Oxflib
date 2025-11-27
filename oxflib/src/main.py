import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Any, Dict

def element_to_dict(elem: ET.Element) -> Dict[str, Any]:
    """
    Convert an xml.etree.ElementTree.Element into a nested dictionary.

    - Child elements with the same tag become a list.
    - Attributes are added with '@' prefix.
    - Element text is added as '#text' when there are attributes or children,
      otherwise the element value is the text string directly.
    """
    node: Dict[str, Any] = {elem.tag: {} if elem.attrib or list(elem) else None}

    children = list(elem)
    if children:
        grouped: defaultdict = defaultdict(list)
        for child in children:
            child_dict = element_to_dict(child)
            for tag, value in child_dict.items():
                grouped[tag].append(value)

        node[elem.tag] = {tag: vals[0] if len(vals) == 1 else vals for tag, vals in grouped.items()}

    if elem.attrib:
        node[elem.tag].update({'@' + k: v for k, v in elem.attrib.items()})

    text = (elem.text or '').strip()
    if text:
        if children or elem.attrib:
            node[elem.tag]['#text'] = text
        else:
            node[elem.tag] = text

    return node

load = element_to_dict