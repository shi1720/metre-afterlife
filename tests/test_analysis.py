import unittest,sys
from pathlib import Path
from decimal import Decimal as D
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from analyze import read,wavelength_residual,comparison,budget
class AuditTests(unittest.TestCase):
 def test_complete_numbered_enumeration(self):
  r=read('radiations.csv')
  self.assertEqual(len(r),31)
  self.assertEqual(len({(x['year'],x['section']) for x in r}),31)
  self.assertEqual([sum(x['year']==y for x in r) for y in ['1983','1992','1997']],[6,10,15])
 def test_frequency_wavelength_rounding(self):
  # Recommendations say the wavelengths are rounded. All printed pairs must
  # agree to half the final printed fm unit (not to zero absolute residual).
  for r in read('radiations.csv'):
   if not r['frequency']:continue
   q=D(1).scaleb(D(r['wavelength_fm']).as_tuple().exponent)
   self.assertLessEqual(abs(wavelength_residual(r)),q/2,msg=f"{r['year']} {r['section']}")
 def test_legacy_exact_unit_conversion(self):
  a=read('legacy_1963.csv');b=read('legacy_lamps.csv')
  self.assertEqual(len(a),len(b))
  for x,y in zip(a,b):
   self.assertEqual(x['species'],y['species'])
   self.assertEqual(D(x['wavelength_angstrom'])*100,D(y['wavelength_pm']))
 def test_convention_aware_ratios(self):
  r=read('radiations.csv')
  self.assertAlmostEqual(comparison(r,'i633',1983,1992)['standard_ratio'],13.6)
  self.assertAlmostEqual(comparison(r,'i633',1983,1992)['mixed_convention_ratio'],40)
  self.assertAlmostEqual(comparison(r,'ch4-cell',1983,1992)['standard_ratio'],44/23)
 def test_methane_modes_not_merged(self):
  r=read('radiations.csv')
  for y in ['1992','1997']:
   a=[x for x in r if x['year']==y and x['species']=='CH4']
   self.assertEqual(len(a),2)
   self.assertEqual({x['standard_relative'] for x in a},{'3e-12','2.3e-11'})
 def test_reclassified_laser_survives(self):
  r=read('radiations.csv')
  self.assertEqual(next(x for x in r if x['year']=='1997' and x['key']=='i576')['section'],'2.3')
 def test_lamp_retention(self):
  r=read('legacy_lamps.csv');self.assertEqual(len(r),12)
  self.assertEqual({x['species'] for x in r},{'Kr86','Hg198','Cd114'})
 def test_independent_budget_hand_calculation(self):
  b=read('nrc_budget.csv');z=budget(b,1000)
  self.assertAlmostEqual(sum(z['variance_shares'].values()),1)
  # 5 constant terms: 2^2+6^2+10^2+2^2+3^2=153.
  self.assertAlmostEqual(sum(float(x['constant_nm'])**2 for x in b),153)
  self.assertAlmostEqual(z['expanded_k2_nm'],271.22684232944204)
  # Source summary is separately preserved; displayed rounded row entries do
  # not sum exactly to its printed 0.144 coefficient. Do not silently force it.
  self.assertAlmostEqual(2*(12.4**2+(.144*1000)**2)**.5,289.0658056567743)
  self.assertLess(z['variance_shares']['Laser'],.002)
 def test_calcium_requires_condition_change(self):
  r=read('radiations.csv');z=comparison(r,'ca657',1992,1997)
  self.assertEqual(z['standard_ratio'],750)
  self.assertNotEqual(z['before_conditions'],z['after_conditions'])
if __name__=='__main__':unittest.main()
