class TemporalRiskSmoother:

    def __init__(self, alpha=0.3):
        self.alpha = alpha
        self.smoothed_score = None

    def smooth(self, current_score):

        if self.smoothed_score is None:
            self.smoothed_score = current_score
        else:
            self.smoothed_score = (
                self.alpha * current_score +
                (1 - self.alpha) * self.smoothed_score
            )

        return round(self.smoothed_score, 3)