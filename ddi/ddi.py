class DDI:
    """
    Base DDI class.
    """

    def __init__(self):
        self.meta = {}
        self.data = None

    def add_statistics(self):
        for varname, meta in self.meta.items():
            if varname in self.data:
                var = self.data[varname]
                self._add_frequencies(var, varname, meta)

    def _add_frequencies(self, var, varname, meta):
        if len(var.unique()) < 30:
            counts = dict(var.value_counts(
                dropna=False,
                sort=False
            ))
            meta["frequencies"] = counts
