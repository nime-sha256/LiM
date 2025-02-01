import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import xgboost as xgb
from sklearn.metrics import classification_report, accuracy_score

# Load the dataframe from NetMatrix
df = pd.read_csv('./cstnet-tls1.3_5_packets.csv')

# Define feature columns and the label column
feature_columns = [col for col in df.columns if col != 'label']

label_column = 'label'

# Split the data into features and labels
X = df[feature_columns]
y = df[label_column]

# Encode the categorical labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Identify categorical and numerical columns
numerical_features = feature_columns 

# Preprocessing for numerical data: StandardScaler
numerical_transformer = StandardScaler()

# Apply preprocessing to the data
# For numerical features
X_numerical = numerical_transformer.fit_transform(X[numerical_features])

# Combine preprocessed features
X_preprocessed = np.hstack([X_numerical])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y_encoded, test_size=0.2, random_state=42)

# Train the XGBoost model
xgb_classifier = xgb.XGBClassifier(eval_metric='mlogloss')

xgb_classifier.fit(X_train, y_train)

# Make predictions
y_pred = xgb_classifier.predict(X_test)

# Decode the predictions and true values back to original labels
y_pred_decoded = label_encoder.inverse_transform(y_pred)
y_test_decoded = label_encoder.inverse_transform(y_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test_decoded, y_pred_decoded))
print("Classification Report:\n", classification_report(y_test_decoded, y_pred_decoded))