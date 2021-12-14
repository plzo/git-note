## generate template
---
### task template 410
```
templ -p . --type=task --file=F:\yang.xie\aidi\tasks\boxdetector_410\task.json
```
### task template 400
```
templ --algo=. --type=task --module=RegClassify --file=D:\yang.xie\aidi_projects\task.json
```

### train template 410
```
templ -p . --module=Detection --type=train --file=F:\yang.xie\aidi\tasks\ocr_detection_410\model\train.json
templ -p . --module=BoxDetector --type=train --file=F:\yang.xie\aidi\tasks\boxdetector_410\model\train.json
```

### train template 400
```
templ --algo=. --type=train --module=BoxDetector --file=F:\yang.xie\aidi\tasks\boxdetector_410\model\train.json

```
### test template 410
```
templ -p . --module=Detection --type=test --file=F:\yang.xie\aidi\tasks\ocr_detection_410\model\test.json
templ -p . --module=Classify --type=train --file=D:\yang.xie\aidi_projects\20210129-pcb-newlabel\test_pcb_origin\RegClassify_0\roi_cls\model\train.json
templ -p . --module=BoxDetector --type=test --file=F:\yang.xie\aidi\tasks\boxdetector_410\model\test.json
```

### test template 400
```
templ --algo=. --type=test --module=BoxDetector --file=F:\yang.xie\aidi\tasks\boxdetector_410\model\test.json

```

## train 410
```
train -p ./algo --auth=1099aaf7-cec3-11e9-ad13-525400162223 F:\yang.xie\aidi_tasks\boxdetector_410\task.json    #150
train -p ./algo --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\aidi_tasks\boxdetector_410\task.json    #151

infer -p ./algo --auth=1099aaf7-cec3-11e9-ad13-525400162223 F:\yang.xie\aidi_tasks\boxdetector_410\task.json    #150
infer -p ./algo --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\aidi_tasks\boxdetector_410\task.json    #151

train -p ./algo --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_tasks\shennan20201019\task.json    #151
train -p ./algo --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_tasks\shennan20201019_big2000\task.json 

train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_tasks\split_reg_cls\task.json
infer -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_tasks\split_reg_cls\task.json
templ -p . --module=RegClassify --type=train --file=D:\yang.xie\aidi_tasks\split_reg_cls\model\train.json

train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_tasks\classify_410\task.json

train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\project-20201022\base_project\RegClassify_0\task.json

train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0\task.json

```
## train 400
```
train --algo=. --auth=494c190d-feb6-11e8-ae1c-525400396520 --task=D:\yang.xie\aidi_projects\task_9000_rearrange_json\task.json
infer --algo=. --auth=494c190d-feb6-11e8-ae1c-525400396520 --task=D:\yang.xie\aidi_projects\task_9000_rearrange_json\task.json
```

## eval
```
eval F:\yang.xie\aidi\cd_newbase\210r_A4\Segment_0\task.json
```

## view 
```
view F:\yang.xie\data\luyan\label\1.aqlabel
view F:\yang.xie\data\luyan\label\1.aqlabel --idx=0
view -f json F:\yang.xie\aidi\label0725\label0725_test\Segment_0\label\1.aqlabel

view -f json D:/yang.xie/aidi_projects/project-20201022/base_project/RegClassify_0/test_result/10.aqlabel
```


train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\update-label0918\reg_cls_all\RegClassify_0\task.json
train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\update-label0918\reg_cls_double\RegClassify_0\task.json
train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\update-label0918\reg_cls_single\RegClassify_0\task.json
train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\update-label0918\reg_cls_all_2class\RegClassify_0\task.json
train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\update-label0918\reg_cls_double_2class\RegClassify_0\task.json

infer -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\update-label0918\reg_cls_all\RegClassify_0\task.json



# 430

templ -p . --module=Classify --type=train --file=D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin_iter04_cp\RegClassify_0\sub_projects\大焊盘-露镍\model\train2.json

infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\test_classify2\Classify_0\task_V1.json


train -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=  F:\yang.xie\projects\test_segment\Segment_0\task_V1.json

infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=  F:\yang.xie\projects\test_segment\Segment_0\task_V1.json


train -p /algo --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\adc-train-project\sub_projects\主体检测\task_V1.json



train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin_iter04_cp\RegClassify_0\sub_projects\cls_all_data_for_test\task_V1.json


train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin_iter04_cp\RegClassify_0\sub_projects\normal\task_aug.json

train -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\20210129-pcb-newlabel\20211014_small\sub_projects\normal\task_V1.json

train -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin_iter04_cp\RegClassify_0\sub_projects\大焊盘-露镍\task_V1.json

vrs.exe train D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin_iter04_cp\RegClassify_0\train_task.json new_aug(打开噪声) 1500 normal

cmake -B./build/vs-release -G "Visual Studio 15 2017" -T host=x64 -A x64
cmake --build ./build/vs-release --config Release --target all -j 42


train -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\adc-train-project\sub_projects\主体检测\task_V1.json


infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20211201-grade-exp-seg\test_classify\Classify_0\task_V1.json

infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20211201-grade-exp-seg\test_classify\Classify_0\task_V1.json

train -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20211115_chaosheng\adc_train_cmd\Classify_0\sub_projects\金面刮伤\task_V1.json

infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20211201-grade-exp-seg\test_classify\Classify_0\task_V1.json