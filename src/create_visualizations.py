import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
import numpy as np

# Load your actual model and data
print("Loading your trained model...")
rf_model = joblib.load('../trained_model/11_model_checkpoints/xg_model_final.pkl')
feature_cols = joblib.load('../trained_model/11_model_checkpoints/feature_cols_final.pkl')
predictions = pd.read_pickle('../trained_model/11_model_checkpoints/predictions.pkl')

# 1. Create Feature Importance visualization
plt.figure(figsize=(10, 8))
importance_df = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=True).tail(15)

plt.barh(importance_df['feature'], importance_df['importance'])
plt.xlabel('Importance')
plt.title('Top 15 Most Important Features in NHL xG Model', fontsize=14)
plt.tight_layout()
plt.savefig('visualizations/feature_importance.png', dpi=300, bbox_inches='tight')
print("✓ Saved feature importance chart")

# 2. Create ROC Curve
plt.figure(figsize=(8, 8))
fpr, tpr, _ = roc_curve(predictions['actual'], predictions['predicted_rf'])
model_auc = auc(fpr, tpr)

plt.plot([0, 1], [0, 1], 'k--', label='Random (AUC = 0.50)')
plt.plot(fpr, tpr, 'b-', linewidth=2, label=f'xG Model (AUC = {model_auc:.4f})')
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('NHL xG Model Performance (ROC Curve)', fontsize=14)
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/roc_curve.png', dpi=300, bbox_inches='tight')
print("✓ Saved ROC curve")

# 3. Create prediction distribution
plt.figure(figsize=(10, 6))
plt.hist(predictions[predictions['actual']==0]['predicted_rf'], bins=50, alpha=0.5, label='No Goal', density=True)
plt.hist(predictions[predictions['actual']==1]['predicted_rf'], bins=50, alpha=0.5, label='Goal', density=True)
plt.xlabel('Predicted Goal Probability (xG)', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.title('Distribution of xG Predictions by Actual Outcome', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/prediction_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Saved prediction distribution")

# 4. Create calibration plot
from sklearn.calibration import calibration_curve

plt.figure(figsize=(8, 8))
fraction_of_positives, mean_predicted_value = calibration_curve(
    predictions['actual'], predictions['predicted_rf'], n_bins=10
)

plt.plot(mean_predicted_value, fraction_of_positives, 's-', label='xG Model')
plt.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration')
plt.xlabel('Mean Predicted Probability', fontsize=12)
plt.ylabel('Fraction of Goals', fontsize=12)
plt.title('xG Model Calibration Plot', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/calibration_plot.png', dpi=300, bbox_inches='tight')
print("✓ Saved calibration plot")

# 5. Model summary statistics
print("\n=== MODEL SUMMARY ===")
print(f"Total test samples: {len(predictions):,}")
print(f"AUC: {model_auc:.4f}")
print(f"Features used: {len(feature_cols)}")
print(f"Most important feature: {importance_df.iloc[-1]['feature']}")
print(f"Actual goal rate: {predictions['actual'].mean():.3%}")
print(f"Mean predicted: {predictions['predicted_rf'].mean():.3%}")

# Save these stats to a file
with open('model_summary.txt', 'w') as f:
    f.write(f"NHL xG Model Summary\n")
    f.write(f"===================\n")
    f.write(f"AUC: {model_auc:.4f}\n")
    f.write(f"Test samples: {len(predictions):,}\n")
    f.write(f"Features: {len(feature_cols)}\n")
    f.write(f"Top feature: {importance_df.iloc[-1]['feature']}\n")