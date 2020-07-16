from pathlib import Path
from os import walk
from typing import Generator, List, Dict, Tuple
import sys
import csv

from tablib import Dataset
from tabulate import tabulate

from ivy_cms.reader import create_value_content_object, ContentObject


def collect_all(root: Path) -> Generator[ContentObject, None, None]:
    root_cms = Path(root) / 'cms'
    for current, sub_dirs, files in walk(root_cms):
        if len(sub_dirs) == 0:
            if 'co.meta' in files:
                co_meta = Path(current) / 'co.meta'
                content_object = create_value_content_object(root_cms, co_meta)
                if content_object:
                    yield content_object

def to_dict_table(content_objects: Generator[ContentObject, None, None]) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    for entry in content_objects:
        # Name, LANG, LANG, ..., URI
        first_columns = {
            'name' : entry.name,
            'uri' : entry.uri
        }
        lang_columns = { lang : value.raw_content for lang, value in entry.values.items() }
        entries.append({ **first_columns, **lang_columns })
    return entries
        

def to_csv(root: Path):
    rows = to_dict_table(collect_all(root))
    field_names = ['name', 'de', 'en', 'fr', 'it', 'uri']
    writer = csv.DictWriter(sys.stdout, fieldnames=field_names, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)


def to_row_tuples(table: List[Dict[str, str]], columns_order: List[str] = None) -> Generator[Tuple, None, None]:
    columns = ['name', 'de', 'en', 'fr', 'it', 'uri']
    columns = columns_order or columns
    for row in table:
        d = tuple(row.get(c) for c in columns)
        yield d
    

def to_xls(root: Path, output_file: Path):
    data = Dataset()
    data.title = f"{root.name} CMS"
    data.headers = ['name', 'de', 'en', 'fr', 'it', 'uri']
    rows = to_dict_table(collect_all(root))
    
    for row in to_row_tuples(rows):
        data.append(row)
   
    if output_file is None:
        output_file = Path.cwd() / 'output.xls'

    with open(output_file, 'wb') as out:
        out.write(data.export('xls'))
    
if __name__ == "__main__":
    import argparse


    parser = argparse.ArgumentParser(description="Export Axon.ivy Project's CMS")
    parser.add_argument('project', type=Path, help="Path to the Axon.ivy Project")
    parser.add_argument('output', type=Path, default=Path.cwd() / 'output', help="Path to the output file")

    args = parser.parse_args()

    project = args.project
    output = args.output

    to_xls(project, output)


