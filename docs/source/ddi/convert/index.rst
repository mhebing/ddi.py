convert
=======

With the modules from ddi.convert, the user can convert datasets and generate statistics for them.

How to start?
-------------

Clone ddi from github
+++++++++++++++++++++

.. code-block:: none

    git clone https://github.com/ddionrails/ddi.py.git

Import from ddi
+++++++++++++++

.. code-block:: python

    sys.path.append(os.path.abspath("../../ddi.py"))
    from ddi.dataset import Dataset
    
    d1 = Dataset()
    
or

.. code-block:: python

    sys.path.append(os.path.abspath("../../../ddi.py"))
    from ddi import stata_to_statistics

    stata_to_statistics(
        study_name="...",
        input_csv="...",
        input_path="...",
        input_path_de="...",
        output_path="..."
    )


Modules for dataset.py
----------------------
.. toctree::
    :maxdepth: 2

    read_stata
    read_tdp
    write_stata
    write_stats
    write_tdp
    
Templates for write_stats.py
----------------------------
.. toctree::
    :maxdepth: 2
     
    template_stats_html
    template_stats_md
    
Module for direct convert stata to statistics
---------------------------------------------
.. toctree::
    :maxdepth: 2
    
    stata_to_statistics
