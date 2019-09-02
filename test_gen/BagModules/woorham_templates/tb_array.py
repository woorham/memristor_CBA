# -*- coding: utf-8 -*-

from typing import Dict

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class woorham_mem_templates__tb_array(Module):
    """Module for library woorham_mem_templates cell tb_array.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'tb_array.yaml'))


    def __init__(self, database, parent=None, prj=None, **kwargs):
        Module.__init__(self, database, self.yaml_file, parent=parent, prj=prj, **kwargs)

    @classmethod
    def get_params_info(cls):
        # type: () -> Dict[str, str]
        """Returns a dictionary from parameter names to descriptions.

        Returns
        -------
        param_info : Optional[Dict[str, str]]
            dictionary from parameter names to descriptions.
        """
        return dict(
            n_word='number of word-lines',
            n_bit='number of bit-lines',
            sel_wl_index='index of selected WL',
            sel_bl_index='index of selected BL',
            init_to='initialized to RST/ST/RANDOM'
        )

    def design(self, n_word, n_bit, sel_wl_index, sel_bl_index, init_to):
        """To be overridden by subclasses to design this module.

        This method should fill in values for all parameters in
        self.parameters.  To design instances of this module, you can
        call their design() method or any other ways you coded.

        To modify schematic structure, call:

        rename_pin()
        delete_instance()
        replace_instance_master()
        reconnect_instance_terminal()
        restore_instance()
        array_instance()
        """
        self.instances['IDUT'].design(n_word=n_word, n_bit=n_bit)
        if init_to == "RST":
            self.reconnect_instance_terminal('IDUT', 'w0<%d:0>'%(n_word-1), '<*%d>RST,WL_SEL,<*%d>RST'%(n_word-sel_wl_index-1,sel_wl_index-1))
        elif init_to == "ST":
            self.reconnect_instance_terminal('IDUT', 'w0<%d:0>'%(n_word-1), '<*%d>ST,WL_SEL,<*%d>ST'%(n_word-sel_wl_index-1,sel_wl_index-1))

        for i in range(n_bit):
            if not i == sel_bl_index-1:
                self.reconnect_instance_terminal('IDUT', 'b%d<0>'%i, 'BL_NSEL')
            else:
                self.reconnect_instance_terminal('IDUT', 'b%d<0>'%i, 'VSS')



