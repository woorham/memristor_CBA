# -*- coding: utf-8 -*-

from typing import Dict

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class woorham_mem_templates__array(Module):
    """Module for library woorham_mem_templates cell array.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'array.yaml'))


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
        )

    def design(self, n_word, n_bit):
        name_list = []
        term_list = []
        for i in range(n_bit):
            name_list.append('CELL%d<%d:0>'%(i, n_word-1))
            term_list.append({'t0': 'w%d<0:%d>'%(i, n_word-1), 't1': 'w%d<0:%d>'%(i+1, n_word-1),
                              'b0': 'b%d<%d:0>'%(i, n_word-1), 'b1': 'b%d<%d:1>'%(i, n_word)})
        self.array_instance('CELL', name_list, term_list)
        for i in range(n_bit):
            self.instances['CELL'][i].design()

        self.rename_pin('w', 'w0<%d:0>'%(n_word-1))
        self.rename_pin('b', 'b0<0>')
        for i in range(n_bit):
            if not i == 0:
                self.add_pin('b%d<0>'%i, 'inputOutput')
