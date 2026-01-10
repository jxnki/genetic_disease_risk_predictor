import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns


sns.set_style("whitegrid")


def _fig_to_base64(fig):
    buf = io.BytesIO()
    # Ensure a solid white background so colors render correctly in browsers
    fig.patch.set_facecolor('white')
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", transparent=False)
    plt.close(fig)
    buf.seek(0)
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    return encoded


def create_thalassemia_plot(prob):
    """Create a single donut chart for Thalassemia: Affected vs Not Affected.

    `prob` is a float between 0 and 1.
    Returns base64-encoded PNG (no data-uri prefix).
    """
    labels = ["Affected", "Not Affected"]
    sizes = [prob, max(0.0, 1 - prob)]
    colors = sns.color_palette("Set2", n_colors=2)

    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    wedges, _ = ax.pie(sizes, startangle=90, colors=colors, wedgeprops=dict(width=0.4))
    ax.set(aspect="equal")
    # center text showing affected percent
    ax.text(0, 0, f"{round(prob*100,2)}%", ha="center", va="center", fontsize=14, weight='bold')
    ax.set_title("Thalassemia risk")
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5))

    return _fig_to_base64(fig)


def create_hemophilia_plot(boy_prob, girl_carrier, girl_affected):
    """Create two side-by-side donut charts for Hemophilia.

    Left: Boy (Affected vs Healthy)
    Right: Girl (Carrier vs Affected vs Normal)

    All probabilities are expected as floats in [0,1].
    Returns base64-encoded PNG (no data-uri prefix).
    """

    # Clamp values to [0,1]
    boy = min(max(boy_prob, 0.0), 1.0)
    gc = min(max(girl_carrier, 0.0), 1.0)
    ga = min(max(girl_affected, 0.0), 1.0)
    # Normalize if carrier+affected exceed 1 (safety)
    total_g = gc + ga
    if total_g > 1.0:
        gc = gc / total_g
        ga = ga / total_g
        gn = 0.0
    else:
        gn = 1.0 - total_g

    palette2 = sns.color_palette("Set2", n_colors=2)
    palette3 = sns.color_palette("Set2", n_colors=3)

    # Make the hemophilia image larger and higher resolution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=150)

    # Boy donut
    labels_boy = ["Affected", "Healthy"]
    sizes_boy = [boy, 1 - boy]
    wedges_b, _ = ax1.pie(sizes_boy, startangle=90, colors=[palette2[0], palette2[1]], wedgeprops=dict(width=0.4))
    ax1.set(aspect="equal")
    ax1.text(0, 0, f"{round(boy*100,2)}%", ha="center", va="center", fontsize=18, weight='bold')
    ax1.set_title("If Boy")
    ax1.legend(wedges_b, labels_boy, loc="center left", bbox_to_anchor=(1, 0.5))

    # Girl donut (3 categories)
    labels_girl = ["Carrier", "Affected", "Normal"]
    sizes_girl = [gc, ga, gn]
    colors_girl = [palette3[0], palette3[1], palette3[2]]
    wedges_g, _ = ax2.pie(sizes_girl, startangle=90, colors=colors_girl, wedgeprops=dict(width=0.4))
    ax2.set(aspect="equal")
    # put combined percent text for affected/carrier in center
    ax2.text(0, 0, f"Carrier: {round(gc*100,2)}%\nAffected: {round(ga*100,2)}%", ha="center", va="center", fontsize=14)
    ax2.set_title("If Girl")
    ax2.legend(wedges_g, labels_girl, loc="center left", bbox_to_anchor=(1, 0.5))

    fig.suptitle("Hemophilia risk", fontsize=18)

    return _fig_to_base64(fig)
