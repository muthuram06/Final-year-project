from models.uncertainty import UncertaintyEstimator

class RiskModel:
    def __init__(self):

        self.high_threshold = 0.7
        self.medium_threshold = 0.4
        self.uncertainty_model = UncertaintyEstimator()
        self.weights = {
            "blink_rate": 0.25,
            "head_movement_rate": 0.25,
            "face_absence_ratio": 0.2,
            "multi_face_rate": 0.3,
            "device_rate": 0.2,
            "voice_rate": 0.2
        }

    def compute_score(self, metrics):

        score = (
            self.weights["blink_rate"] * metrics["blink_rate"] +
            self.weights["head_movement_rate"] * metrics["head_movement_rate"] +
            self.weights["face_absence_ratio"] * metrics["face_absence_ratio"] +
            self.weights["multi_face_rate"] * metrics["multi_face_rate"]
        )

        return round(score, 2)

    def classify(self, metrics):

        risk_score = self.compute_score(metrics)

        if risk_score >= self.high_threshold:
            level = "HIGH RISK"
            explanation = "Multiple suspicious behavioral patterns detected."
        elif risk_score >= self.medium_threshold:
            level = "MEDIUM RISK"
            explanation = "Moderate behavioral deviations observed."
        else:
            level = "LOW RISK"
            explanation = "Behavior within normal range."

        return {
            "risk_score": risk_score,
            "risk_level": level,
            "explanation": explanation,
            "features": metrics
        }
    
    def compute_deviation_score(self, metrics, baseline):

        epsilon = 1e-3
        score = 0
        contributions = {}

        for key in self.weights.keys():

            base = baseline.get(key, 0)
            current = metrics.get(key, 0)

            deviation = abs(current - base) / (base + current + epsilon)

            weighted = self.weights[key] * deviation
            contributions[key] = round(weighted, 3)

            score += weighted

        return round(score, 3), contributions
    
    def classify(self, metrics, baseline):

        risk_score, contributions = self.compute_deviation_score(metrics, baseline)

        if risk_score >= self.high_threshold:
            level = "HIGH RISK"
        elif risk_score >= self.medium_threshold:
            level = "MEDIUM RISK"
        else:
            level = "LOW RISK"

        uncertainty = self.uncertainty_model.compute_uncertainty(contributions)
        confidence = self.uncertainty_model.compute_confidence(uncertainty)

        return {
           "risk_score": risk_score,
           "risk_level": level,
           "confidence": confidence,
           "uncertainty": uncertainty,
           "feature_contributions": contributions
        }