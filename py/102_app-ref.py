#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 11:15:31 2018

@author: Kazuki
"""

import numpy as np
import pandas as pd
import utils
#utils.start(__file__)
#==============================================================================

PREF = 'prev_102_'

KEY = 'SK_ID_CURR'

# =============================================================================
# 
# =============================================================================
prev = utils.read_pickles('../data/previous_application')
base = prev[[KEY]].drop_duplicates().set_index(KEY)

gr_app = prev[prev['NAME_CONTRACT_STATUS']=='Approved'].groupby(KEY)
gr_ref = prev[prev['NAME_CONTRACT_STATUS']=='Refused'].groupby(KEY)

col = ['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 
       'AMT_CREDIT-dby-AMT_ANNUITY', 'DAYS_BIRTH']

train = utils.load_train([KEY]+col)
test = utils.load_test([KEY]+col)

train.columns = [KEY] + ['app_'+c for c in train.columns[1:]]
test.columns  = [KEY] + ['app_'+c for c in test.columns[1:]]

col_init = train.columns.tolist()

# =============================================================================
# feature
# =============================================================================
base['cnt_approved'] = gr_app.size()

base['DAYS_DECISION_app_min'] = gr_app['DAYS_DECISION'].min()
base['DAYS_DECISION_app_max'] = gr_app['DAYS_DECISION'].max()




base['cnt_refused'] = gr_ref.size()
base['DAYS_DECISION_ref_min'] = gr_ref['DAYS_DECISION'].min()
base['DAYS_DECISION_ref_max'] = gr_ref['DAYS_DECISION'].max()



base.reset_index(inplace=True)
# =============================================================================
# merge
# =============================================================================

def mk_feature(df):
    
    df['DAYS_DECISION_app_min-m-DAYS_BIRTH'] = df['DAYS_DECISION_app_min'] - df['app_DAYS_BIRTH']
    df['DAYS_DECISION_app_max-m-DAYS_BIRTH'] = df['DAYS_DECISION_app_max'] - df['app_DAYS_BIRTH']
    
    df['DAYS_DECISION_ref_min-m-DAYS_BIRTH'] = df['DAYS_DECISION_ref_min'] - df['app_DAYS_BIRTH']
    df['DAYS_DECISION_ref_max-m-DAYS_BIRTH'] = df['DAYS_DECISION_ref_max'] - df['app_DAYS_BIRTH']
    
    return

train2 = pd.merge(train, base, on=KEY, how='left')
mk_feature(train2)


test2 = pd.merge(test, base, on=KEY, how='left')
mk_feature(test2)


# =============================================================================
# output
# =============================================================================
train2.drop(col_init, axis=1, inplace=True)
test2.drop(col_init, axis=1, inplace=True)
utils.to_feature(train2.add_prefix(PREF), '../feature/train')
utils.to_feature(test2.add_prefix(PREF),  '../feature/test')

#==============================================================================
utils.end(__file__)


