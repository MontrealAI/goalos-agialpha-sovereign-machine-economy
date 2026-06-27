from pathlib import Path
import sys
sys.path.insert(0, str(Path('src').resolve()))
from goalos_ascension.demo_runner import write_demo_pack
pack = write_demo_pack()
print('Autonomous demo pack written:', len(pack['dockets']), 'dockets')
