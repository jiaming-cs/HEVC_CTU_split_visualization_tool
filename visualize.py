import os
from PIL import Image
import pickle
import numpy as np
import cv2

class DataVisualization():
    def __init__(self, data_list, frame_number = None , data_folder = "./"):
        self.data_list = data_list
        self.frame_number = frame_number
        self.data_folder = data_folder
        assert(frame_number == None or len(frame_number) == len(data_list))

   
    def load(self, QP):
        def tuple_add(tuple_1, tuple_2):
            out = (tuple_1[0]+tuple_2[0], tuple_1[1]+tuple_2[1])
            return out
        x_data_64 = []
        y_data_64 = []
        x_data_32 = []
        y_data_32 = []
        x_data_16 = []
        y_data_16 = []
        for i, data in enumerate(self.data_list):
            img_path = os.path.join(self.data_folder, data, "img")
            total_frame = 0
            for file_name in os.listdir(img_path):
                if file_name.find(".png") != -1:
                    total_frame += 1
            for file_name in os.listdir(os.path.join(self.data_folder, data, str(QP))):
                if file_name.find(".pkl") != -1:
                    pkl_file = file_name
                    break
            
            with open(os.path.join(self.data_folder, data, str(QP), pkl_file), "rb") as f:
                data_dict = pickle.load(f)
                for frame in os.listdir(img_path): 
                    if frame.find(".png") == -1:
                        continue
                    img = Image.open(os.path.join(img_path, frame))
                    img_cv = cv2.imread(os.path.join(img_path, frame), cv2.IMREAD_COLOR)
                    img_cv = img_cv[:1024, :, :]
                    img_cv_avc = img_cv.copy()
                    img_array = np.array(img)

                    frame_index = int(frame.split(".")[0]) - 1 
                    img = Image.open(os.path.join(img_path, frame))
                    img_array = np.array(img)
                    height, width, _ = img_array.shape
                    cu_per_row = width // 64
                    for x in range(height // 64):
                        for y in range(width // 64):
                            cu_index = x * cu_per_row + y
                            cu = img_array[x*64:x*64+64, y*64:y*64+64, :]
                            lb_ctu_64 = np.array(data_dict[frame_index][cu_index]).reshape((4, 4))
                            
                            start_point_64 = (y*64, x*64)
                            cv2.rectangle(img = img_cv,pt1 = start_point_64, pt2 = tuple_add(start_point_64, (64, 64)), color = (255, 255, 255), thickness = 1)
                                
                            
                            if lb_ctu_64.sum() == 0: # do not split
                                x_data_64.append(cu)
                                y_data_64.append(0)
                                continue
                            else:
                                if lb_ctu_64.sum() == 16: # only split once 
                                    
                                    cv2.line(img_cv, tuple_add(start_point_64, (32, 0)), tuple_add(start_point_64, (32, 64)), (255, 255, 255))
                                    cv2.line(img_cv, tuple_add(start_point_64, (0, 32)), tuple_add(start_point_64, (64, 32)), (255, 255, 255))
                                    
                                    x_data_64.append(cu)
                                    y_data_64.append(1)
                                    continue
                                else:
                                    x_data_64.append(cu)
                                    y_data_64.append(2)
                                    for ctu_32_x in range(2):
                                        for ctu_32_y in range(2):

                                            offset_32 = (ctu_32_y*32, ctu_32_x*32)
                                            start_point_32 = tuple_add(start_point_64, offset_32)
                                            cv2.rectangle(img_cv, start_point_32, tuple_add(start_point_32, (32, 32)), (255, 255, 255))

                                            lb_ctu_32 = lb_ctu_64[ctu_32_x*2:ctu_32_x*2+2, ctu_32_y*2:ctu_32_y*2+2]
                                            ctu_32 = cu[ctu_32_x*32:ctu_32_x*32+32, ctu_32_y*32:ctu_32_y*32+32]
                                            if lb_ctu_32.sum() == 4: # do not split
                                                x_data_32.append(ctu_32)
                                                y_data_32.append(0)
                                            else:
                                                if lb_ctu_32.sum() == 8: # no more split
                                                    cv2.line(img_cv, tuple_add(start_point_32, (16, 0)), tuple_add(start_point_32, (16, 32)), (255, 255, 255))
                                                    cv2.line(img_cv, tuple_add(start_point_32, (0, 16)), tuple_add(start_point_32, (32, 16)), (255, 255, 255))
                                                        
                                                    x_data_32.append(ctu_32)
                                                    y_data_32.append(1)
                                                    continue
                                                else:
                                                    x_data_32.append(ctu_32)
                                                    y_data_32.append(2)
                                                    for ctu_16_x in range(2):
                                                        for ctu_16_y in range(2):
                                                            offset_16 = (ctu_16_y*16, ctu_16_x*16)
                                                            start_point_16 = tuple_add(start_point_32, offset_16)
                                                            cv2.rectangle(img_cv, start_point_16, tuple_add(start_point_16, (16, 16)), (255, 255, 255))
                                                            ctu_16 = ctu_32[ctu_16_x*16:ctu_16_x*16+16, ctu_16_y*16:ctu_16_y*16+16]
                                                            lb_ctu_16 = lb_ctu_32[ctu_16_x, ctu_16_y]
                                                            if lb_ctu_16 == 2:
                                                                x_data_16.append(ctu_16)
                                                                y_data_16.append(0)
                                                            else:
                                                                x_data_16.append(ctu_16)
                                                                y_data_16.append(1)
                                                                cv2.line(img_cv, tuple_add(start_point_16, (8, 0)), tuple_add(start_point_16, (8, 16)), (255, 255, 255))
                                                                cv2.line(img_cv, tuple_add(start_point_16, (0, 8)), tuple_add(start_point_16, (16, 8)), (255, 255, 255))
                    #img_cv = cv2.resize(img_cv, (img_cv.shape[1]//2, img_cv.shape[0]//2))   
                         
                    cv2.imshow("frame {}".format(frame_index+1), img_cv)
                    cv2.imwrite(f"img/{data}_HEVC_{frame}", img_cv)
                    for i in range(0, 1024, 16):    
                        cv2.line(img_cv_avc, (0, i), (1920, i), (255, 255, 255))
                    for i in range(0, 1920, 16):    
                        cv2.line(img_cv_avc, (i, 0), (i, 1024), (255, 255, 255))
                    cv2.imshow("avc {}".format(frame_index+1), img_cv_avc)
                    cv2.imwrite(f"img/{data}_AVC_{frame}", img_cv_avc)
                    cv2.waitKey(0)
                    
                    img.close()
                        
        return np.array(x_data_64), np.array(x_data_32), np.array(x_data_16), np.array(y_data_64), np.array(y_data_32), np.array(y_data_16)


  


if __name__ == "__main__":
    data_list = ["YachtRide"] # Dataset
    data_loader = DataVisualization(data_list)
    x_data_64, y_data_64, x_data_32, y_data_32, x_data_16, y_data_16 = data_loader.load(37) # QP
  