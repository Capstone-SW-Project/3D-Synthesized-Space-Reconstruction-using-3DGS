# 2개의 ply (point cloud) 파일을 합치는 코드

import numpy as np
from plyfile import PlyData, PlyElement
import torch
import numpy as np
from torch import nn
import os
from plyfile import PlyData, PlyElement
import transformations as tr


def construct_list_of_attributes(features_dc, features_rest, scaling, rotation):
    l = ['x', 'y', 'z', 'nx', 'ny', 'nz']
    # All channels except the 3 DC
    for i in range(features_dc.shape[1]*features_dc.shape[2]):
        l.append('f_dc_{}'.format(i))
    for i in range(features_rest.shape[1]*features_rest.shape[2]):
        l.append('f_rest_{}'.format(i))
    l.append('opacity')
    for i in range(scaling.shape[1]):
        l.append('scale_{}'.format(i))
    for i in range(rotation.shape[1]):
        l.append('rot_{}'.format(i))
    return l


def rotate_point_cloud(point_cloud, displacement, rotation_angles, scales_bias):
    
    theta, phi, y = rotation_angles

    rotation_matrix_z = torch.tensor([
        [torch.cos(theta), -torch.sin(theta), 0],
        [torch.sin(theta),  torch.cos(theta), 0],
        [0,                0,               1]
    ]).to(point_cloud)
    rotation_matrix_x = torch.tensor([
        [1, 0,                0],
        [0, torch.cos(phi), -torch.sin(phi)],
        [0, torch.sin(phi),  torch.cos(phi)]
    ]).to(point_cloud)
    rotation_matrix_y = torch.tensor([
        [torch.cos(y), 0, torch.sin(y)],
        [0, 1, 0],
        [-torch.sin(y), 0,  torch.cos(y)]
    ]).to(point_cloud)
    rotation_matrix = torch.matmul(rotation_matrix_z, rotation_matrix_x)
    rotation_matrix = torch.matmul(rotation_matrix, rotation_matrix_y)
    # rotation_matrix = 
    # print(rotation_matrix)
    point_cloud = point_cloud*scales_bias
    rotated_point_cloud = torch.matmul(point_cloud, rotation_matrix.t())
    displaced_point_cloud = rotated_point_cloud# + displacement

    return displaced_point_cloud


def build_rotation(r):
    norm = torch.sqrt(r[:,0]*r[:,0] + r[:,1]*r[:,1] + r[:,2]*r[:,2] + r[:,3]*r[:,3])

    q = r / norm[:, None]

    R = torch.zeros((q.size(0), 3, 3), device='cuda')

    r = q[:, 0]
    x = q[:, 1]
    y = q[:, 2]
    z = q[:, 3]

    R[:, 0, 0] = 1 - 2 * (y*y + z*z)
    R[:, 0, 1] = 2 * (x*y - r*z)
    R[:, 0, 2] = 2 * (x*z + r*y)
    R[:, 1, 0] = 2 * (x*y + r*z)
    R[:, 1, 1] = 1 - 2 * (x*x + z*z)
    R[:, 1, 2] = 2 * (y*z - r*x)
    R[:, 2, 0] = 2 * (x*z - r*y)
    R[:, 2, 1] = 2 * (y*z + r*x)
    R[:, 2, 2] = 1 - 2 * (x*x + y*y)
    return R


def quaternion_rotation_matrix(Q):
    """
    Covert a quaternion into a full three-dimensional rotation matrix.
 
    Input
    :param Q: A 4 element array representing the quaternion (q0,q1,q2,q3) 
 
    Output
    :return: A 3x3 element matrix representing the full 3D rotation matrix. 
             This rotation matrix converts a point in the local reference 
             frame to a point in the global reference frame.
    """
    # Extract the values from Q
    q0 = Q[:,0].detach().cpu().numpy()
    q1 = Q[:,1].detach().cpu().numpy()
    q2 = Q[:,2].detach().cpu().numpy()
    q3 = Q[:,3].detach().cpu().numpy()
     
    # First row of the rotation matrix
    r00 = 2 * (q0 * q0 + q1 * q1) - 1
    r01 = 2 * (q1 * q2 - q0 * q3)
    r02 = 2 * (q1 * q3 + q0 * q2)
     
    # Second row of the rotation matrix
    r10 = 2 * (q1 * q2 + q0 * q3)
    r11 = 2 * (q0 * q0 + q2 * q2) - 1
    r12 = 2 * (q2 * q3 - q0 * q1)
     
    # Third row of the rotation matrix
    r20 = 2 * (q1 * q3 - q0 * q2)
    r21 = 2 * (q2 * q3 + q0 * q1)
    r22 = 2 * (q0 * q0 + q3 * q3) - 1
     
    # 3x3 rotation matrix
    rot_matrix = np.array([[r00, r01, r02],
                           [r10, r11, r12],
                           [r20, r21, r22]])
                            
    return rot_matrix

