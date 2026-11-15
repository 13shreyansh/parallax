import unittest
from service.app import verified_absence
class AbsenceScope(unittest.TestCase):
 def test_only_reviewed_parent_revision_proves_material_absence(self):
  version={'claim_id':'c'};flags=[{'claim_id':'c','history':{'material_absence_verified':True,'before_revision':123}}]
  self.assertTrue(verified_absence(version,flags,123))
  self.assertFalse(verified_absence(version,flags,122))
  self.assertFalse(verified_absence(version,flags,None))
 def test_unreviewed_or_other_claim_never_proves_absence(self):
  self.assertFalse(verified_absence({'claim_id':'c'},[{'claim_id':'x','history':{'material_absence_verified':True,'before_revision':123}}],123))
