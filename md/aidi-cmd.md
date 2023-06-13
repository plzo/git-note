## generate template
---
### task template 400
```
templ --algo=. --type=task --module=RegClassify --file=D:\yang.xie\aidi_projects\task.json
```
### train template 400
```
templ --algo=. --type=train --module=BoxDetector --file=F:\yang.xie\aidi\tasks\boxdetector_410\model\train.json

```
### test template 400
```
templ --algo=. --type=test --module=BoxDetector --file=F:\yang.xie\aidi\tasks\boxdetector_410\model\test.json

```
## train 400
```
train --algo=. --auth=494c190d-feb6-11e8-ae1c-525400396520 --task=D:\yang.xie\aidi_projects\task_9000_rearrange_json\task.json
infer --algo=. --auth=494c190d-feb6-11e8-ae1c-525400396520 --task=D:\yang.xie\aidi_projects\task_9000_rearrange_json\task.json
```
### task template 410
```
templ -p . --type=task --file=F:\yang.xie\aidi\tasks\boxdetector_410\task.json
```
### train template 410
```
templ -p . --module=Detection --type=train --file=F:\yang.xie\aidi\tasks\ocr_detection_410\model\train.json
templ -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Release --module=Classify --type=train --file=F:\yang.xie\projects\20220525_pcb\filter5000\Classify_0\new_train.json
```
### test template 410
```
templ -p . --module=BoxDetector --type=test --file=F:\yang.xie\aidi\tasks\boxdetector_410\model\test.json
```
## train 410
```
train -p ./algo --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\aidi_tasks\boxdetector_410\task.json
infer -p ./algo --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\aidi_tasks\boxdetector_410\task.json

```
## eval
```
eval F:\yang.xie\aidi\cd_newbase\210r_A4\Segment_0\task.json
```
## view 
```
view F:\yang.xie\data\luyan\label\1.aqimg
view F:\yang.xie\data\luyan\label\1.aqimg --idx=0
view -f json F:\yang.xie\data\luyan\label\1.aqlabel
```
# 430 segment eval
```
aidi_vision.exe eval F:\yang.xie\projects\20220112-cdsegment\chaosheng200_aidi\Segment_0\train_task.json --eval="recall(--granul=pixel)>0.33"
aidi_vision.exe eval F:\yang.xie\projects\20220112-cdsegment\chaosheng200_aidi\Segment_0\train_task.json --eval="precision(--granul=pixel)>0.33"
```
# make
```
cmake -B./build -G "Visual Studio 15 2017" -T host=x64 -A x64
cmake --build ./build --config Release --target all -j 42
```

git remote add origin2 git@git.aqrose.com:yang.xie/aidi_vision_v2_cls_seg.git

train -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\task.json

train -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Debug --auth=123 F:\yang.xie\projects\20220525_pcb\aidi_pcb_1c_small\Classify_0\task.json  //测试caffe

train -p F:\yang.xie\workspace\aidi_vision_v2_pvd\aidi_vision_v2\build\x64\bin\Debug --auth=123 F:\yang.xie\projects\20220610_CD\chaosheng200\2.0.AIDI_seg_cd200\Segment_0\tarin_task.json

train -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Release --auth=123 F:\yang.xie\projects\20220610_CD\0.test_small\task.json

train -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\HB0415-2W\Classify_0\task.json

train -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\fix_bugs\244\Segment_0\task.json

train -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20230510_pvd\5.pvd-696\Segment_0\task.json

train -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\HB0415-2W\Classify_0\task.json

train -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\test_pcb_seg\Segment_0\task.json

train -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\1.test_440_classify_1c\Classify_0\task.json

templ -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Debug --module=Classify --type=train --file=F:\yang.xie\projects\20220525_pcb\1.test_440_classify_1c\Classify_0\task2.json




# 2.5d
```
python src/compute_light_directions.py images/chrome/chrome.txt output/lights.txt
python src/simple_photometric_stereo.py images/chrome/chrome.txt output/lights.txt output/calibrated_chrome_%s.png
python src/unknown_light_photometric_stereo.py images/chrome/chrome.txt output/uncalibrated_chrome_%s.png
python src/compute_depth_map.py images/chrome/chrome.txt output/calibrated_chrome_normal.png output/calibrated_chrome_%s.png
python src/compute_depth_map.py images/chrome/chrome.txt output/uncalibrated_chrome_normal.png output/uncalibrated_chrome_%s.png

python src/compute_light_directions.py images/ball/ball.txt output/lights.txt
python src/simple_photometric_stereo.py images/ball/ball.txt output/lights.txt output/calibrated_ball_%s.png
python src/unknown_light_photometric_stereo.py images/ball/ball.txt output/uncalibrated_ball_%s.png
python src/compute_depth_map.py images/ball/ball.txt output/calibrated_ball_normal.png output/calibrated_ball_%s.png
python src/compute_depth_map.py images/ball/ball.txt output/uncalibrated_ball_normal.png output/uncalibrated_ball_%s.png
```

# sdk

```
bazelisk build compdb

git clone git@git.aqrose.com:aidi/aidi-sdk.git

$ cd aidi-sdk

# 构建命令行工具
$ bazelisk build cli

# 执行所有测试用例
$ bazelisk test //test/...

# 构建文档
$ bazelisk build docs

# 在浏览器中预览文档
$ bazelisk run docs:server


```