def rotation_to_quaternion(R):
    r11, r12, r13 = R[:, 0, 0], R[:, 0, 1], R[:, 0, 2]
    r21, r22, r23 = R[:, 1, 0], R[:, 1, 1], R[:, 1, 2]
    r31, r32, r33 = R[:, 2, 0], R[:, 2, 1], R[:, 2, 2]

    qw = torch.sqrt((1 + r11 + r22 + r33).clamp_min(1e-7)) / 2
    qx = (r32 - r23) / (4 * qw)
    qy = (r13 - r31) / (4 * qw)
    qz = (r21 - r12) / (4 * qw)

    quaternion = torch.stack((qw, qx, qy, qz), dim=-1)
    quaternion = torch.nn.functional.normalize(quaternion, dim=-1)
    return quaternion


def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1[:, 0], q1[:, 1], q1[:, 2], q1[:, 3]
    w2, x2, y2, z2 = q2[:, 0], q2[:, 1], q2[:, 2], q2[:, 3]

    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2

    result_quaternion = torch.stack((w, x, y, z), dim=1)
    return result_quaternion


def quaternion_to_rotation_matrix(q):
    w, x, y, z = q[:, 0], q[:, 1], q[:, 2], q[:, 3]

    r11 = 1 - 2 * y * y - 2 * z * z
    r12 = 2 * x * y - 2 * w * z
    r13 = 2 * x * z + 2 * w * y

    r21 = 2 * x * y + 2 * w * z
    r22 = 1 - 2 * x * x - 2 * z * z
    r23 = 2 * y * z - 2 * w * x

    r31 = 2 * x * z - 2 * w * y
    r32 = 2 * y * z + 2 * w * x
    r33 = 1 - 2 * x * x - 2 * y * y

    rotation_matrix = torch.stack((torch.stack((r11, r12, r13), dim=1),
                                   torch.stack((r21, r22, r23), dim=1),
                                   torch.stack((r31, r32, r33), dim=1)), dim=1)
    return rotation_matrix


def load_ply(path):
    plydata = PlyData.read(path)

    xyz = np.stack((np.asarray(plydata.elements[0]["x"]),
                    np.asarray(plydata.elements[0]["y"]),
                    np.asarray(plydata.elements[0]["z"])),  axis=1)
    opacities = np.asarray(plydata.elements[0]["opacity"])[..., np.newaxis]

    features_dc = np.zeros((xyz.shape[0], 3, 1))
    features_dc[:, 0, 0] = np.asarray(plydata.elements[0]["f_dc_0"])
    features_dc[:, 1, 0] = np.asarray(plydata.elements[0]["f_dc_1"])
    features_dc[:, 2, 0] = np.asarray(plydata.elements[0]["f_dc_2"])

    extra_f_names = [p.name for p in plydata.elements[0].properties if p.name.startswith("f_rest_")]
    extra_f_names = sorted(extra_f_names, key = lambda x: int(x.split('_')[-1]))
    assert len(extra_f_names)==3*(3 + 1) ** 2 - 3
    features_extra = np.zeros((xyz.shape[0], len(extra_f_names)))
    for idx, attr_name in enumerate(extra_f_names):
        features_extra[:, idx] = np.asarray(plydata.elements[0][attr_name])
    features_extra = features_extra.reshape((features_extra.shape[0], 3, (3 + 1) ** 2 - 1))

    scale_names = [p.name for p in plydata.elements[0].properties if p.name.startswith("scale_")]
    scale_names = sorted(scale_names, key = lambda x: int(x.split('_')[-1]))
    scales = np.zeros((xyz.shape[0], len(scale_names)))
    for idx, attr_name in enumerate(scale_names):
        scales[:, idx] = np.asarray(plydata.elements[0][attr_name])

    rot_names = [p.name for p in plydata.elements[0].properties if p.name.startswith("rot")]
    rot_names = sorted(rot_names, key = lambda x: int(x.split('_')[-1]))
    rots = np.zeros((xyz.shape[0], len(rot_names)))
    for idx, attr_name in enumerate(rot_names):
        rots[:, idx] = np.asarray(plydata.elements[0][attr_name])

    xyz = nn.Parameter(torch.tensor(xyz, dtype=torch.float, device="cuda").requires_grad_(True))
    features_dc = nn.Parameter(torch.tensor(features_dc, dtype=torch.float, device="cuda").transpose(1, 2).contiguous().requires_grad_(True))
    features_rest = nn.Parameter(torch.tensor(features_extra, dtype=torch.float, device="cuda").transpose(1, 2).contiguous().requires_grad_(True))
    opacity = nn.Parameter(torch.tensor(opacities, dtype=torch.float, device="cuda").requires_grad_(True))
    scaling = nn.Parameter(torch.tensor(scales, dtype=torch.float, device="cuda").requires_grad_(True))
    rotation = nn.Parameter(torch.tensor(rots, dtype=torch.float, device="cuda").requires_grad_(True))

    active_sh_degree = 3

    return xyz, features_dc, features_rest, opacity, scaling, rotation


