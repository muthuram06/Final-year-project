class BaselineBuilder:
    def __init__(self, required_windows=6):
        self.samples = []
        self.required_windows = required_windows

    def update(self, metrics):
        self.samples.append(metrics)

    def is_ready(self):
        return len(self.samples) >= self.required_windows

    def compute_baseline(self):

        baseline = {}

        keys = self.samples[0].keys()

        for key in keys:
            baseline[key] = round(
                sum(sample[key] for sample in self.samples) / len(self.samples),
                3
            )

        return baseline