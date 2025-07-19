from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def get_metrics(y_true, y_pred):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
    }

def get_confusion_figure(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(6, 4))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="YlGnBu",
        cbar=False,
        annot_kws={"size": 14, "color": "white"},
        linewidths=0.5,
        linecolor='gray',
        ax=ax
    )

    ax.set_title("Confusion figure", fontsize=14, color='white')
    ax.set_xlabel("Predicted class", fontsize=12, color='white')
    ax.set_ylabel("Actual class", fontsize=12, color='white')
    ax.tick_params(colors='Black')  # deixa os números dos eixos visíveis
    fig.patch.set_facecolor('#0e1117')  # fundo da figura
    ax.set_facecolor('#0e1117')  # fundo da área da matriz

    return fig

def get_roc_curve(y_true, y_pred):
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    fig = px.area(x=fpr, y=tpr, title=f"Curve ROC (AUC = {roc_auc:.2f})",
                  labels={"x": "FPR", "y": "TPR"})
    return fig