def save_ply(xyz, features_dc, features_rest, opacity, scaling, rotation, savepath):
        xyz = xyz.detach().cpu().numpy()
        normals = np.zeros_like(xyz)
        f_dc = features_dc.detach().transpose(1, 2).flatten(start_dim=1).contiguous().cpu().numpy()
        f_rest = features_rest.detach().transpose(1, 2).flatten(start_dim=1).contiguous().cpu().numpy()
        opacities = opacity.detach().cpu().numpy()
        scale = scaling.detach().cpu().numpy()
        rotation = rotation.detach().cpu().numpy()

        dtype_full = [(attribute, 'f4') for attribute in construct_list_of_attributes(features_dc, features_rest, scaling, rotation)]

        elements = np.empty(xyz.shape[0], dtype=dtype_full)
        attributes = np.concatenate((xyz, normals, f_dc, f_rest, opacities, scale, rotation), axis=1)
        elements[:] = list(map(tuple, attributes))
        el = PlyElement.describe(elements, 'vertex')
        PlyData([el]).write(savepath + '/point_cloud.ply')

# 객체의 point cloud
xyz1, features_dc1, features_rest1, opacity1, scaling1, rotation1= load_ply("객체 point cloud 경로")
# 배경의 point cloud
xyz2, features_dc2, features_rest2, opacity2, scaling2, rotation2= load_ply("배경 point cloud 경로")

# 객체 주변의 미세한 noise를 제거하려면 1, 아니면 0
filtering =1
if filtering:
    idx = torch.where(opacity1>opacity1.mean())[0]
    xyz1 = xyz1[idx]
    features_dc1 = features_dc1[idx]
    features_rest1 = features_rest1[idx]
    opacity1 = opacity1[idx]
    scaling1 = scaling1[idx]
    rotation1 = rotation1[idx]

    
print("front : ", xyz1.shape[0])
print("back : ", xyz2.shape[0])

savepath = '저장 경로'

scaling_inverse_activation = torch.log
# CloudCompare에서 가져온 transform matrix 입력
transform = torch.tensor(
    [[1.000000, 0.000000, 0.000000, 0.000000],
     [0.000000, 1.000000, 0.000000, 0.000000],
     [0.000000, 0.000000, 1.000000, 0.000000],
     [0.000000, 0.000000, 0.000000, 1.000000]], device="cuda")
save_transform = transform.cpu().numpy()

np.savetxt(savepath + '/transform.txt', save_transform)
np.savetxt(savepath + '/num_points.txt', np.array(xyz1.shape), fmt='% 06d')


scale = transform[:3, :3].norm(dim=-1).to('cuda')
scaling1 = scaling_inverse_activation(torch.exp(scaling1) * scale)
xyz_homo = torch.cat([xyz1, torch.ones_like(xyz1[:, :1])], dim=-1)
xyz1 = (xyz_homo @ transform.T)[:, :3]
rotation = transform[:3, :3] / scale[:, None]
rotation_q = rotation_to_quaternion(rotation[None])
rotation1 = quaternion_multiply(rotation_q, rotation1)

xyz = torch.concat([xyz1, xyz2])
features_dc = torch.concat([features_dc1,features_dc2])
features_rest = torch.concat([features_rest1,features_rest2])
opacity = torch.concat([opacity1,opacity2])
scaling = torch.concat([scaling1 ,scaling2])
rotation = torch.concat([rotation1,rotation2])

save_ply(xyz, features_dc, features_rest, opacity, scaling, rotation, savepath)

print('complete')