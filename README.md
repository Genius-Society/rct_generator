# 随机对照试验生成器 WebUI
[![license](https://img.shields.io/github/license/Genius-Society/rct_generator.svg)](./LICENSE)
[![auto-sync](https://github.com/Genius-Society/rct_generator/actions/workflows/auto-sync.yml/badge.svg)](https://github.com/Genius-Society/rct_generator/actions/workflows/auto-sync.yml)
[![hf](https://img.shields.io/badge/huggingface-rct__generator-ffd21e.svg)](https://huggingface.co/spaces/Genius-Society/rct_generator)
[![ms](https://img.shields.io/badge/modelscope-rct__generator-624aff.svg)](https://www.modelscope.cn/studios/Genius-Society/rct_generator)

为进行随机对照试验(RCT)，首先确定试验的参与者数量、组别数量以及分配比例。选择可靠的随机数生成算法如Mersenne Twister 或线性同余生成器（LCG），编写程序生成每个参与者的随机分配结果。确保随机数生成器的公正性和可重复性，使用固定的随机种子，并进行测试验证确保分配结果符合预期并符合统计特性。最后，根据生成的随机数将参与者分配到相应的试验组别，并记录分配结果供后续分析使用。