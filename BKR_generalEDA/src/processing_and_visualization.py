import os
import joblib
import pandas as pd
import numpy as np
import duckdb
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import HTML
import io
import sys
# -------------------------------------------------------------------
# Quick save various files in data directory if they do not already exist
# -------------------------------------------------------------------
def quick_save_file(data_dir, filename, obj):
    """
    Save an object to the specified data directory if it does not already exist.
    Automatically handles pandas DataFrames and NumPy arrays for optimal speed.
    
    Parameters:
        data_dir (str): Directory where the file should be saved.
        filename (str): Name of the file (include extension, e.g., .pkl, .parquet, .npy).
        obj: Object to save. If filename ends with .parquet, obj must be a pandas DataFrame.
             If obj is a NumPy array, it will be saved as .npy for speed if possible.
    """
    path = os.path.join(data_dir, filename)
    
    if os.path.exists(path):
        print(f"{filename} already exists. Skipping save.")
        return

    # Handle pandas DataFrames
    if isinstance(obj, pd.DataFrame) or filename.endswith(".parquet"):
        obj.to_parquet(path)
    # Handle NumPy arrays
    elif isinstance(obj, np.ndarray):
        # Ensure .npy extension for speed
        if not filename.endswith(".npy"):
            path = os.path.splitext(path)[0] + ".npy"
        np.save(path, obj)
    # Fallback for other objects
    else:
        joblib.dump(obj, path)  # turn off compression for speed
    
    print(f"Saved {os.path.basename(path)}")


# -------------------------------------------------------------------
# Save output of UMAP and HDBSCAN clustering for a set topic
# -------------------------------------------------------------------

def save_topic_files(data_dir, topic, clusterer, umap_embedding, df):
    """
    Saves the clusterer, UMAP embedding, and clustered DataFrame for a given topic.
    
    Parameters:
        data_dir (str): Directory where files should be saved.
        topic (str): Topic name used in filenames.
        clusterer: The clustering model object to save (e.g., HDBSCAN).
        umap_embedding: The UMAP embedding object to save.
        df: The clustered DataFrame to save as parquet.
    """
    files_to_save = {
        f"{topic}_hdbscan_model.pkl": clusterer,
        f"{topic}_umap_embedding.pkl": umap_embedding,
        f"{topic}_clustered_df.parquet": df
    }

    for filename, obj in files_to_save.items():
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            if filename.endswith(".parquet"):
                obj.to_parquet(path)
            else:
                joblib.dump(obj, path)
            print(f"Saved {filename}")
        else:
            print(f"{filename} already exists. Skipping save.")

# -------------------------------------------------------------------
# Save minimal question cluster data with UMAP embeddings to be reattached to full dataset
# -------------------------------------------------------------------

def save_question_clusters(df, embedding_2d, topic, folder='../data'):
    """
    Save minimal question cluster data with UMAP embeddings.

    Parameters
    ----------
    df : pd.DataFrame
        Original DataFrame with 'question_id', 'cluster', 'meta_label'.
    embedding_2d : np.ndarray
        2D UMAP embeddings (n_rows, 2).
    topic : str
        Topic name (e.g., 'unlabeled', 'chicken', 'maize').
    folder : str
        Folder to save the Parquet file.
    """
    minimal_df = df[['question_id', 'meta_label', 'cluster']].copy()
    # Downcast integer columns
    minimal_df = minimal_df.astype({'question_id': 'int32',
                                    'cluster': 'int32',
                                    'meta_label': 'int32'})
    # Add 2D UMAP embeddings as float32
    minimal_df['umap_x'] = embedding_2d[:, 0].astype('float32')
    minimal_df['umap_y'] = embedding_2d[:, 1].astype('float32')
    
    filename = f"{folder}/question_clusters_{topic}.parquet"
    minimal_df.to_parquet(filename, index=False)
    print(f"Saved {filename} ({minimal_df.shape[0]} rows)")


# -------------------------------------------------------------------
# Load and join question data with embeddings
# -------------------------------------------------------------------


