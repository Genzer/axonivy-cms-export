from dataclasses import dataclass, fields
from typing import List, Dict, Type, Set
from pathlib import Path
from enum import Enum

import re

LangId = Type[str]

class ContentType(Enum):
    """Describe the ContentType used in Axon.ivy CMS system.
    The values are the GUIDs defined in a table located in the JAR
    ch.ivyteam.ivy.cm_7.0.8.201810041409.jar.
    The file is ch/ivyteam/ivy/cm/internal/TypeTable.data.
    You can find a copy of a files in ./docs.
    """
    STRING = 'E6AFEA2034301F66'
    TEXT = 'E6AFEA202AFB4911'
    PLAIN_TEXT = 'E6AFEA1FBC44F7F7'
    FOLDER = 'E6AFEA2049948BDF'
    
    @staticmethod
    def textual_types() -> Set['ContentType']:
        return {ContentType.STRING, ContentType.TEXT, ContentType.PLAIN_TEXT} 

@dataclass
class ContentObjectValue:
    langid: str
    guid: str
    path: Path
    raw_content: str

@dataclass
class ContentObject:
    name: str = ''
    uri: str = ''
    path: Path = None
    typeguid: str = ''
    values: Dict[LangId, ContentObjectValue] = None

def __fieldnames(dataclass):
    """Returns the fields in a @dataclass"""
    return dataclass.__dataclass_fields__.keys()

def __parse_fields(raw_property: str, returns_only: dict = None) -> dict:
    """Parse a line in Axon.ivy ContentObjectData into a Python dict
    
    A key pair value is defined as key={value} in which "value" may contain spaces
    and other characters.
    """
    KEY_PAIR_PATTERN = re.compile(r'(?P<key>[a-zA-Z]+)\=\{(?P<value>.*?)\}')
    all =  dict(KEY_PAIR_PATTERN.findall(raw_property))
    return all if returns_only == None else { key : all[key] for key in returns_only if key in all}

def create_value_content_object(root_cms: Path, co_meta: Path) -> ContentObject:
    """Returns a `ContentObject` given a `Path` to the file `co.meta`.
    """
    with open(co_meta, 'r') as co_meta_file:
        fields = {}
        content_object_values: List[ContentObjectValue] = []
        for line_number, line in enumerate(co_meta_file.readlines()):
            if line_number == 0:
                # First line MUST always start with 'co: '                
                raw_properties = line.replace("co: ", "")
                defined_fields = __parse_fields(raw_properties, returns_only=__fieldnames(ContentObject))

                if defined_fields.get('typeguid') not in {c.value for c in ContentType.textual_types()}:
                    raise RuntimeError(f"{co_meta} is not a textual value type")

                fields = { 
                    **defined_fields,
                    **{
                        'path' : co_meta,
                        'uri' : '/' + str(co_meta.parent.relative_to(root_cms))
                    }
                }


            else:
                # next lines MUST starts with 'val: "
                raw_values = line.replace("val: ", "")
                defined_fields = __parse_fields(raw_values, returns_only={'guid', 'langid'})
                value_path = co_meta.parent / (defined_fields['guid'] + '.data')
                raw_content = ''
                with open(value_path, 'r', encoding='utf8') as value_file:
                    raw_content = value_file.read()

                more_fields = {
                    'raw_content' : raw_content,
                    'path' : value_path,
                }
                content_object_values.append(ContentObjectValue(**defined_fields, **more_fields)) 
        values = {
            'values' : dict({ v.langid : v for v in content_object_values })
        }
        return ContentObject(**fields, **values)

