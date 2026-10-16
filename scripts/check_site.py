"""Check project-relative HTML resources and anchors without network requests."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote


class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.links=[];self.ids=set();self.feed(text)
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if values.get('id'):self.ids.add(values['id'])
        for key in ['href','src']:
            if values.get(key):self.links.append(values[key])


def check(root):
    pages={path:Page(path.read_text()) for path in root.rglob('*.html')
           if not any(part.startswith('.') or part in {'data','build','artifacts','node_modules'} for part in path.relative_to(root).parts)}
    count=0
    for path,page in pages.items():
        for link in page.links:
            url=urlsplit(link)
            if url.scheme or url.netloc:continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            if not target.is_relative_to(root) or not target.is_file():
                raise ValueError(f'{path.relative_to(root)}: missing/outside resource {link}')
            if url.fragment and target.suffix=='.html':
                parsed=pages.get(target) or Page(target.read_text())
                if unquote(url.fragment) not in parsed.ids:raise ValueError(f'Missing anchor: {link}')
            count+=1
    print(f'{len(pages)} pages; {count} relative resources/anchors verified')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    check(p.parse_args().root.resolve())
