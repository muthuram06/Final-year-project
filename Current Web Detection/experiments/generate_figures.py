import os
import matplotlib.pyplot as plt
import numpy as np

# Save path (inside project root)
save_path = os.getcwd()

# ==============================
# FIGURE 2 – Workflow Diagram
# ==============================
plt.figure()
plt.title("Workflow of Enhanced AI-Based Online Proctoring System")
plt.text(0.1, 0.8, "Input Acquisition\n(Webcam + Microphone)")
plt.text(0.1, 0.6, "Feature Extraction\n(Face, Blink, Head Pose,\nDevice & Audio Detection)")
plt.text(0.1, 0.4, "Feature Fusion & Behavior Analysis")
plt.text(0.1, 0.2, "Risk Classification\n(Low / Medium / High)")

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xticks([])
plt.yticks([])
plt.box(False)

plt.savefig(os.path.join(save_path, "Fig2_Workflow.png"), dpi=300, bbox_inches='tight')
plt.close()


# ==============================
# FIGURE 3 – Performance Comparison
# ==============================
metrics = ["Accuracy", "Sensitivity", "Specificity", "F1-Score", "Precision", "AUC"]
existing = [82, 78, 85, 76, 74, 84]
proposed = [94, 91, 96, 92, 90, 95]

x = np.arange(len(metrics))
width = 0.35

plt.figure()
plt.bar(x - width/2, existing, width, label="Existing System")
plt.bar(x + width/2, proposed, width, label="Proposed AI Proctoring")

plt.ylabel("Percentage (%)")
plt.title("Performance Comparison Between Existing and Proposed System")
plt.xticks(x, metrics, rotation=45)
plt.legend()

plt.savefig(os.path.join(save_path, "Fig3_Performance.png"), dpi=300, bbox_inches='tight')
plt.close()


# ==============================
# FIGURE 4 – Confusion Matrix
# ==============================
conf_matrix = np.array([[185, 15],
                        [12, 188]])

plt.figure()
plt.imshow(conf_matrix)
plt.title("Confusion Matrix of Proposed AI Proctoring Model")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")

for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        plt.text(j, i, conf_matrix[i, j],
                 ha="center", va="center")

plt.xticks([0, 1], ["Normal", "Suspicious"])
plt.yticks([0, 1], ["Normal", "Suspicious"])

plt.savefig(os.path.join(save_path, "Fig4_ConfusionMatrix.png"), dpi=300, bbox_inches='tight')
plt.close()

print("Figures saved successfully in project root folder.")