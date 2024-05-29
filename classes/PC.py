import numpy as np
import pprint
from time import time
from .PC_UTILS import PC_UTILS
import laspy
import pandas as pd


class PC:
    def __init__(self, points = None, intensity = None, rgb = None, index = None, gps_time = None):
        self.points = points
        self.intensity = intensity
        self.rgb = rgb
        self.index = index
        self.gps_time = gps_time

    def open(self, file_path, verbose = False):
        """ open .pcd """
        if file_path.endswith('.pcd'):
            if verbose:
                start = time()
                print(f"Opening .pcd file ...")
            data, ix, ii, ir, ig, iid = PC_UTILS.PCD_OPEN(file_path, verbose)
            if verbose:
                end = time()-start
                print(f"Time reading: {end:.3f} s")
                start = time()
            points = data[:,ix:ix + 3]
            rgb = np.asarray(data[:,ir]) if ir is not None else None
            rgb = np.nan_to_num(rgb)
            intensity = np.asarray(data[:,ii]) if ii is not None else None
            intensity = np.nan_to_num(intensity)
            gps_time = np.nan_to_num(np.asarray(data[:,ig])) if ig is not None else None
            index = np.nan_to_num(np.asarray(data[:,iid])) if iid is not None else None
            if verbose:
                end = time()-start
                print(f"Time stacking data: {end:.3f} s")
            self.points, self.intensity, self.rgb, self.index, self.gps_time = points, intensity, rgb, index, gps_time

        if file_path.endswith('.las'):
            """ open .las """
            if verbose:
                start = time()
                print(f"Opening .las file ...")
            las = laspy.read(file_path)
            points = np.vstack([las.points.x, las.points.y, las.points.z]).transpose()
            intensity = np.full(points.shape[0], 0)
            rgb = np.full(points.shape[0], 0)
            index = np.full(points.shape[0], 0)
            gps_time = np.full(points.shape[0], 0)
            for dimension in las.point_format.dimensions:
                print(dimension.name)
            try:
                intensity = np.asarray(las.intensity, dtype=np.int32)
                intensity = np.nan_to_num(intensity)
            except AttributeError:
                pass
            try:
                red = np.asarray(las.red, dtype=np.int32)
                green = np.asarray(las.green, dtype=np.int32)
                blue = np.asarray(las.blue, dtype=np.int32)
                rgb = PC_UTILS.get_color_float(red, green, blue)
                rgb = np.nan_to_num(rgb)
            except AttributeError:
                pass
            try:
                index = np.asarray(las.point_source_id, dtype=np.float16)
                index = np.nan_to_num(index)
            except AttributeError:
                pass
            try:
                gps_time = np.asarray(las.GpsTime, dtype=np.float16)
                gps_time = np.nan_to_num(gps_time)
            except AttributeError:
                pass
            if verbose:
                end = time()-start
                print(f"Time stacking data: {end:.3f} s")
            self.points, self.intensity, self.rgb, self.index, self.gps_time = points, intensity, rgb, index, gps_time

        if file_path.endswith('.csv'):
            """ open .csv """
            if verbose:
                start = time()
                print(f"Opening .csv file ...")
            df = pd.read_csv(file_path)
            self.points = df[['x', 'y', 'z']].values if 'x' in df.columns else None
            self.intensity = df['intensity'].values if 'intensity' in df.columns else None
            self.gps_time = df['GpsTime'].values if 'GpsTime' in df.columns else None
            self.index = df['index'].values if 'index' in df.columns else None
            self.rgb = df['rgb'].values if 'rgb' in df.columns else None
            if verbose:
                end = time()-start
                print(f"Time stacking data: {end:.3f} s")

    def save(self, file_path, verbose = False):
        """ save .pcd """
        if file_path.endswith('.pcd'):
            if verbose:
                print(f"Saving .pcd file ...")
                start = time()
            self.points = np.asarray(self.points)
            if self.intensity == None:
                self.intensity = np.full(self.points.shape[0], 0)
            dt = np.c_[self.points, self.intensity]
            dt = np.array(dt, dtype=np.float32)
            new_cloud = PC_UTILS.make_xyz_intensity_point_cloud(dt)
            if verbose:
                pprint.pprint(new_cloud.get_metadata())
                print(dt, dt.shape)
            new_cloud.save_pcd(file_path, 'binary')
            if verbose:
                end = time()-start
                print(f"Time saving: {end:.3f} s")
#"""" save .las """
        if file_path.endswith('.las'):
            if verbose:
                print(f"Saving .pcd file ...")
                start = time()
            header = laspy.header.Header()
            header.version = '1.4'
            # header.scale = np.array([0.01, 0.01, 0.01])  # Шкала в метрах
            # header.offset = np.array([100000, 200000, 300000])  # Смещение в метрах
            header.point_format = laspy.format.PointFormat.XYZRGBI
            header.point_count = len(self.points)

            las = laspy.LasData(header)
            las.x = self.points[:, 0]
            las.y = self.points[:, 1]
            las.z = self.points[:, 2]
            las.red = self.rgb
            las.green = self.rgb
            las.blue = self.rgb
            las.intensity = self.intensity
            las.gps_time = self.gps_time
            las.point_source_id = self.index

            las.write(file_path)
            if verbose:
                end = time()-start
                print(f"Time saving: {end:.3f} s")

#"""" save .csv """
        if file_path.endswith('.csv'):
            if verbose:
                print(f"Saving .csv file ...")
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
                data["rgb"] = self.rgb
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            if verbose:
                end = time()-start
                print(f"Time saving: {end:.3f} s")