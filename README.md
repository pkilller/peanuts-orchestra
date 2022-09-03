# 花生桌面乐队

> 树莓派作平台，通过GPIO控制外设来实现一个虚拟“乐队”。

## 特征生成器 Generator.py
**说明:** 解析指定midi文件, 并生成供Player播放的数据.

## 播放器 Player.py
**说明:** 运行于Raspberrypi2中, 使用python的GPIO控制外部设备发声.

# 新增乐器
虽然目前仅支持了`步进电机`（模拟了弦乐器、键盘乐器），但代码架构上考虑了扩展新“乐器”的能力。 基于Abstract_MusicalInstrument基类实现关键方法即可。

(原计划是加入几类`打击乐乐器`表现鼓类的声部，但后来就忘了)

# 演示

# 现有问题
1. 步进电机音不准的问题：
   由于本身为机械结构，所以脉冲频率越高，丢帧越多，所以需要给予补偿值，补偿值跟频率间没有严格关系，与不同批次、品牌甚至每个电机都不同。需要单独对每个音符测试出补偿值。尝试多种驱动方式，没有明显改善。（演示视频中应该能听出，高音明显上不去）

# 设备
## Stepper 0.9'
**厂商:** 东莞信浓马达有限公司

**型号:** STH-42C1008

**参考:** https://item.taobao.com/item.htm?spm=a1z09.2.0.0.1f30a53fK9WY3k&id=549480248775&_u=2mo1ulj8d40

| 实际频率   | 目标频率    | 补偿值(c_val) |
| -------- |:-----------:| -----:|
| 124.6 |  130.81(C3)   | -0.09 |
| 247   |  261.63(C4)   | -0.1 |
| 470   |  523.25(C5)   | -0.11 |


