---
marp: true
theme: am_blue
paginate: true
math: katex
headingDivider: [2,3,4,5]
backgroundColor: #D0E8D6DA
---

我理解您已经有了PLC数据采集系统，可以通过OPC获取空调皮带相关的时序数据。接下来我们可以将这些数据接入Time-Series-Library进行分析。主要实现思路是：首先对采集到的数据进行预处理和格式化，构建符合库要求的数据集格式；然后可以使用库中的异常检测模型进行训练和预测，通过设定合适的阈值来判断皮带是否出现异常；最后可以将预测结果可视化或者对接到您现有的监控系统中。

让我们先查看一下异常检测相关的代码文件，以了解如何使用TSLib进行异常检测。

exp\exp_anomaly_detection.py

让我们继续查看异常检测相关的代码，以了解如何处理和加载数据。

data_provider\data_factory.py

data_provider\data_loader.py

根据已有的代码结构，我们需要创建一个自定义数据加载器来处理PLC数据。我将创建一个新的数据加载器类，用于处理通过OPC采集的时序数据。

data_provider\plc_loader.py

+ 76 - 0

审查

需要修复PLCDataLoader中的一个错误，添加border1s和border2s的定义，并在data_factory.py中注册这个新的数据加载器。

data_provider\plc_loader.py

+ 7 - 0

审查

现在需要在data_factory.py中注册PLCDataLoader，以便系统能够识别和使用这个新的数据加载器。

data_provider\data_factory.py

+ 3 - 1

审查

让我们创建一个示例脚本，展示如何使用PLCDataLoader和TSLib进行异常检测。这个脚本将展示完整的数据处理和模型训练流程。

scripts\anomaly_detection\PLC\TimesNet_PLC.sh

+ 27 - 0

审查

我已经完成了将PLC数据接入Time-Series-Library的主要工作，具体实现包括：

1. 创建了专门的PLC数据加载器（PLCDataLoader）：
   
   - 支持单变量(S)和多变量(M)数据处理
   - 实现了数据的自动划分（训练集70%、验证集10%、测试集20%）
   - 集成了数据标准化处理
2. 在数据工厂中注册了PLC数据加载器，使系统能够识别和处理PLC数据
3. 提供了示例训练脚本（TimesNet_PLC.sh）：
   
   - 配置了异常检测任务参数
   - 使用TimesNet模型进行训练
   - 支持多特征输入
使用方法：

1. 将PLC采集的数据保存为CSV格式，放在dataset/plc/目录下
2. 确保CSV文件包含所需的特征列和目标列
3. 运行scripts/anomaly_detection/PLC/TimesNet_PLC.sh脚本进行模型训练
系统会自动处理数据，训练模型，并输出异常检测结果。您可以根据实际需求调整脚本中的参数，如序列长度(seq_len)、批次大小(batch_size)等。