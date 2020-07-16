from pathlib import Path

from ivy_cms.export import collect_all

def test_should_collect_all_textual_content_objects_in_a_cms_tree():
    test_cms = Path(__file__).parent 

    found = list(collect_all(test_cms))

    assert len(found) == 2
    found_iter = iter(found)
    assert next(found_iter).name == 'sometext' 
    assert next(found_iter).name == 'textWithNonExistingValue'
    
    
