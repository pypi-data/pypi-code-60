"""
PCBA dataset loader.
"""
import os
import logging
import deepchem
import gzip

logger = logging.getLogger(__name__)

DEFAULT_DIR = deepchem.utils.get_data_dir()


def load_pcba(featurizer='ECFP',
              split='random',
              reload=True,
              data_dir=None,
              save_dir=None,
              **kwargs):
  return load_pcba_dataset(
      featurizer=featurizer,
      split=split,
      reload=reload,
      assay_file_name="pcba.csv.gz",
      data_dir=data_dir,
      save_dir=save_dir,
      **kwargs)


def load_pcba_146(featurizer='ECFP',
                  split='random',
                  reload=True,
                  data_dir=None,
                  save_dir=None,
                  **kwargs):
  return load_pcba_dataset(
      featurizer=featurizer,
      split=split,
      reload=reload,
      assay_file_name="pcba_146.csv.gz",
      data_dir=data_dir,
      save_dir=save_dir,
      **kwargs)


def load_pcba_2475(featurizer='ECFP',
                   split='random',
                   reload=True,
                   data_dir=None,
                   save_dir=None,
                   **kwargs):
  return load_pcba_dataset(
      featurizer=featurizer,
      split=split,
      reload=reload,
      assay_file_name="pcba_2475.csv.gz",
      data_dir=data_dir,
      save_dir=save_dir,
      **kwargs)


def load_pcba_dataset(featurizer='ECFP',
                      split='random',
                      reload=True,
                      assay_file_name="pcba.csv.gz",
                      data_dir=None,
                      save_dir=None,
                      **kwargs):
  """Load PCBA dataset

  PubChem BioAssay (PCBA) is a database consisting of biological activities of 
  small molecules generated by high-throughput screening. We use a subset of 
  PCBA, containing 128 bioassays measured over 400 thousand compounds, 
  used by previous work to benchmark machine learning methods.

  Random splitting is recommended for this dataset.

  The raw data csv file contains columns below:

  - "mol_id" - PubChem CID of the compound
  - "smiles" - SMILES representation of the molecular structure
  - "PCBA-XXX" - Measured results (Active/Inactive) for bioassays:
        search for the assay ID at 
        https://pubchem.ncbi.nlm.nih.gov/search/#collection=bioassays 
        for details

  References
  ----------
  .. [1] Wang, Yanli, et al. "PubChem's BioAssay database." 
     Nucleic acids research 40.D1 (2011): D400-D412.
  """
  if data_dir is None:
    data_dir = DEFAULT_DIR
  if save_dir is None:
    save_dir = DEFAULT_DIR

  if reload:
    save_folder = os.path.join(save_dir,
                               assay_file_name.split(".")[0] + "-featurized",
                               featurizer)
    if featurizer == "smiles2img":
      img_spec = kwargs.get("img_spec", "std")
      save_folder = os.path.join(save_folder, img_spec)
    save_folder = os.path.join(save_folder, str(split))

  dataset_file = os.path.join(data_dir, assay_file_name)

  if not os.path.exists(dataset_file):
    deepchem.utils.download_url(
        url="http://deepchem.io.s3-website-us-west-1.amazonaws.com/datasets/{0}".
        format(assay_file_name),
        dest_dir=data_dir)

  # Featurize PCBA dataset
  logger.info("About to featurize PCBA dataset.")
  if featurizer == 'ECFP':
    featurizer = deepchem.feat.CircularFingerprint(size=1024)
  elif featurizer == 'GraphConv':
    featurizer = deepchem.feat.ConvMolFeaturizer()
  elif featurizer == 'Weave':
    featurizer = deepchem.feat.WeaveFeaturizer()
  elif featurizer == 'Raw':
    featurizer = deepchem.feat.RawFeaturizer()
  elif featurizer == "smiles2img":
    img_spec = kwargs.get("img_spec", "std")
    img_size = kwargs.get("img_size", 80)
    featurizer = deepchem.feat.SmilesToImage(
        img_size=img_size, img_spec=img_spec)

  with gzip.GzipFile(dataset_file, "r") as fin:
    header = fin.readline().rstrip().decode("utf-8")
    columns = header.split(",")
    columns.remove("mol_id")
    columns.remove("smiles")
    PCBA_tasks = columns

  if reload:
    loaded, all_dataset, transformers = deepchem.utils.save.load_dataset_from_disk(
        save_folder)
    if loaded:
      return PCBA_tasks, all_dataset, transformers

  loader = deepchem.data.CSVLoader(
      tasks=PCBA_tasks, smiles_field="smiles", featurizer=featurizer)

  dataset = loader.featurize(dataset_file)

  if split == None:
    transformers = [deepchem.trans.BalancingTransformer(dataset=dataset)]

    logger.info("Split is None, about to transform data")
    for transformer in transformers:
      dataset = transformer.transform(dataset)

    return PCBA_tasks, (dataset, None, None), transformers

  splitters = {
      'index': deepchem.splits.IndexSplitter(),
      'random': deepchem.splits.RandomSplitter(),
      'scaffold': deepchem.splits.ScaffoldSplitter(),
      'stratified': deepchem.splits.SingletaskStratifiedSplitter()
  }
  splitter = splitters[split]
  logger.info("About to split dataset using {} splitter.".format(split))
  frac_train = kwargs.get("frac_train", 0.8)
  frac_valid = kwargs.get('frac_valid', 0.1)
  frac_test = kwargs.get('frac_test', 0.1)

  train, valid, test = splitter.train_valid_test_split(
      dataset,
      frac_train=frac_train,
      frac_valid=frac_valid,
      frac_test=frac_test)

  transformers = [deepchem.trans.BalancingTransformer(dataset=train)]

  logger.info("About to transform dataset.")
  for transformer in transformers:
    train = transformer.transform(train)
    valid = transformer.transform(valid)
    test = transformer.transform(test)

  if reload:
    deepchem.utils.save.save_dataset_to_disk(save_folder, train, valid, test,
                                             transformers)

  return PCBA_tasks, (train, valid, test), transformers
