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
infer -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 D:\yang.xie\aidi_projects\update-label0918\reg_cls_all\RegClassify_0\task.json



# 430

%(AdditionalOptions) -Zm800

    gen_rectangle1(ROI_0,220,220,240,240)
    reduce_domain(NormalVectors,ROI_0,ImageReduced)
    get_region_points(ROI_0,Rows,Columns)
    get_grayval(NormalVectors,Rows,Columns,Grayval)


    gen_rectangle1(ROI_0,220,220,221,221)
get_region_points(ROI_0,Rows2,Columns2)
decompose3 (NormalVectors, Nx2, Ny2, Nz2)
get_grayval (Nx2, Rows2, Columns2, GvNx2)
get_grayval (Ny2, Rows2, Columns2, GvNy2)
get_grayval (Nz2, Rows2, Columns2, GvNz2)
GvN2 := [GvNx2,GvNy2,GvNz2]
create_matrix (3, |GvNx2|, [GvNx2,GvNy2,GvNz2], MatrixNtID2)
transpose_matrix (MatrixNtID2, MatrixNID2)

segment:
aidi_vision.exe eval F:\yang.xie\projects\20220112-cdsegment\chaosheng200_aidi\Segment_0\train_task.json --eval="recall(--granul=pixel)>0.33"
aidi_vision.exe eval F:\yang.xie\projects\20220112-cdsegment\chaosheng200_aidi\Segment_0\train_task.json --eval="precision(--granul=pixel)>0.33"

cmake -B./build/vs-release -G "Visual Studio 15 2017" -T host=x64 -A x64
cmake --build ./build/vs-release --config Release --target all -j 42

cmake -B./build -G "Visual Studio 15 2017" -T host=x64 -A x64

git remote add origin2 git@git.aqrose.com:yang.xie/aidi_vision_v2_cls_seg.git

templ -p . --module=Classify --type=train --file=F:\yang.xie\projects\STD_test_contrasive_classify\train.json

templ -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Release --module=Classify --type=train --file=F:\yang.xie\projects\20220525_pcb\filter5000\Classify_0\new_train.json

templ -p F:\yang.xie\workspace\aidi_vision_v2_cls_seg\build\x64\bin\Debug --module=TDSegment --type=task --file=F:\yang.xie\projects\20220505_3D\kptest_dinghan\task1.json

train -p F:\yang.xie\workspace\aidi_vision_v2_cls_seg\build\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220505_3D\kptest_dinghan\task.json

infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\test_classify2\Classify_0\task_V1.json

train -p ./algo --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn100_test\Classify_0\train_task.json

train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn100\Classify_0\train_task.json

infer -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn010\Classify_0\all_task.json

infer -p ./algo --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn100_test\Classify_0\all_task.json

infer -p D:\yang.xie\workspace\aidi_vision_v2_develop\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\aidi_pcb_2c_small\Classify_0\task.json


train -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\aidi_pcb_1c_small\Classify_0\task.json


infer -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\data\20221205_stable\AIDI_projects\base\Segment_0\task.json\task.json

train -p F:\yang.xie\workspace\aidi_vision_v2_cls_seg\build\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:/yang.xie/projects/20220505_3D/焊渣焊高/task.json

engine: CAFFE

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

train -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb500_small\v12.8_pcb600\Classify_0\task.json

infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb500_small\v12.8_pcb600\Classify_0\task.json


aidi_vision.exe infer -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn000\Classify_0\all_task.json
aidi_vision.exe train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn100\Classify_0\train_task.json

infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn100_test\Classify_0\task1.json

infer -p D:\yang.xie\workspace\aidi_vision_v2_roi\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn100_test\Classify_0\task2.json

infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn000\Classify_0\all_task.json


infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn100_test\Classify_0\task.json

infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_dsn111\Classify_0\all_task.json


train -p D:\yang.xie\workspace\aidi_vision_v2_2.3.1_seg\aidi_vision_v2\build\vs-release\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220610_CD\chaosheng200\2.1.AIDI_seg_cd200_v2\Segment_0\train_task.json

infer -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\aidi_pcb_2c_small\Classify_0\task.json

infer -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\aidi_pcb_2c_small\Classify_0\task.json




train -p D:\yang.xie\workspace\aidi_vision_v2_2.3.1_seg\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220610_CD\0.test_small\all_task.json

aidi_vision.exe train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_att_dsn0111\Classify_0\train_task.json

train -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\pcb5000_exp_8\roi_siam_att_dsn0111\Classify_0\task.json


infer -p D:\yang.xie\workspace\aidi_vision_v2_develop\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\aidi_pcb_2c_small\Classify_0\task.json



train -p D:\yang.xie\workspace\aidi_vision_v2_2.3.1_seg\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220610_CD\0.test_small\all_task.json

train -p D:\yang.xie\workspace\aidi_vision_v2_2.3.1_seg\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220610_CD\chaosheng200\2.0.AIDI_seg_cd200\Segment_0\train_task.json


templ -p D:\yang.xie\workspace\aidi_vision_v2_2.3.1_seg\aidi_vision_v2\build\vs-release\x64\bin\Debug --module=Segment --type=test --file=F:\yang.xie\projects\20220610_CD\chaosheng200\2.0.AIDI_seg_cd200\Segment_0\model\test.json


infer -p D:\yang.xie\workspace\aidi_vision_v2_2.3.1_seg\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220610_CD\chaosheng1000\5.1.AIDI_seg_cd1000\Segment_0\test_task.json


infer -p D:\yang.xie\workspace\aidi_vision_v2_2.3.1_seg\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220610_CD\chaosheng200\2.0.AIDI_seg_cd200\Segment_0\test_task.json


infer -p D:\yang.xie\workspace\aidi_vision_v2_develop\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\TMP\081110\Classify_0\task.json


train -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\aidi_pcb_3c_small\Classify_0\task.json


train -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\aidi_pcb_2c_small\Classify_0\task.json
infer -p D:\yang.xie\workspace\aidi_vision_v2_develop\aidi_vision_v2\build\vs-release\x64\bin\Debug --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\TMP\081110\Classify_0\task.json

templ -p D:\yang.xie\workspace\aidi_vision_v2\build\vs-release\x64\bin\Debug --module=Classify --type=train --file=F:\yang.xie\projects\20220525_pcb\aidi_pcb_3c_small\Classify_0\new_train.json

aidi_vision.exe train -p . --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\projects\20220525_pcb\aidi_pcb_2c_small\Classify_0\task.json



infer -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\data\20221205_stable\AIDI_projects\base\Segment_0\task.json

infer -p F:\yang.xie\workspace\aidi_vision_v2\build\x64\bin\Release --auth=494c190d-feb6-11e8-ae1c-525400396520 F:\yang.xie\data\20221205_stable\AIDI_projects\03-101-V2\Segment_0\task.json