智能汽车
转至元数据结尾
创建： 张腾元，最新修改于： 2018-05-10 转至元数据起始
状态	DEV
干系人	张腾元,周从军 郑晓旭
结果	高优进行Lane Detection功能实现
到期日	2018-05-20
拥有者	 
背景
智能汽车-Lane Detection 算法与工作计划  

Lane Detection 效果指导

指导视频

Lane detection and steering module with OpenCV & Arduino

Fast and Robust Lane Detection using OpenCV

Ddge Detection 道路识别和检测主要工作点： 周从军  2018-05-09 
 Camera图像去扭曲       Undistort (Camera Lens Distotion OpenCV cv2.undistort )
 图像灰度处理                Warp (Warp Images )
 边缘检测与道路线识别  Isolate line 
 拟合道路虚线                Curve fit
 标注道路区域                Final image
 计算Camera中线与道路中线的偏移值   


Steering Advise    张腾元  2018-05-09 


Car Detection      郑晓旭   2018-05-09 
车辆识别
车辆跟踪
智能跟车， 能够判断前车距离， 保持车距（超声波测距）




 

Decision 
障碍物躲避， 能够躲避前方障碍物  
基于Rule-Base的lane权重图处理
自动倒车入库， 能够识别车库的二维码标识， 且能够自动倒车入库
Traffic Signs Detection
信号灯 识别

指示牌 识别

识别红绿灯， 且能做出红灯停， 绿灯行的正确决策


Mechanical Sterring  电机控制

沿车道线行走，不得超出车道线范围

智能跟车， 能够判断前车距离， 保持车距


外壳制作

 参赛队需为车模制作外壳， 材料不限。 无外壳队伍不允许参加评比 （加分项，taobao定制）
