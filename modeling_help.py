import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# profiling packages
from ydata_profiling import ProfileReport

# modeling packages
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve, precision_recall_curve, accuracy_score

# can you wrap this analysis into a function that takes in the model object you create and returns the evaluation metrics?
def evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)

    # make predictions
    y_pred = model.predict(X_test)

    # evaluate the model
    print('Model Evaluation on Test Data:')
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc_score_var = roc_auc_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')
    print(f'ROC AUC Score: {roc_auc_score_var}')

    # create a confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    print(conf_matrix)

    # create a classification report
    class_report = classification_report(y_test, y_pred)
    print(class_report)

    # create a ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, y_pred)

    plt.plot(fpr, tpr)
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.show()

    # create a precision-recall curve
    precision, recall, thresholds = precision_recall_curve(y_test, y_pred)

    plt.plot(recall, precision)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.show()

    print('Model Evaluation on Train Data: Want to see how this may be overfitting...')
    y_pred_train = model.predict(X_train)

    # evaluate the model
    accuracy_train = accuracy_score(y_train, y_pred_train)
    roc_auc_score_var_train = roc_auc_score(y_train, y_pred_train)
    print(f'Accuracy: {accuracy_train}')
    print(f'ROC AUC Score: {roc_auc_score_var_train}')

    # create a confusion matrix
    conf_matrix_train = confusion_matrix(y_train, y_pred_train)
    print(conf_matrix_train)

    # create a classification report
    class_report_train = classification_report(y_train, y_pred_train)
    print(class_report_train)

    # create a ROC curve
    fpr_train, tpr_train, thresholds_train = roc_curve(y_train, y_pred_train)

    plt.plot(fpr_train, tpr_train)
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.show()

    # create a precision-recall curve
    precision_train, recall_train, thresholds_train = precision_recall_curve(y_train, y_pred_train)

    plt.plot(recall_train, precision_train)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.show()
    
    return accuracy, roc_auc_score_var, conf_matrix, class_report, fpr, tpr, precision, recall