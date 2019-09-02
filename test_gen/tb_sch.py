# -*- coding: utf-8 -*-

import pprint

import bag
import numpy as np
import yaml

lib_name = 'woorham_mem_templates'
cell_name = 'tb_array'
impl_lib = 'woorham_generated'
# tb_lib = 'adc_sar_testbenches'

params = dict(
    )

load_from_file=False
# yamlfile_spec="./ACG_ILO/specs/tinv.yaml"

# if load_from_file==True:
#     with open(yamlfile_spec, 'r') as stream:
#         specdict = yaml.load(stream)
#     params['lch']=specdict['lch']*1e-6
#     params['m']=specdict['layout_params']['fg_num']
#     params['nw']=specdict['layout_params']['fg_w_dict']['nmos']*1e-6
#     params['pw']=specdict['layout_params']['fg_w_dict']['pmos']*1e-6
#     params['n_intent']=specdict['layout_params']['type_dict']['nmos']
#     params['p_intent']=specdict['layout_params']['type_dict']['pmos']

params['n_word'] = 1024
params['n_bit'] = 2
params['sel_wl_index'] = 1
params['sel_bl_index'] = 1
params['init_to']='ST'

print('creating BAG project')
prj = bag.BagProject()

# create design module and run design method.
print('designing module')
dsn = prj.create_design_module(lib_name, cell_name)
print('design parameters:\n%s' % pprint.pformat(params))
dsn.design(**params)

# implement the design
print('implementing design with library %s' % impl_lib)
dsn.implement_design(impl_lib, top_cell_name=cell_name, suffix='_' + str(params['n_word']) + 'by' + str(params['n_bit']))
#dsn.implement_design(impl_lib, top_cell_name=cell_name_standalone, erase=True)

