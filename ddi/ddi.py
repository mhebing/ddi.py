class DDI:
    """
    Base DDI class.
    """

    def __init__(self):
        self.metadata = {}
        self.data = None

    def add_statistics(self):
        for varname, meta in self.metadata.items():
            try:
                var = self.data[varname]
                self._add_frequencies(var, varname, meta)
            except:
                pass

    def _add_frequencies(self, var, varname, meta):
        if len(var.unique()) < 30:
            counts = dict(var.value_counts(
                dropna=False,
                sort=False
            ))
            if "value_labels" in self.metadata[varname]:
                counts = {int(key):val for key, val in counts.items()}
            self.metadata[varname]["frequencies"] = counts
