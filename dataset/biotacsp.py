import logging

import numpy as np
import pandas as pd

import torch
from torch_geometric.data import InMemoryDataset

import transforms.tograph

log = logging.getLogger(__name__)

class BioTacSp(InMemoryDataset):

  def __init__(self, root, transform=None, pre_transform=None):
    super(BioTacSp, self).__init__(root, transform, pre_transform)

    self.data, self.slices = torch.load(self.processed_paths[0])

  @property
  def raw_file_names(self):
    return ['biotac-palmdown-grasps.csv']

  @property
  def processed_file_names(self):
    return ['biotacsp.pt']

  def download(self):

    url_ = "https://github.com/yayaneath/biotac-sp-images"

    raise RuntimeError(
      "Dataset not found. Please download {} from {} and move it to {}".format(
        str(self.raw_file_names),
        url_,
        self.raw_dir))

  def process(self):
    
    transform_tograph_ = transforms.tograph.ToGraph()

    grasps_ = pd.read_csv(self.raw_paths[0])

    data_list_ = []
    for i in range(len(grasps_)):
      
      sample_ = self.sample_from_csv(grasps_, i)
      sample_ = transform_tograph_(sample_)

      if self.pre_transform is not None:
        sample_ = self.pre_transform(sample_)

      data_list_.append(sample_)

    log.debug(data_list_[0].keys())

    data_, slices_ = self.collate(data_list_)

    torch.save((data_, slices_), self.processed_paths[0])

  def sample_from_csv(self, grasps, idx):

    sample_ = grasps.iloc[idx]
    
    object_ = sample_.iloc[0]
    slipped_ = sample_.iloc[1]
    data_index_ = np.copy(sample_.iloc[2:26]).astype(np.int, copy=False)
    data_middle_ = np.copy(sample_.iloc[26:50]).astype(np.int, copy=False)
    data_thumb_ = np.copy(sample_.iloc[50:75]).astype(np.int, copy=False)
    
    sample_ = {'object': object_,
              'slipped': slipped_,
              'data_index': data_index_,
              'data_middle': data_middle_,
              'data_thumb': data_thumb_}

    return sample_