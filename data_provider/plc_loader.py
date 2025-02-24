import os
import numpy as np
import pandas as pd
from torch.utils.data import Dataset
from sklearn.preprocessing import StandardScaler

class PLCDataLoader(Dataset):
    def __init__(self, args, root_path, flag='train', size=None,
                 features='S', data_path='plc_data.csv',
                 target='target', scale=True):
        # size [seq_len, label_len, pred_len]
        self.args = args
        # info
        if size == None:
            self.seq_len = 24 * 4 * 4  # 默认使用4天的数据作为序列长度
            self.label_len = 24 * 4    # 默认使用1天的数据作为标签长度
            self.pred_len = 24 * 4     # 默认预测1天的数据
        else:
            self.seq_len = size[0]
            self.label_len = size[1]
            self.pred_len = size[2]

        # 初始化数据集类型
        assert flag in ['train', 'test', 'val']
        type_map = {'train': 0, 'val': 1, 'test': 2}
        self.set_type = type_map[flag]

        self.features = features
        self.target = target
        self.scale = scale
        self.root_path = root_path
        self.data_path = data_path
        self.__read_data__()

    def __read_data__(self):
        self.scaler = StandardScaler()
        df_raw = pd.read_csv(os.path.join(self.root_path, self.data_path))
        
        # 根据特征类型选择数据列
        if self.features == 'S':
            cols = [self.target]
        elif self.features == 'M':
            cols = df_raw.columns.tolist()
            cols.remove(self.target) if self.target in cols else cols
            cols = [self.target] + cols
        
        # 选择相关的列
        df_raw = df_raw[cols]
        
        # 数据划分边界
        num_samples = len(df_raw)
        num_train = int(num_samples * 0.7)  # 70% 用于训练
        num_val = int(num_samples * 0.1)   # 10% 用于验证
        border1s = [0, num_train - self.seq_len, num_train + num_val - self.seq_len]
        border2s = [num_train, num_train + num_val, num_samples]
        
        # 数据标准化
        if self.scale:
            train_data = df_raw[border1s[0]:border2s[0]]
            self.scaler.fit(train_data.values)
            data = self.scaler.transform(df_raw.values)
        else:
            data = df_raw.values
            
        self.data_x = data
        self.data_y = data

    def __getitem__(self, index):
        s_begin = index
        s_end = s_begin + self.seq_len
        r_begin = s_end - self.label_len
        r_end = r_begin + self.label_len + self.pred_len

        seq_x = self.data_x[s_begin:s_end]
        seq_y = self.data_y[r_begin:r_end]

        return seq_x, seq_y
    
    def __len__(self):
        return len(self.data_x) - self.seq_len - self.pred_len + 1

    def inverse_transform(self, data):
        return self.scaler.inverse_transform(data)
