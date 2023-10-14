# ChurnGuardian
<img src="https://github.com/FTDS-assignment-bay/FTDS-007-HCK-group-002/blob/main/assets/ChurnGuardian-Logo-Transparants.png?raw=true" width="50%">

<h3 align="left"><a href="https://huggingface.co/spaces/Irfnn/Final_Projects">Machine learning application to predict customer churn and loyalty, and clusters customers for targeted strategies.</a></h3>

- [Edy Setiawan](https://www.linkedin.com/in/edysetiawan/)


## Project's Background

**Background:**

The telecommunications industry is highly competitive, and customer churn is a significant concern. Retaining existing customers is often more cost-effective than acquiring new ones. Therefore, predicting customer churn and understanding the underlying reasons can provide invaluable insights for customer retention strategies.

**Problem Statement:**

To develop a machine learning model that predicts customer churn in the telecommunications industry with at least 80% recall score, and to segment the identified "at-risk" customers into clusters for targeted retention strategies.

## Datasets

**Dataset Overview:**

- Dataset Source: This dataset is obtained from the Kaggle public dataset
- This dataset contains information about customers in the telecommunications industry, focusing on various attributes that could be indicative of customer churn

## Objectives

- Data Preparation and Exploration: To clean and explore the dataset to understand the variables that influence customer churn.
- Predictive Modeling: To develop a classification model that can predict customer churn with an accuracy of at least 85%.
- Clustering Analysis: To segment the customers predicted as 'Churn' into different clusters based on their characteristics.
- Retention Strategy: To propose targeted retention strategies for each identified cluster.
- Evaluation: To evaluate the effectiveness of the model and the proposed retention strategies within a set timeframe (e.g., 3 months).

<h3 align="left">WORKFLOW CHART</h3>
<img src="https://github.com/FTDS-assignment-bay/FTDS-007-HCK-group-002/blob/main/assets/Flowchart_Fix.png?raw=true" width="50%">

## Demo

- App Demo Link : https://huggingface.co/spaces/eeeeeedy/churnguardian
  . Note: if app is not loading, please click "Restart this Space" button


- How to use the app video: [Watch the Video](https://www.youtube.com/watch?v=O-dJi6GAvT8)

## Technology Stacks

#### Data Manipulation and Analysis:
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

#### Data Preprocessing:
- **Scikit-learn (sklearn)**: Various preprocessing techniques
- **Imbalanced-learn (imblearn)**: Pipeline construction

#### Machine Learning Algorithms:
- **Scikit-learn (sklearn)**
  - KMeans: Clustering
  - Gradient Boosting: Classification
  - Random Forest: Classification
  - k-Nearest Neighbors (k-NN): Classification
  - Decision Trees: Classification
  - Support Vector Machines (SVM): Classification
  - Logistic Regression: Classification
- **Hugging Face**: Model deployment

#### Model Evaluation Techniques:
- **Scikit-learn (sklearn)**
  - Stratified K-Fold: Cross-validation
  - Randomized Search CV: Hyperparameter tuning
  - Metrics: 
    - F1 Score
    - Recall
    - Precision
    - Accuracy
    - ROC-AUC
  - Confusion Matrix
  - Precision-Recall Curve
  - ROC Curve
  
#### Dimensionality Reduction:
- **Scikit-learn (sklearn)**: Principal Component Analysis (PCA)

#### Data Visualization:
- **Matplotlib**: Plotting and visualization

#### Data Pipeline Automation:
- **Apache Airflow**: Workflow automation
  - Data ingestion to Postgres
  - Data cleaning
  - Pushing cleaned data back to Postgres

#### Databases:
- **PostgreSQL (Postgres)**: Relational database

#### Miscellaneous:
- **Python's Standard Library**: Warning control
