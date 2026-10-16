"""Reconstruct documentary comparisons; no synthetic experimental observations."""
from pathlib import Path
from decimal import Decimal, getcontext
from collections import Counter, defaultdict
import csv,json,math,argparse
getcontext().prec=40
ROOT=Path(__file__).resolve().parents[1]
D=Decimal

def read(name):
 with (ROOT/'data'/name).open() as f:return list(csv.DictReader(f))
def wavelength_residual(row):
 """Difference in fm between printed wavelength and c/f, without binary rounding."""
 scale={'kHz':D(1000),'MHz':D(1000000)}
 if not row['frequency']:return None
 f=D(row['frequency'])*scale[row['frequency_unit']]
 return D(row['wavelength_fm'])-D(299792458)/f*D(10)**15

def comparison(rows,key,y0,y1):
 a=next(r for r in rows if r['key']==key and int(r['year'])==y0)
 b=next(r for r in rows if r['key']==key and int(r['year'])==y1)
 return dict(key=key,years=[y0,y1],standard_ratio=float(D(a['standard_relative'])/D(b['standard_relative'])),
  mixed_convention_ratio=float(D(a['overall_relative'])/D(b['standard_relative'])) if a['overall_relative'] else None,
  before_conditions=a['conditions'],after_conditions=b['conditions'],
  interpretation='ratio of documentary assigned uncertainties; not a controlled apparatus comparison')

def budget(rows,L):
 groups=defaultdict(float)
 for r in rows:groups[r['group']]+=float(r['constant_nm'])**2+(float(r['nm_per_mm'])*L)**2
 v=sum(groups.values())
 return dict(length_mm=L,standard_nm=math.sqrt(v),expanded_k2_nm=2*math.sqrt(v),
  variance_shares={g:x/v for g,x in groups.items()},
  max_reduction_removing_laser_percent=100*(1-math.sqrt(1-groups['Laser']/v)),
  published_expanded_k2_nm=2*math.sqrt(12.4**2+(.144*L)**2))

def main():
 rows=read('radiations.csv');b=read('nrc_budget.csv')
 residuals=[dict(year=int(r['year']),section=r['section'],key=r['key'],residual_fm=str(wavelength_residual(r))) for r in rows if r['frequency']]
 results=dict(counts=dict(Counter(r['year'] for r in rows)),legacy_lines=len(read('legacy_lamps.csv')),
  comparisons=[comparison(rows,k,1983,1992) for k in ['ch4-cell','i633','i612','i515']],
  calcium_1992_1997=comparison(rows,'ca657',1992,1997),
  methane_1983_best_1992_ratio=float(D('4.4e-11')/D('3e-12')),
  krypton_relative_shift=float((D('605780210.3')-D('605780210'))/D('605780210')),
  nrc_budget=[budget(b,L) for L in [10,100,1000]],
  table_constant_coefficient=math.sqrt(sum(float(r['constant_nm'])**2 for r in b)),
  table_length_coefficient=math.sqrt(sum(float(r['nm_per_mm'])**2 for r in b)),
  frequency_wavelength_residuals=residuals)
 (ROOT/'results/analysis.json').write_text(json.dumps(results,indent=2)+'\n')
 with (ROOT/'results/comparisons.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=['key','standard_ratio','mixed_convention_ratio']);w.writeheader()
  for r in results['comparisons']:w.writerow({k:r[k] for k in w.fieldnames})
 print(json.dumps({k:v for k,v in results.items() if k!='frequency_wavelength_residuals'},indent=2))
if __name__=='__main__':main()
