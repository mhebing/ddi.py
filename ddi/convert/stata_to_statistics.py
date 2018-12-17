import logging
import os
import sys

import pandas as pd
from ddi.dataset import Dataset

logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath("../../../ddi.py"))


def stata_to_statistics(
    study_name, input_csv, input_path, output_path, input_path_de=""
):
    filereader = pd.read_csv(input_csv, delimiter=",", header=0)

    for data, weight, split, analysis_unit, period, sub_type in zip(
        filereader.filename,
        filereader.weight,
        filereader.split,
        filereader.analysis_unit,
        filereader.period,
        filereader.sub_type,
    ):
        d1 = Dataset()
        try:
            d1.read_stata(input_path + data + ".dta")
        except:
            logger.warning("Unable to find " + data + ".dta in " + input_path + ".")
            continue

        metadata_de = ""
        if input_path_de != "":
            d2 = Dataset()
            try:
                d2.read_stata(input_path_de + data + ".dta")
                metadata_de = d2.metadata
            except:
                logger.warning(
                    "Unable to find " + data + ".dta in " + input_path_de + "."
                )
                continue

        d1.write_stats(
            output_path + data + "_stats.json",
            split=split,
            weight=weight,
            analysis_unit=analysis_unit,
            period=period,
            sub_type=sub_type,
            study=study_name,
            metadata_de=metadata_de,
        )
