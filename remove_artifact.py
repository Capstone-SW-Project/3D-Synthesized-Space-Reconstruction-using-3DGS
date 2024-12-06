import os
import numpy as np
import argparse
from plyfile import PlyData, PlyElement
# from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN
# import hdbscan
# from sklearn.neighbors import NearestNeighbors
# from sklearn.preprocessing import StandardScaler
# from joblib import Parallel, delayed


def read_ply(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    try:
        plydata = PlyData.read(filename)
    except Exception as e:
        raise ValueError(f"Failed to read PLY file: {e}")
    
    header = plydata
    data = plydata['vertex'].data  # Access vertex data
    points = np.array([list(row) for row in data])  # Convert to numpy array
    return header, points


def write_ply(filename, header, points):
    vertex_dtype = header['vertex'].data.dtype
    filtered_data = np.empty(len(points), dtype=vertex_dtype)

    for i, name in enumerate(vertex_dtype.names):
        filtered_data[name] = points[:, i]

    vertex_element = PlyElement.describe(filtered_data, 'vertex')

    PlyData([vertex_element], text=False).write(filename)

def compute_median_distance(points, sample_size=1000):
    if len(points) > sample_size:
        indices = np.random.choice(len(points), size=sample_size, replace=False)
        sampled_points = points[indices]
    else:
        sampled_points = points
    
    dists = np.linalg.norm(sampled_points[:, np.newaxis, :3] - sampled_points[np.newaxis, :, :3], axis=2)
    dists = dists[np.triu_indices(len(sampled_points), k=1)]
    median_dist = np.median(dists)
    return median_dist

# <KDTree>
# def calc_point(points):
#     tree = cKDTree(points[:, :3])  # Use x, y, z for distance calculations
#     distances, _ = tree.query(points[:, :3], k=2)
#     nearest_neighbor_distances = distances[:, 1]  # Second nearest neighbor
#     threshold = np.mean(nearest_neighbor_distances)
#     keep_mask = nearest_neighbor_distances < threshold
#     filtered_points = points[keep_mask]
#     return filtered_points

# <DBSCAN>
def calc_point(points, eps=0.05, min_samples=10):
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points[:, :3])
    labels = clustering.labels_
    filtered_points = points[labels != -1]
    return filtered_points

# <HDBSCAN>
# def calc_point(points, min_cluster_size=10):
#     clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
#     labels = clusterer.fit_predict(points[:, :3])
#     filtered_points = points[labels != -1]
#     return filtered_points

# <mean distance>
# def knn_remover(points, k=10, threshold_multiplier=2.0):
#     nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='auto').fit(points[:, :3])
#     distances, _ = nbrs.kneighbors(points[:, :3])
#     mean_distances = distances[:, 1:].mean(axis=1)
#     overall_mean = mean_distances.mean()
#     overall_std = mean_distances.std()
#     threshold = overall_mean + threshold_multiplier * overall_std
#     keep_mask = mean_distances < threshold
#     filtered_points = points[keep_mask]
#     return filtered_points

def main():
    parser = argparse.ArgumentParser(description="Remove artifacts from a point cloud.")
    parser.add_argument('-d', '--dataset', type=str, required=True, help='Dataset name')
    args = parser.parse_args()

    dataset_path = args.dataset
    folder_path = f'output/{dataset_path}/filtered_point_cloud'
    os.makedirs(folder_path, exist_ok=True)

    dataset_name = os.path.basename(dataset_path)
    ply_file_path = f"output/{dataset_name}/point_cloud_object_decompose/iteration_30000/point_cloud.ply"
    
    header, points = read_ply(ply_file_path)

    filtered_points = calc_point(points)
    
    # scaler = StandardScaler()
    # points_normalized = scaler.fit_transform(points[:, :3])
    
    # median_dist = compute_median_distance(points, sample_size=1000)
    # print(f"Median Distance: {median_dist}")

    # filtered_points = knn_remover(points_normalized, k=10, threshold_multiplier=2.0)

    output_file = os.path.join(folder_path, "filtered_point_cloud.ply")
    write_ply(output_file, header, filtered_points)

    print(f"Original Points: {len(points)}")
    print(f"Filtered Points: {len(filtered_points)}")
    print("Filtered point cloud saved successfully")

if __name__ == "__main__":
    main()
