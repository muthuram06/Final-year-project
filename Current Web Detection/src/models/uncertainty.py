import numpy as np

class UncertaintyEstimator:

    def compute_uncertainty(self, feature_contributions):

        values = list(feature_contributions.values())

        if len(values) == 0:
            return 0.0

        std_dev = np.std(values)

        return round(std_dev, 3)

    def compute_confidence(self, uncertainty):

        confidence = 1 / (1 + uncertainty)

        return round(confidence, 3)