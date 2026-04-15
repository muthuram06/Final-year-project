class ContinualUpdater:

    def __init__(self, alpha=0.05):
        self.alpha = alpha

    def update_baseline(self, baseline, current_metrics):

        updated = {}

        for key in baseline.keys():
            updated[key] = (
                self.alpha * current_metrics[key] +
                (1 - self.alpha) * baseline[key]
            )

        return updated