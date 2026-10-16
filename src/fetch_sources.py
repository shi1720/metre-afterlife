"""Optional source retrieval. Original files are not bundled or relicensed.

Hashes identify inspected copies. Dynamic HTML differences are reported, not
silently adopted as a new authoritative transcription.
"""
from pathlib import Path
from urllib.request import urlopen,Request
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def main():
 dest=ROOT/'sources';dest.mkdir(exist_ok=True)
 for s in json.loads((ROOT/'source_catalogue.json').read_text()):
  try:
   with urlopen(Request(s['url'],headers={'User-Agent':'metre-afterlife-research/1.0'}),timeout=60) as r:data=r.read()
   p=dest/s.get('snapshot_filename',s['id']+'.html');p.write_bytes(data)
   same=hashlib.sha256(data).hexdigest()==s.get('sha256')
   print(s['id'],'matches inspected snapshot' if same else 'DIFFERENT from inspected snapshot: review before use')
  except Exception as e:print(s['id'],'retrieval failed:',e)
if __name__=='__main__':main()
