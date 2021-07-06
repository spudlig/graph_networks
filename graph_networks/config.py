#!/usr/bin/env python

# =============================================================================
# MODULE DOCSTRING
# =============================================================================

"""

"""

# =============================================================================
# GLOBAL IMPORTS
# =============================================================================

from dataclasses import dataclass, field
from typing import List

import tensorflow as tf
from graph_networks.utilities import *
import logging
import os




ATOM_FEATURE_DIM = DGIN6_ATOM_FEATURE_DIM
EDGE_FEATURE_DIM = DGIN6_EDGE_FEATURE_DIM


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================

@dataclass
class BasicModelConfig:
    """
    Config for all graph neural network files.
    General model parameters
    """
    model_name: str = 'only_logdp_dgin6_2' # without h_w in DGIN gin part - added h_v_0 instead
                                    # whole train/eval split - no more double split within train data set
                                    # random train/test split in get_data_sd - only change overall_seed
                                    # CHANGES dgin3 10.02.2021:
                                    # *added new bondFeaturesDGIN2 and atomFeaturesDGIN2; DGIN2_ATOM_FEATURE_DIM; DGIN2_EDGE_FEATURE_DIM
                                    # *from project_path+'data/processed/lipo/pickled/train_frags3/' to project_path+'data/processed/lipo/pickled/test_frags3/'
                                    # CHANGES dgin3 16.02.2021:
                                    # *added new bondFeaturesDGIN3 and atomFeaturesDGIN3; DGIN3_ATOM_FEATURE_DIM; DGIN3_EDGE_FEATURE_DIM
                                    # *from project_path+'data/processed/lipo/pickled/train_frags_dgin3/' to project_path+'data/processed/lipo/pickled/test_frags_dgin3/'
                                    # CHANGES dgin4 16.02.2021:
                                    # *added add_species bool in model1 config - previously not there; for dgin2 featurization adds the species type after the dgin 
                                    # encoding before logD prediction
                                    # test_frags_dgin4 was added for species inclusion in model2 call()
    batch_size: int =15
    override_if_exists: bool = True

    overall_seed: int = 2
    
    project_path:str = '/home/owieder/Projects/graphnets/'
    # project_path:str = os.getcwd()+'/'
    # project_path:str = '/home/oliver/projects/graphnets/'

    retrain_model: bool = False
    retrain_model_name: str = ''
    retrain_model_epoch: str = ''
    retrain_model_weights_dir: str = project_path+'reports/model_weights/'+retrain_model_name+'/epoch_'+retrain_model_epoch+'/checkp_'+retrain_model_epoch

    train_data_dir: str = project_path+'data/processed/lipo/pickled/train_dgin6_logd/'
    test_data_dir: str = project_path+'data/processed/lipo/pickled/test_dgin6_logd/'

    combined_dataset: bool = False

    add_train_data_dir: str = project_path+'data/processed/lipo/pickled/train_dgin6_logs/'
    add_test_data_dir: str = project_path+'data/processed/lipo/pickled/test_dgin6_logs/'

    test_model: bool = False
    test_model_epoch: str = '609'
    test_model_weights_dir: str = project_path+'reports/model_weights/'+model_name+'/epoch_'+test_model_epoch+'/checkp_'+test_model_epoch
    encode_hidden: bool = False

    log_dir: str = project_path+'logs/'+model_name+'.log'
    verbosity_level = logging.INFO

    model_type: str = "DGIN" # can be either "GIN", "MPNN" or "DGIN"
    
    plot_dir: str = project_path+'reports/figures/'+model_name+'/'
    tensorboard_log_dir: str = project_path+'reports/tensorboard/'+model_name+'/'
    config_log_dir: str = project_path+'reports/configs/'+model_name+'/'
    model_weights_dir: str = project_path+'reports/model_weights/'+model_name+'/'
    stats_log_dir: str = project_path+'reports/stats/'+model_name+'/'

@dataclass
class DGINConfig:
    """
    Config for D-GIN/D-MPNN or GIN model class.
    

    """
    dropout_aggregate_dmpnn: bool = False
    layernorm_aggregate_dmpnn: bool = True
    dropout_passing_dmpnn: bool = False
    layernorm_passing_dmpnn: bool = True

    dropout_aggregate_gin: bool = False
    layernorm_aggregate_gin: bool = True
    dropout_passing_gin: bool = False
    layernorm_passing_gin: bool = True

    gin_aggregate_bias: bool = False
    dmpnn_passing_bias: bool = False
    init_bias: bool = False

    massge_iteration_dmpnn: int = 4
    message_iterations_gin: int = 4
    dropout_rate: float = 0.15
    input_size: int = (ATOM_FEATURE_DIM+EDGE_FEATURE_DIM) # combination of node feature len (33) and edge feature len (12)
    passing_hidden_size: int = 56 # this can be changed
    input_size_gin: int = (ATOM_FEATURE_DIM+passing_hidden_size)

    return_hv: bool = True # model3 parameter

@dataclass
class Model1Config:
    """
    Configs for the different models that utilize 
    Config model1 class - no subclass configs are defined here.
    """
    validation_split: float = 0.90
    learning_rate: float = 0.004
    clip_rate: float = 0.6
    optimizer = tf.keras.optimizers.Adam(learning_rate)
    lipo_loss_mse = tf.keras.losses.mse
    lipo_loss_mae = tf.keras.losses.mae
    logP_loss_mse = tf.keras.losses.mse
    logS_loss_mse = tf.keras.losses.mse
    mw_loss_mse = tf.keras.losses.mse
    metric = tf.keras.losses.mae
    epochs: int = 1600
    safe_after_batch: int = 3
    dropout_rate: float = 0.15 # the overall dropout rate of the readout functions
    train_data_seed: int = 0

    hidden_readout_1: int = 32
    hidden_readout_2: int = 14
    activation_func_readout = tf.nn.relu
    
    include_logD: bool = True
    include_logS: bool = False
    include_logP: bool = True
    include_mw: bool = False
    include_rot_bond: bool = False
    include_HBA: bool = False
    include_HBD: bool = False

    best_evaluation_threshold: float = 1.45 #was introduced on the 25.03.2021/ 
                                            # 2.45 for all_logs
                                            # 0.70 logP
                                            # 0.75 logD
                                            # 1.00 logS
                                            # 1.75 logSD
                                            # 1.70 logSP
                                            # 1.45 logDP

    include_fragment_conv: bool = False # was introduced on the 4.12.2020

    use_rmse: bool = True # uses RMSE instead of MSE for only lipo_loss
    shuffle_inside: bool = True # reshuffles the train/valid test seach in each epoch (generalizes)

    add_species: bool = False # 16.02 introduction; previously not there; for dgin3 adds the species type after the dgin encoding before logD prediction

@dataclass
class FrACConfig:
    """
    Config fragment aggregation class - no subclass configs are defined here.
    """
    input_size_gin: int = 28
    layernorm_aggregate: bool = True
    reduce_mean: bool = True # when false -> reduce_sum

@dataclass
class Config():
    """
    Overall config class for model2 and run file.
    Includes all submodels config
    """
    basic_model_config: BasicModelConfig
    model1_config: Model1Config
    d_gin_config: DGINConfig
    frag_acc_config: FrACConfig
    model: str = 'model10'