# wechat-jump-jump



使用 python 玩微信跳一跳



### 参考项目

https://github.com/moneyDboat/wechat_jump_jump

 

### 实现

- 通过 adb 截取手机屏幕并上传到电脑

- 通过opencv 匹配小人，获取小人的位置点 b

- 获取图像canny边缘

- 将小人从canny 图像中删除

- 获取当前canny图像中最高的边缘点 a

- 下一次需要跳的位置点为 c，做过b水平线交过a垂直线于d，其中a d c 构成一个直角三角形，夹角为30度。

  现已知a、b两点，求出c点即可

  ![demo](./img/demo1.png)

- 计算c点与b点欧式距离

- 通过距离计算需按压时长

- 通过 adb 实现模拟点压



### 调优

因本人只有720分辨率的测试机，因此自带的参数可能只适配720分辨率

如使用1080 或1440 分辨率的手机需进行几个调优：

- 将小人的素材图片替换为对应分辨率下的截图（不知道720的能不能正确匹配小人）。

- 将小人的中心偏移量设置为对应分辨率下的值

- 为了得到下一个位置的最高点，因此会切割掉图片上部的分数等多余部分，切割的高度需要进行设置

- 在将小人从canny图片中删除时，需要计算小人的宽度，应替换为对应宽度

- 距离时间计算公式 time =  ( distance + b ) * w

  > 其中 w = 1440 / 分辨率大小
  >
  > b在设置好小人中心位置后，手动调节至合适值即可


### 效果

- 比起原项目只能打到1000分，改进后只要参数正确，能无限制的刷分
- 做了随机化操作，防止刷分被监测出来导致无法计入排行榜或分数归零

![demo](./img/demo.png)



### 最后

欢迎大家提出建议或者疑问，如果喜欢的话，请给我一颗星星哦～