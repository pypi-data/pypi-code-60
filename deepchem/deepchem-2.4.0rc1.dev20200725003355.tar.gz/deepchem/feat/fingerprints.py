"""
Topological fingerprints.
"""
from deepchem.feat.base_classes import MolecularFeaturizer


class CircularFingerprint(MolecularFeaturizer):
  """Circular (Morgan) fingerprints.

  Extended Connectivity Circular Fingerprints compute a bag-of-words style
  representation of a molecule by breaking it into local neighborhoods and
  hashing into a bit vector of the specified size. See [1]_ for more details.

  Parameters
  ----------
  radius : int, optional (default 2)
      Fingerprint radius.
  size : int, optional (default 2048)
      Length of generated bit vector.
  chiral : bool, optional (default False)
      Whether to consider chirality in fingerprint generation.
  bonds : bool, optional (default True)
      Whether to consider bond order in fingerprint generation.
  features : bool, optional (default False)
      Whether to use feature information instead of atom information; see
      RDKit docs for more info.
  sparse : bool, optional (default False)
      Whether to return a dict for each molecule containing the sparse
      fingerprint.
  smiles : bool, optional (default False)
      Whether to calculate SMILES strings for fragment IDs (only applicable
      when calculating sparse fingerprints).

  References
  ----------
  .. [1] Rogers, David, and Mathew Hahn. "Extended-connectivity fingerprints."
         Journal of chemical information and modeling 50.5 (2010): 742-754.

  Note
  ----
  This class requires RDKit to be installed.
  """
  name = 'circular'

  def __init__(self,
               radius=2,
               size=2048,
               chiral=False,
               bonds=True,
               features=False,
               sparse=False,
               smiles=False):
    try:
      from rdkit import Chem
      from rdkit.Chem import rdMolDescriptors
    except ModuleNotFoundError:
      raise ValueError("This class requires RDKit to be installed.")
    self.radius = radius
    self.size = size
    self.chiral = chiral
    self.bonds = bonds
    self.features = features
    self.sparse = sparse
    self.smiles = smiles

  def _featurize(self, mol):
    """Calculate circular fingerprint.

    Parameters
    ----------
    mol : RDKit Mol
        Molecule.
    """
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors
    if self.sparse:
      info = {}
      fp = rdMolDescriptors.GetMorganFingerprint(
          mol,
          self.radius,
          useChirality=self.chiral,
          useBondTypes=self.bonds,
          useFeatures=self.features,
          bitInfo=info)
      fp = fp.GetNonzeroElements()  # convert to a dict

      # generate SMILES for fragments
      if self.smiles:
        fp_smiles = {}
        for fragment_id, count in fp.items():
          root, radius = info[fragment_id][0]
          env = Chem.FindAtomEnvironmentOfRadiusN(mol, radius, root)
          frag = Chem.PathToSubmol(mol, env)
          smiles = Chem.MolToSmiles(frag)
          fp_smiles[fragment_id] = {'smiles': smiles, 'count': count}
        fp = fp_smiles
    else:
      fp = rdMolDescriptors.GetMorganFingerprintAsBitVect(
          mol,
          self.radius,
          nBits=self.size,
          useChirality=self.chiral,
          useBondTypes=self.bonds,
          useFeatures=self.features)
    return fp

  def __hash__(self):
    return hash((self.radius, self.size, self.chiral, self.bonds, self.features,
                 self.sparse, self.smiles))

  def __eq__(self, other):
    if not isinstance(self, other.__class__):
      return False
    return self.radius == other.radius and \
           self.size == other.size and \
           self.chiral == other.chiral and \
           self.bonds == other.bonds and \
           self.features == other.features and \
           self.sparse == other.sparse and \
           self.smiles == other.smiles
