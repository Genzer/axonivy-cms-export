from inspect import cleandoc
from pathlib import Path

from ivy_cms.reader import __parse_fields, ContentObject, ContentObjectValue
from ivy_cms.reader import create_value_content_object

def test_should_parse_key_pair_to_dict():
    given_raw_keypair_line = ' '.join([
        'name={uploadButton}',
        'description={}',
        'changed={2019-06-03 09:40:09 CEST}',
        'changedby={User}',
        'visualorder={0}',
        'guid={167546A12034FF89}',
        'parentguid={}',
        'typeguid={E6AFEA2034301F66}',
        'id={}',
        'parentid={}',
        'typeid={}'
        ])

    parsed_fields = __parse_fields(given_raw_keypair_line)
    expected_fields = {
        'name' : 'uploadButton',
        'description' : '',
        'changed' : '2019-06-03 09:40:09 CEST',
        'changedby': 'User',
        'visualorder' : '0',
        'guid' : '167546A12034FF89',
        'parentguid' : '',
        'typeguid' : 'E6AFEA2034301F66',
        'id' : '',
        'parentid' : '',
        'typeid' : ''
    }
    assert parsed_fields == expected_fields

def test_should_parse_content_object_value_correctly():
    test_cms_root = Path(__file__).parent / 'cms'
    sometext = test_cms_root/ 'com' / 'ubitec' / 'sometext'
    co_meta = sometext / 'co.meta'

    content_object_value: ContentObject = create_value_content_object(test_cms_root, co_meta)
    assert content_object_value.name == 'sometext'
    assert content_object_value.path == co_meta
    assert content_object_value.uri == '/com/ubitec/sometext'
    assert content_object_value.values['de'].raw_content == 'GERMAN TEXT\n'