def load_clustered_questions(full_path, cluster_path, topic):
    """
    Load the large WeFarm 'full dataset' (e.g. "b0cd514b-b9cc-4972-a0c2-c91726e6d825.csv", CSV or Parquet) and join it with the cluster
    annotation file (always Parquet). Returns a Pandas DataFrame of the joined data.
    """

    full_path = Path(full_path)
    cluster_path = Path(cluster_path)

    con = duckdb.connect()

    # Detect the format of the full dataset
    if full_path.suffix.lower() in ['.csv', '.txt']:
        full_reader = f"read_csv_auto('{full_path.as_posix()}', HEADER=True)"
    elif full_path.suffix.lower() in ['.parquet']:
        full_reader = f"read_parquet('{full_path.as_posix()}')"
    else:
        raise ValueError(f"Unsupported full dataset file type: {full_path.suffix}")

    # Build WHERE clause for topic
    if topic is None:
        where_clause = "WHERE f.question_topic IS NULL AND f.question_language = 'eng'"
    else:
        where_clause = f"WHERE f.question_topic = '{topic}' AND f.question_language = 'eng'"

    # Cluster labels are always Parquet
    cluster_reader = f"read_parquet('{cluster_path.as_posix()}')"

    query = f"""
    SELECT f.question_id, f.question_content, c.cluster, c.meta_label, c.umap_x, c.umap_y
    FROM {full_reader} AS f
    RIGHT JOIN {cluster_reader} AS c
    ON f.question_id = c.question_id
    {where_clause}
    """

    df = con.execute(query).df()
    df = df.drop_duplicates(subset='question_id', keep='first')

    return df

# -------------------------------------------------------------------
# Plot metacluster distribution with raw counts and percentages
# -------------------------------------------------------------------

def plot_metacluster_distribution(df, label_col='meta_label_titles', noise_col='meta_label', noise_val=-1, title="Metacluster Distribution"):
    """
    Plot a bar chart of the number of questions per metacluster (raw counts on x-axis), 
    with percentages annotated above each bar. Excludes the noise cluster from the bars,
    but shows the proportion of noise questions in the top-right corner.

    Parameters:
        df (pd.DataFrame): DataFrame containing questions
        label_col (str): Column with metacluster names
        noise_col (str): Column indicating the cluster label
        noise_val: Value representing the noise cluster (default -1)
        title (str): Title for the plot
    """
    # Separate noise and non-noise
    noise_mask = df[noise_col] == noise_val
    noise_count = noise_mask.sum()
    classified_df = df[~noise_mask]

    # Count questions per metacluster
    meta_counts = classified_df[label_col].value_counts().sort_values(ascending=False)
    total_classified = meta_counts.sum()

    # Compute percentages for annotations
    meta_percent = (meta_counts / total_classified) * 100

    # Colors
    palette = sns.color_palette("Set2", n_colors=len(meta_counts))

    # Plot raw counts
    plt.figure(figsize=(10,6))
    bars = plt.bar(meta_counts.index, meta_counts.values, color=palette, edgecolor='k')

    # Rotate x labels
    plt.xticks(rotation=45, ha='right', fontsize=11)
    plt.ylabel('Number of Questions', fontsize=12)
    plt.xlabel('Metacluster', fontsize=12)
    plt.title(title, fontsize=14)

    # Annotate % above bars
    for bar, pct in zip(bars, meta_percent.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + total_classified*0.005, f'{pct:.1f}%', 
                 ha='center', va='bottom', fontsize=10)

    # Annotate noise percentage in top-right corner
    total_questions = len(df)
    noise_percent_total = noise_count / total_questions * 100
    plt.text(0.95, 0.95, f"Noise: {noise_percent_total:.1f}%", 
             ha='right', va='top', fontsize=12, fontweight='bold', transform=plt.gca().transAxes)

    # Adjust y-axis for padding above bars
    plt.ylim(0, max(meta_counts.values)*1.2)

    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------------
#  Plot UMAP centroids of clusters with fixed axes and custom colors
# -------------------------------------------------------------------

import pandas as pd
import plotly.express as px

