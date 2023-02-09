1、prepare_data.py  清空数据 从origin获取数据 生成list
2、运行develop-label-tools-pcb，转换数据，生成新标签和数据
3、update_dataset_filter.py 同步新数据
4、fix_data_info_aqlabel.py 同步更新data_info.json
5、打开AIDI工程，选择训练集
6、update_task.py 更新task
7、update_db_train_set.py 同步其他AIDI项目训练集