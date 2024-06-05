import numpy as np
from time import time
import laspy
import pandas as pd
from pypcd import pypcd
import h5py

class PC:
    def __init__(self, points = None, intensity = None, rgb = None, index = None, gps_time = None):
        self.points = points
        self.intensity = intensity
        self.rgb = rgb
        self.index = index
        self.gps_time = gps_time

    def open(self, file_path, verbose = False):
        if file_path.endswith(".h5"):
            """ open .h5 """
            if verbose:
                start = time()
                print(f"Opening file {file_path} ...")
            h5f = h5py.File(file_path,'r')
            df = h5f.get('dataset_a')[5]
            h5f.close()
            self.points = np.asarray(df[:])
            if verbose:
                end = time()-start
                print(f"Time stacking data: {end:.3f} s")
        elif file_path.endswith('.pcd'):
            """ open .pcd """
            if verbose:
                start = time()
                print(f"Opening file {file_path} ...")
            # data, ix, ii, ir, ig, iid = PC_UTILS.PCD_OPEN(file_path, verbose)
            cloud = pypcd.PointCloud.from_path(file_path)
            # data = cloud.pc_data.copy()
            data = cloud.pc_data.view(np.float32).reshape(cloud.pc_data.shape + (-1,))
            ix = cloud.get_metadata()["fields"].index('x')
            self.points = data[:,ix:ix + 3]
            try:
                ii = cloud.get_metadata()["fields"].index('Intensity')
                self.intensity = np.nan_to_num(np.asarray(data[:,ii]))
            except ValueError:
                ii = None
            try:
                ir = cloud.get_metadata()["fields"].index('rgb')
                rgb = pypcd.decode_rgb_from_pcl(data[:,ir])
                self.rgb = np.nan_to_num(rgb)
            except ValueError:
                ir = None
            try:
                ig = cloud.get_metadata()["fields"].index('GpsTime')
                self.gps_time = np.nan_to_num(np.asarray(data[:,ig]))
            except ValueError:
                ig = None
            try:
                iid = cloud.get_metadata()["fields"].index('Original_cloud_index')
                self.index = np.nan_to_num(np.asarray(data[:,iid]))
            except ValueError:
                iid = None
            if verbose:
                end = time()-start
                print(f"Time stacking data: {end:.3f} s")

        elif file_path.endswith('.las'):
            """ open .las """
            if verbose:
                start = time()
                print(f"Opening file {file_path} ...")
            las = laspy.read(file_path)
            points = np.vstack([las.points.x, las.points.y, las.points.z]).transpose()
            self.points = points
            # for dimension in las.point_format.dimensions:
            #     print(dimension.name)
            try:
                self.intensity = np.nan_to_num(np.asarray(las.intensity, dtype=np.int32))
            except:
                self.intensity = None # np.full(points.shape[0], 0)
            try:
                rgb = np.vstack([las.points.red, las.points.green, las.points.blue]).transpose()
                self.rgb = (rgb // 256).astype(np.uint8)
            except:
                self.rgb = None # np.zeros((points.shape[0], 3), dtype=np.int32)
            try:
                self.index = np.nan_to_num(np.asarray(las.point_source_id, dtype=np.float16))
            except:
                self.index = None
            try:
                self.gps_time = np.nan_to_num(np.asarray(las.GpsTime, dtype=np.float16))
            except:
                self.gps_time = None
            if verbose:
                end = time()-start
                print(f"Time stacking data: {end:.3f} s")

        elif file_path.endswith('.laz'):
            """ open .laz """
            if verbose:
                start = time()
                print(f"Opening file {file_path} ...")
            with laspy.open(file_path) as fh:
                las = fh.read()
                points = np.vstack([las.points.x, las.points.y, las.points.z]).transpose()
                self.points = points
                # for dimension in las.point_format.dimensions:
                #     print(dimension.name)
                try:
                    self.intensity = np.nan_to_num(np.asarray(las.intensity, dtype=np.int32))
                except:
                    self.intensity = None # np.full(points.shape[0], 0)
                try:
                    rgb = np.vstack([las.points.red, las.points.green, las.points.blue]).transpose()
                    self.rgb = (rgb // 256).astype(np.uint8)
                except:
                    self.rgb = None # np.zeros((points.shape[0], 3), dtype=np.int32)
                try:
                    self.index = np.nan_to_num(np.asarray(las.point_source_id, dtype=np.float16))
                except:
                    self.index = None
                try:
                    self.gps_time = np.nan_to_num(np.asarray(las.GpsTime, dtype=np.float16))
                except AttributeError:
                    self.gps_time = None
            if verbose:
                end = time()-start
                print(f"Time stacking data: {end:.3f} s")

        elif file_path.endswith('.csv'):
            """ open .csv """
            if verbose:
                start = time()
                print(f"Opening file {file_path} ...")
            df = pd.read_csv(file_path)
            self.points = df[['x', 'y', 'z']].values if 'x' in df.columns else None
            self.intensity = df['intensity'].values if 'intensity' in df.columns else None
            self.gps_time = df['GpsTime'].values if 'GpsTime' in df.columns else None
            self.index = df['index'].values if 'index' in df.columns else None
            self.rgb = df[['red', 'green', 'blue']].values if 'red' in df.columns else None
            if verbose:
                end = time()-start
                print(f"Time stacking data: {end:.3f} s")
        else:
            print("invalid format")
    def save(self, file_path, verbose = False):
        if file_path.endswith('.pcd'):
            """ save .pcd """
            if verbose:
                print(f"Saving file {file_path} ...")
                start = time()
            dt = np.zeros((len(self.points), 7), dtype=np.float32)
            dt[:, :3] = self.points
            dt[:, 3] = self.gps_time if self.gps_time is not None else None
            dt[:, 4] = self.index if self.index is not None else None
            dt[:, 5] = self.intensity if self.intensity is not None else None
            if self.rgb is not None:
                rgb = np.uint8(self.rgb)
                dt[:, 6] = pypcd.encode_rgb_for_pcl(rgb)
            md = {'version': .7,
                'fields': ['x', 'y', 'z', 'rgb', 'GpsTime', 'Original_cloud_index', 'Intensity'],
                'count': [1, 1, 1, 1, 1, 1, 1],
                'width': len(dt),
                'height': 1,
                'viewpoint': [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                'points': len(dt),
                'type': ['F', 'F', 'F', 'F', 'F', 'F', 'F'],
                'size': [4, 4, 4, 4, 4, 4, 4],
                'data': 'binary'}
            pc_data = dt.view(np.dtype([('x', np.float32),
                                            ('y', np.float32),
                                            ('z', np.float32),
                                            ('rgb', np.float32),
                                            ('GpsTime', np.float32),
                                            ('Original_cloud_index', np.float32),
                                            ('Intensity', np.float32)])).squeeze()
            new_cloud = pypcd.PointCloud(md, pc_data)
            new_cloud.save_pcd(file_path, 'binary')
            if verbose:
                end = time()-start
                print(f"Time saving: {end:.3f} s")
                
        elif file_path.endswith('.las'):
            """" save .las """
            if verbose:
                print(f"Saving file {file_path} ...")
                start = time()
            header = laspy.LasHeader(point_format=3, version="1.4")
            header.point_count = len(self.points)
            las = laspy.LasData(header)
            self.points = np.asarray(self.points, dtype=np.float32)
            las.x = self.points[:, 0]
            las.y = self.points[:, 1]
            las.z = self.points[:, 2]
            if self.rgb is not None:
                las.red = self.rgb[:, 0] * 256
                las.green = self.rgb[:, 1] * 256
                las.blue = self.rgb[:, 2] * 256
            if self.intensity is not None:
                las.intensity = self.intensity
            if self.gps_time is not None:
                las.gps_time = self.gps_time
            if self.index is not None:
                las.point_source_id = self.index
            las.write(file_path)
            if verbose:
                end = time()-start
                print(f"Time saving: {end:.3f} s")

        elif file_path.endswith('.laz'):
            """" save .laz """
            if verbose:
                print(f"Saving file {file_path} ...")
                start = time()
            header = laspy.LasHeader(point_format=3, version="1.4")
            header.point_count = len(self.points)
            las = laspy.LasData(header)
            self.points = np.asarray(self.points, dtype=np.float32)
            las.x = self.points[:, 0]
            las.y = self.points[:, 1]
            las.z = self.points[:, 2]
            if self.rgb is not None:
                las.red = self.rgb[:, 0] * 256
                las.green = self.rgb[:, 1] * 256
                las.blue = self.rgb[:, 2] * 256
            if self.intensity is not None:
                las.intensity = self.intensity
            if self.gps_time is not None:
                las.gps_time = self.gps_time
            if self.index is not None:
                las.point_source_id = self.index
            las.write(file_path)
            if verbose:
                end = time()-start
                print(f"Time saving: {end:.3f} s")

        elif file_path.endswith('.csv'):
            """" save .csv """
            if verbose:
                print(f"Saving file {file_path} ...")
                start = time()
            data = {}
            if self.points is not None:
                points = np.asarray(self.points)
                data["x"] = points[:,0]
                data["y"] = points[:,1]
                data["z"] = points[:,2]
            if self.intensity is not None:
                data["intensity"] = self.intensity
            if self.gps_time is not None:
                data["GpsTime"] = self.gps_time
            if self.index is not None:
                data["index"] = self.index
            if self.rgb is not None:
                rgb = np.asarray(self.rgb)
                data["red"] = rgb[:,0]
                data["green"] = rgb[:,1]
                data["blue"] = rgb[:,2]
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            if verbose:
                end = time()-start
                print(f"Time saving: {end:.3f} s")
        else:
            print("invalid format")