def plot_umap_centroids(df, cluster_col='cluster', meta_col='meta_label', title_col='meta_label_titles',
                         umap_x_col='umap_x', umap_y_col='umap_y', 
                         size_scale=2.0, size_max=120, title="Centroid Map of Clusters in 2D UMAP Space",
                         noise_val=-1, noise_color='lightgray'):
    """
    Plot cluster centroids in 2D UMAP space using Plotly.
    Axes remain fixed when selecting/highlighting clusters.
    Noise cluster is colored differently (default light gray).
    Uses human-readable titles for the legend, ordered numerically by cluster.

    Parameters:
        df (pd.DataFrame): DataFrame with UMAP coordinates and cluster info.
        cluster_col (str): Column name for clusters.
        meta_col (str): Column name for metaclusters.
        title_col (str): Column containing descriptive metacluster titles.
        umap_x_col (str): Column name for UMAP x-coordinates.
        umap_y_col (str): Column name for UMAP y-coordinates.
        size_scale (float): Scale factor for centroid point sizes.
        size_max (float): Maximum size for points.
        title (str): Plot title.
        noise_val: Value representing noise cluster.
        noise_color: Color for noise cluster points.
    """
    # Aggregate centroids
    centroids = (
        df.groupby([cluster_col, meta_col, title_col], as_index=False)
          .agg(
              **{
                  umap_x_col: (umap_x_col, 'mean'),
                  umap_y_col: (umap_y_col, 'mean'),
                  'size': (cluster_col, 'count')
              }
          )
    )

    # Order clusters numerically
    ordered_labels = sorted(centroids[meta_col].unique())
    centroids[meta_col] = centroids[meta_col].astype('category')
    centroids[meta_col] = centroids[meta_col].cat.set_categories(ordered_labels, ordered=True)

    # Color map
    qual_colors = px.colors.qualitative.Plotly
    color_map = {}
    i = 0
    for label in ordered_labels:
        if label == noise_val:
            color_map[label] = noise_color
        else:
            color_map[label] = qual_colors[i % len(qual_colors)]
            i += 1

    # Legend labels: just human-readable titles
    centroids['legend_title'] = centroids[title_col]

    # Scale sizes
    centroids['scaled_size'] = centroids['size'] * size_scale

    # Axis ranges for square-ish layout
    x_range = [centroids[umap_x_col].min() - 1, centroids[umap_x_col].max() + 1]
    y_range = [centroids[umap_y_col].min() - 1, centroids[umap_y_col].max() + 1]

    # Plot
    fig = px.scatter(
        centroids,
        x=umap_x_col,
        y=umap_y_col,
        color='legend_title',
        color_discrete_map={row['legend_title']: color_map[row[meta_col]] 
                            for _, row in centroids.iterrows()},
        size='scaled_size',
        size_max=size_max,
        category_orders={'legend_title': [centroids[centroids[meta_col]==label][title_col].iloc[0] 
                                          for label in ordered_labels]},
        hover_data={
            cluster_col: True,
            meta_col: True,
            title_col: True,
            'size': True,
            umap_x_col: ':.2f',
            umap_y_col: ':.2f'
        }
    )

    fig.update_layout(
        title=f"<b>{title}</b>",
        width=800,
        height=800,
        legend_title="Meta-Cluster",
        xaxis=dict(scaleanchor="y", scaleratio=1, range=x_range),
        yaxis=dict(scaleanchor="x", scaleratio=1, range=y_range),
        legend=dict(
            itemclick="toggleothers",
            itemdoubleclick="toggle",
            traceorder="normal",  # preserves the order
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02  # move legend slightly outside to keep plot area square
        )
    )

    fig.update_traces(
        selected=dict(marker=dict(opacity=1)),
        unselected=dict(marker=dict(opacity=0.15))
    )

    fig.show()


# -------------------------------------------------------------------
#  Wrapper function to make scrollable output display on GitHub
# -------------------------------------------------------------------


def collapsible_preview(func, *args, summary_label="Show output", max_height="400px", **kwargs):
    """
    Runs a function that prints output, captures the printed text,
    and displays it in a collapsible, scrollable block.
    
    Returns whatever the function normally returns (e.g. a DataFrame).
    """
    
    # Capture printed output
    buffer = io.StringIO()
    stdout_original = sys.stdout
    sys.stdout = buffer
    
    result = func(*args, **kwargs)
    
    sys.stdout = stdout_original
    preview_text = buffer.getvalue()

    # Collapsible + scrollable block
    display(HTML(f"""
    <details>
      <summary>{summary_label}</summary>
      <div style="max-height: {max_height}; overflow-y: auto; border: 1px solid #ccc; padding: 8px;">
        <pre>{preview_text}</pre>
      </div>
    </details>
    """))
    
    return result
