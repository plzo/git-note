<!-- TOC -->autoauto- [1. Boxdetector](#1-boxdetector)auto- [2. Cmake](#2-cmake)auto    - [2.1. cmake下载安装](#21-cmake下载安装)auto    - [2.2. cmake编程](#22-cmake编程)auto        - [2.2.1. 一般](#221-一般)auto        - [2.2.2. 添加cuda](#222-添加cuda)auto        - [2.2.3. NO_DEFAULT_PATH](#223-no_default_path)auto    - [2.3. 运行](#23-运行)auto- [3. conda](#3-conda)auto    - [3.1. conda安装](#31-conda安装)auto    - [3.2. linux命令](#32-linux命令)auto    - [3.3. wiondows命令](#33-wiondows命令)auto    - [3.4. python包安装](#34-python包安装)auto        - [3.4.1. conda安装](#341-conda安装)auto        - [3.4.2. Anaconda.org安装](#342-anacondaorg安装)auto        - [3.4.3. pip安装](#343-pip安装)auto    - [3.5. 切换python包下载源](#35-切换python包下载源)auto        - [3.5.1. windows下切换](#351-windows下切换)auto            - [3.5.1.1. 切换pip源](#3511-切换pip源)auto            - [3.5.1.2. 切换conda源](#3512-切换conda源)auto        - [3.5.2. linux下切换](#352-linux下切换)auto            - [3.5.2.1. 、切换pip源](#3521-切换pip源)auto            - [3.5.2.2. 切换conda源](#3522-切换conda源)auto- [4. linux命令](#4-linux命令)auto    - [4.1. 常用命令](#41-常用命令)auto    - [4.2. 切换用户](#42-切换用户)auto    - [4.3. docker](#43-docker)auto        - [4.3.1. linux](#431-linux)auto        - [4.3.2. Windows](#432-windows)auto    - [4.4. tmux命令](#44-tmux命令)auto    - [4.5. 磁盘空间](#45-磁盘空间)auto    - [4.6. 创建用户](#46-创建用户)auto    - [4.7. 权限管理](#47-权限管理)auto    - [4.8. ssh安装](#48-ssh安装)auto    - [4.9. 修改环境变量](#49-修改环境变量)auto    - [deb文件安装](#deb文件安装)auto    - [4.10. openssl下载安装](#410-openssl下载安装)auto    - [4.11. 重装cuda](#411-重装cuda)auto- [5. gcc命令](#5-gcc命令)auto- [6. Git](#6-git)auto    - [6.1. git添加密钥](#61-git添加密钥)auto    - [6.2. git命令](#62-git命令)auto        - [6.2.1. 常用](#621-常用)auto        - [6.2.2. 重命名远程分支](#622-重命名远程分支)auto        - [6.2.3. Create a new repository](#623-create-a-new-repository)auto        - [6.2.4. Existing folder(main)](#624-existing-foldermain)auto        - [6.2.5. Existing Git repository](#625-existing-git-repository)auto- [7. python编程](#7-python编程)auto    - [7.1. tensorflow](#71-tensorflow)auto    - [7.2. 文本读取](#72-文本读取)auto        - [7.2.1. 普通文本](#721-普通文本)auto            - [7.2.1.1. 直接open](#7211-直接open)auto            - [7.2.1.2. readline()](#7212-readline)auto            - [7.2.1.3. readlines()](#7213-readlines)auto        - [7.2.2. json读写](#722-json读写)auto    - [7.3. scripts](#73-scripts)auto        - [7.3.1. 散点图](#731-散点图)auto    - [7.4. 密度曲线图](#74-密度曲线图)auto        - [7.4.1. 文件移动](#741-文件移动)auto- [8. C++编程](#8-c编程)auto    - [8.1. OpenCV](#81-opencv)auto        - [8.1.1. 关于rows，cols](#811-关于rowscols)auto        - [8.1.2. 关于findContours](#812-关于findcontours)auto        - [8.1.3. 类型](#813-类型)auto    - [8.2. 文本读写](#82-文本读写)auto        - [8.2.1. 读文件](#821-读文件)auto        - [8.2.2. 写文件](#822-写文件)auto- [9. sublime安装](#9-sublime安装)auto    - [9.1. 步骤](#91-步骤)auto    - [9.2. 证书](#92-证书)auto- [10. Caffe问题解决](#10-caffe问题解决)auto- [MXnet安装](#mxnet安装)auto- [VScode](#vscode)auto    - [修改颜色](#修改颜色)autoauto<!-- /TOC -->
---
# 1. Boxdetector
```
C:\Program Files\Caffe\bin>encrypt_model.exe -model D:\assets\crpn_resnet18_luyan_iter_600.caffemodel -path D:\assets\ -proto D:\assets\test_prototxt\resnet18_change_test_split.prototxt aqrose

python /home/xieyang/caffe/tools/extra/plot_training_log.py 6 lossluyan88.png iter-lossluyan88.log

 D:\gitclone\BoxDetector_CPP\build\demo>demo.exe ../100.png ../100.pcd

../example.png ../example.pcd

sudo build/tools/caffe train -solver examples/myfile/solver.prototxt
./build/tools/caffe train --solver=examples/mnist/lenet_solver.prototxt

/home/xieyang/caffe//build/tools/caffe train -solver resnet18_solver_tianma.prototxt 2>&1 |tee out.log

python /home/xieyang/caffe/tools/extra/plot_training_log.py 6 testloss.png out.log

```
---
# 2. Cmake
## 2.1. cmake下载安装
- 下载
https://cmake.org/files/v3.1/下载
- cmake-3.1.0.tar.gz
```
tar -xzvf cmake-3.1.0.tar.gz
./configure
make
sudo make install
sudo update-alternatives --install /usr/bin/cmake /usr/local/bin/cmake 1 --force
cmake --version   #查看版本号
```
## 2.2. cmake编程
### 2.2.1. 一般
```
# OpenCV 3
find_package(OpenCV 3 REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
link_directories(${OpenCV_LIBRARY_DIRS})
add_definitions(${OpenCV_DEFINITIONS})

# OpenCV 3
set(OpenCV_DIRS "D:/aidi_libs/420-vs2017/opencv3.3.4.11")
if (CMAKE_BUILD_TYPE STREQUAL Debug)
    set(OpenCV_LIBRARY_DIRS ${OpenCV_DIRS}/build/Debug/x64)
	set(OpenCV_LIBS "opencv_world3411d.lib")
else()
    set(OpenCV_LIBRARY_DIRS ${OpenCV_DIRS}/build/Release/x64)
	set(OpenCV_LIBS "opencv_world3411.lib")
endif()
include_directories(${OpenCV_DIRS}/include)
link_directories(${OpenCV_LIBRARY_DIRS})

# requires Caffe
find_package(Caffe REQUIRED)
if(Caffe_FOUND)
    get_property(Caffe_INCLUDE_DIRS TARGET caffe PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
    include_directories(${Caffe_INCLUDE_DIRS})
endif()

# Eigen
find_package(Eigen3 REQUIRED PATHS ${CMAKE_CURRENT_LIST_DIR}/ThirdParty NO_DEFAULT_PATH)
if (${MSVC_VERSION} GREATER_EQUAL 1915)
    add_definitions(-D_ENABLE_EXTENDED_ALIGNED_STORAGE)
endif()
include_directories(${EIGEN3_INCLUDE_DIR})

# openssl
add_library(crypto STATIC IMPORTED)
set_target_properties(crypto PROPERTIES IMPORTED_LOCATION "${CMAKE_CURRENT_LIST_DIR}/ThirdParty/openssl/lib/libcrypto.lib")

# rapidjson
find_package(RapidJSON REQUIRED PATHS "${CMAKE_CURRENT_LIST_DIR}/ThirdParty/" NO_DEFAULT_PATH)
include_directories(${RapidJSON_INCLUDE_DIR})

file(GLOB_RECURSE SOURCE_FILES
    "Application/src/*.cpp"
    "Utils/Ransac/src/*.cpp"
    main.cpp
)

set(BOXDETECTOR_VERSION ${BOXDETECTOR_MAJOR_VERSION}.${BOXDETECTOR_MINOR_VERSION}.${BOXDETECTOR_PATCH_VERSION})
include_directories(Packing/include)
target_link_libraries(main ${OpenCV_LIBS} ${Caffe_LIBRARIES} ${GTEST_LIBRARY} crypto clipperlib)

```
### 2.2.2. 添加cuda
```
# packages
find_package(CUDA)
include_directories(${CUDA_INCLUDE_DIRS})

# nvcc flags
set(CUDA_NVCC_FLAGS -O3;-G;-g)

# build the library
file(GLOB_RECURSE SOURCE_FILES
    "src/*.cpp"
    "src/*.cu"
)
cuda_add_library(${PROJECT_NAME} STATIC ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS} kinematics camera geometry clipperlib)

cuda_add_executable(main
    ${SOURCE_FILES}
)
target_link_libraries(main ${OpenCV_LIBS} ${Caffe_LIBRARIES} ${GTEST_LIBRARY} crypto clipperlib)
```
### 2.2.3. NO_DEFAULT_PATH
- 生效需删除build文件或cache
```
find_package( Caffe REQUIRED PATHS "C:\\Program Files\\Caffe" NO_DEFAULT_PATH )
find_package( Caffe REQUIRED PATHS "C:\\Program Files\\Caffe_ori\\share\\Caffe" NO_DEFAULT_PATH )
```
链接第三方库
（1）链接静态库
```
set(PROTOBUF_LIBS "libprotobuf.lib")
include_directories(${PROTOBUF_PATH}/include)
link_directories(${PROTOBUF_PATH}/build/${CMAKE_BUILD_TYPE}/x64)

add_executable(main ${SOURCE_FILES})
target_link_libraries(main ${OpenCV_LIBS} ${AIDIVISION_LIBS} ${PROTOBUF_LIBS} AqimgLabel)
```
（2）如果是动态库，则需要保证链接库的.dll文件和.exe在一个目录，或设置环境变量（将.dll放入环境变量路径）。
find_package设置路径的一种方法：
list(APPEND CMAKE_PREFIX_PATH ${PROTOBUF_PATH})
find_package(Protobuf CONFIG REQUIRED)
include_directories(STATUS ${Protobuf_INCLUDE_DIR})

add_executable(main ${SOURCE_FILES})
target_link_libraries(main ${OpenCV_LIBS} ${AIDIVISION_LIBS} AqimgLabel protobuf::libprotobuf)


```

## 2.3. 运行
```
cmake -G"NMake Makefiles" -DCMAKE_BUILD_TYPE=Release ..
```
---
# 3. conda
## 3.1. conda安装
- windows安装包安装，linux下载安装包，bash安装
```
bash Anaconda3-5.2.0-Linux-x86_64.sh
```
- 最后一步不能选择了默认的no 选择yes添加path。
- 删除conda直接remove。
```
rm -rf ~/anaconda3
```
## 3.2. linux命令
```
conda --version
conda update --help
conda update conda 
conda create -n py3 python=3 tensorflow
conda create -n py31 --clone py3
source activate py3
source deactivate
conda remove -n py3 --all
conda install tensorflow-gpu
conda info -e
```
## 3.3. wiondows命令
```
conda env list
conda create -n py3 python=2.7
conda env remove -n py3
activate py3
conda install tensorflow
conda install --name py3 tensorflow  (指定安装到py3环境)
conda search numpy   (含“numpy”)
conda search --full --name numpy  （全字匹配）

conda env create -f conda_environment.yml
conda install --yes --file requirements.txt
pip install --index-url https://pypi.douban.com/simple filterpy
pip install imagecodecs -i https://pypi.tuna.tsinghua.edu.cn/simple/   关闭vpn

```

## 3.4. python包安装
### 3.4.1. conda安装
- 全部可用安装包查询（可用conda install安装）：
https://docs.anaconda.com/anaconda/packages/pkg-docs
### 3.4.2. Anaconda.org安装
- 如果不可用conda安装，从Anaconda.org安装：
https://anaconda.org/saku16/dashboard
```
anaconda search -t conda numpy
conda show xxx/xxx
conda install --channel https://conda.anaconda.org/ukoethe numpy
```
### 3.4.3. pip安装
- 对于那些无法通过conda安装或者从Anaconda.org获得的包，我们通常可以用pip（“pip install packages”的简称）来安装包。
- Tips： pip只是一个包管理器，所以它不能为你管理环境。pip甚至不能升级python，因为它不像conda一样把python当做包来处理。但是它可以安 装一些conda安装不了的包，和vice versa（此处不会翻译）。pip和conda都集成在Anaconda或miniconda里边。

## 3.5. 切换python包下载源
### 3.5.1. windows下切换
#### 3.5.1.1. 切换pip源

-  在windows文件管理器中,输入 %APPDATA%
-  会定位到一个新的目录下，在该目录下新建pip文件夹，然后到pip文件夹里面去新建个pip.ini文件
-  在新建的pip.ini文件中输入以下内容，搞定文件路径："C:\Users\Administrator\AppData\Roaming\pip\pip.ini
```
[global]
timeout = 6000
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```
#### 3.5.1.2. 切换conda源

- 打开cmd
```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```
### 3.5.2. linux下切换
#### 3.5.2.1. 、切换pip源
修改~/.pip/pip.conf，修改index-url至相应源
```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```
#### 3.5.2.2. 切换conda源
- 方法一
```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```
- 方法二
cd /etc/apt/
sudo cp sources.list sources.list.bak 
chmod 777 sources.list
sudo gedit sources.list
```
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-proposed main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-proposed main restricted universe multiverse
```

---
# 4. linux命令
## 4.1. 常用命令
```
sudo ln -s /home/xieyang/anaconda3/bin/python3  /usr/lib/python3.7m  #快捷方式
find ./ -name libc.so*
sudo apt-get update  #更新源 
sudo apt-get upgrade  #更新软件
tar -xzvf 
rm -rf python2.7
mkdir test
touch test.py
ipcs -m #查看共享内存
top
free  #显卡信息
nvidia-smi
nvidia-smi -L #GPU信息
sudo apt-get remove vim  #卸载vim
wget -qO- https://raw.github.com/ma6174/vim/master/setup.sh | sh -x  #vim安装
make -j8 && make pycaffe
sudo ln -s /root/anaconda3/bin/python3  /usr/lib/python3.7m  #建立软连接（快捷方式）
sudo ln -s libboost_python-py35.so.1.58.0 libboost_python3.so


cat /proc/cpuinfo | grep name | sort | uniq #查看cpu型号
cat /proc/cpuinfo | grep "physical id"  #物理cpu数
cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l
cat /proc/cpuinfo | grep "core id" | sort | uniq | wc -l
cat /proc/cpuinfo | grep "processor" | sort | uniq | wc -l


```
## 确定python的site-packages路径
```
python
from  distutils.sysconfig  import  get_python_lib
print  get_python_lib()
```
## 4.2. 切换用户
```
sudo -s #切换到root，环境变量不变
su - root  #配合sudo -s 切换环境变量
sudo - root  #直接切换到root和环境
su xieyang
```
## 4.3. docker
### 4.3.1. linux
- 参数-t让Docker分配一个伪终端并绑定在容器的标准输入上，-i让容器的标准输入保持打开。
```
docker iamges
docker pull bvlc/caffe:gpu
sudo nvidia-docker run -it -v bvlc/caffe --name ts ba28bcb1294c /bin/bash
sudo docker run --name caffe -it wuyupei/caffe:latest bash
```
```
docker exec -it caffe bash  #容器中关闭docker
docker start caffe  #启动容器
docker stop caffe  #关闭容器
docker rm caffe  #删除容器
docker ps -a  #列出所有容器
```
- 在進入容器後，就可以使用各種 caffe 的指令了。另外，caffe 的各個工具已經被加到 PATH 中，可以執行：
```
caffe --version
```
### 4.3.2. Windows
在系统右下角托盘Docker图标内右键菜单选择Settings，打开配置窗口后左侧导航菜单选择Daemon。在Registry mirrors一栏中填写地址 https://docker.mirrors.ustc.edu.cn/ ，之后点击Apply保存后Docker就会重启并应用配置的镜像地址了。

## 4.4. tmux命令
```
tmux new -s s1  #新建一个会话
tmux ls  #列出所有会话
tmux kill-session -t s1  #关闭会话s1
tmux kill-server　　#关闭所有会话
tmux a -t mysession　　#连接指定会话
```

## 4.5. 磁盘空间
```
du -h --max-depth=1
df -hl 查看磁盘剩余空间
df -h 查看每个根路径的分区大小
du -sh [目录名] 返回该目录的大小
du -sm [文件夹] 返回该文件夹总M数
du -h [目录名] 查看指定文件夹下的所有文件大小（包含子文件夹）
```
## 4.6. 创建用户
```
useradd -m yang
passwd yang
userdel yang
```

## 4.7. 权限管理
```
chgrp root caffe
chgrp -R root caffe  #递归修改caffe用户组为root
chown xieyang caffe
chown -R xieyang caffe  #递归修改所有者
chgrp 777 caffe
chgrp -R 777 caffe  #递归修改权限
```

设置python路径，$(pwd)是终端所在目录
```
export PYTHONPATH=$(pwd)/python:$PYTHONPATH
```

## 4.8. ssh安装
```
ssh localhost ssh  #检查是否安装
sudo apt-get install openssh-server
sudo /etc/init.d/ssh start  #启动
ps -e|grep ssh  #检查是否启动
```

## 4.9. 修改环境变量

- 方法一：用户主目录下的.profile或.bashrc文件（推荐） 

1、登录到你的用户（非root），在终端输入： 
```
$ sudo gedit ~/.profile(or .bashrc) 
```
2、可以在此文件末尾加入PATH的设置如下： 
```
export PATH=”$PATH:your path1:your path2 ...”
```
3、保存文件，注销再登录，变量生效。 该方式添加的变量只对当前用户有效。 

- 方法二：系统目录下的profile文件（谨慎）
1、在系统的etc目录下，有一个profile文件，编辑该文件： 
```
$ sudo gedit /etc/profile 
```
2、在最后加入PATH的设置如下： 
```
export PATH=”$PATH:your path1:your path2 ...” 
```
3、该文件编辑保存后，重启系统，变量生效。 该方式添加的变量对所有的用户都有效。

- 方法三：系统目录下的 environment 文件（谨慎）

1、在系统的etc目录下，有一个environment文件，编辑该文件： 
```
$ sudo gedit /etc/environment 
```
2、找到以下的 PATH 变量： 
```
PATH="<......>" 
```
3、修改该 PATH 变量，在其中加入自己的path即可，例如： 
```
PATH="<......>:your path1:your path2 …"
```
4、各个path之间用冒号分割。该文件也是重启生效，影响所有用户。 注意这里不是添加export PATH=… 。 

- 方法四：直接在终端下输入 
这种方式变量立即生效，但用户注销或系统重启后设置变成无效，适合临时变量的设置。
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/xieyang/anaconda3/lib
```

## deb文件安装
https://ubuntu.pkgs.org/16.04/ubuntu-universe-amd64/cableswig_0.1.0+git20150808-2_amd64.deb.html
```
sudo dpkg -i linuxidc.deb
```

## 4.10. openssl下载安装
```
git clone https://github.com/openssl/openssl.git
cd openssl
./config
make
sudo make install
# Open file /etc/ld.so.conf, add a new line: "/usr/local/lib" at EOF
sudo ldconfig
```

## 4.11. 重装cuda
- 查看版本
```
cat /usr/local/cuda/version.txt
```
- 卸载cuda
```
sudo /usr/local/cuda-9.2/bin/uninstall_cuda_9.2.pl
```
- 卸载驱动
```
sudo /usr/bin/nvidia-uninstall
```
- 卸载干净
```
sudo apt-get remove --purge nvidia-*
sudo apt-get remove --purge xserver-xorg-video-nouveau 
sudo apt-get install ubuntu-desktop
sudo mv /etc/X11/xorg.conf /etc/X11/xorg.conf.bak
```

---
# 5. gcc命令
```
gcc test.c -o test  #预处理、汇编、编译并链接形成可执行文件test
gcc -E test.c -o test.i  #将test.c预处理输出test.i文件
gcc -S test.i  #将预处理输出文件test.i汇编成test.s文件
gcc -c test.s  #将汇编输出文件test.s编译输出test.o文件
```
---
# 6. Git
## 6.1. git添加密钥
- 打开git bash或cmd
```
cd ~/.ssh/
ssh-keygen -t rsa -C "yang.xie@aqrose.com" #或
ssh-keygen -t rsa -C "473222093@qq.com"  #生成密钥文件
```
- 回车，回车
- 打开github： https://github.com/settings/keys   添加C:\Users\Yang\.ssh\id_rsa.pub中的内容
- 打开cmd 输入： ssh -T git@github.com
- 设置 
```
git config --global user.name “plzo”
git config --global user.email "473222093@qq.com"

git config --global user.email "yang.xie@aqrose.com"
git config --global user.name “xieyang”

```
```
git remote rm origin
git remote add origin git@git.aqrose.com:aqrose_vision/aidi_vision_v2.git
git remote add origin2 git@git.aqrose.com:yang.xie/aidi_vision_v2.git
git remote -v

git reset -- . #取消git add .
git restore staged a.cpp
git restore a.cpp  #撤回a.cpp的更改，不可逆
git checkout -b new_branch #复制当前分支

```

## 6.2. git命令
### 6.2.1. 常用
```
git add .
git commit -m "Initial commit"
git push origin master

git push -u origin master #加-u之后，以后push只需要git push
git push -u origin master -f   #强制push

git pull origin master  #拉下来并合并merge
git pull origin master --allow-unrelated-histories

git branch xieyang
git push -u origin xieyang

git branch  #查看本地分支
git branch -r  #查看远程分支
git branch -a  #查看所有分支
git checkout master  #切换本地分支

git status
git log --pretty=oneline
git reflog
git reset --hard 23e0f

git rm 文件名字
git rm -rf 文件夹名字

git fetch origin master
git checkout packing
git merge origin/master

git checkout -b 410-dev origin/410-dev  #拉取新分支

```
```
Git fetch origin master
git log -p master..origin/master
git merge origin/master


Git fetch origin master  #从远程的origin的master主分支下载最新的版本到origin/master分支上
git push origin master #将本地的origin/master分支推送到远程origin库的master分支

git fetch origin master:tmp
git diff tmp
git merge tmp

```
### 6.2.2. 重命名远程分支
```
git branch -b mix git@git.aqrose.com:Group3DV/BoxDetector_tmp.git  #先连接远程仓库
git push origin --delete mix  #删除远程分支
git branch -m mix new_mix  #复制本地分支
git push origin new_mix  
git branch -d mix  #删除本地分支

git clean -f # 删除 untracked files
git clean -fd # 连 untracked 的目录也一起删掉
git clean -xfd # 连 gitignore 的untrack 文件/目录也一起删掉 （慎用，一般这个是用来删掉编译出来的 .o之类的文件用的）

git clean -nxfd
git clean -nf
git clean -nfd # 在用上述 git clean 前，强烈建议加上 -n 参数来先看看会删掉哪些文件，防止重要文件被误删
```
### 6.2.3. Create a new repository
```
git clone git@git.aqrose.com:yang.xie/example2.git
cd example2
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master
```
### 6.2.4. Existing folder(main)
```
cd existing_folder
git init
git remote add origin git@git.aqrose.com:yang.xie/example2.git
git add .
git commit -m "Initial commit"
git push -u origin master #加-u之后，以后push只需要git push
```
### 6.2.5. Existing Git repository
```
cd existing_repo
git remote rename origin old-origin
git remote add origin git@git.aqrose.com:yang.xie/example2.git
git push -u origin --all
git push -u origin --tags

token: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
git config --global http.proxy "localhost:7890"
git config --global https.proxy "localhost:7890"
```
---
# 7. python编程
## 7.1. tensorflow
```
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  #去掉警告
os.environ["CUDA_VISIBLE_DEVICES"] = '0'  #设置为第一块显卡
config = tf.ConfigProto()  
config.gpu_options.per_process_gpu_memory_fraction = 0.3  #最多用30显存  
config.gpu_options.allow_growth = True    #按需分配显存
```
- intra_op_parallelism_threads，用过来设定每个运算（即每个计算图里的节点）最多可以使用多少个线程，默认是2，见tensorflow/tensorflow
```
with tf.Session(config=tf.ConfigProto(device_count={"GPU":2},inter_op_parallelism_threads=1,intra_op_parallelism_threads=1)) as sess:
```

## 7.2. 文本读取
### 7.2.1. 普通文本
#### 7.2.1.1. 直接open
```
lines=[line for line in open(datalst,'r')]
for line in lines:
    data=line.strip().split()

fp = open(outputpath,'w')
fp.write(' '.join(data))
fp.write('\n')
```
#### 7.2.1.2. readline()
从字面意思可以看出，该方法每次读出一行内容，所以，读取时占用内存小，比较适合大文件，该方法返回一个字符串对象。
```
f = open("a.txt")
line = f.readline()
print(type(line))
while line:
    print line,
    line = f.readline()
f.close()
```
#### 7.2.1.3. readlines()
readlines()方法读取整个文件所有行，保存在一个列表(list)变量中，每行作为一个元素，但读取大文件会比较占内存。
```
f = open("a.txt")
lines = f.readlines()
print(type(lines))
for line in lines:
    print line
f.close()
```
### 7.2.2. json读写
- 先用普通的读取方法读从json中读出字符串，然后用loads（）将字符串变换成字典。
- dumps()：将python中的 字典 转换为 字符串
```
import json

test_dict = {'bigberg': [7600, {1: [['iPhone', 6300], ['Bike', 800], ['shirt', 300]]}]}
print(test_dict)
print(type(test_dict))

json_str = json.dumps(test_dict)  #dumps 将字典转换成字符串
print(json_str)
print(type(json_str))
```
- loads: 将 字符串 转换为 字典
```
new_dict = json.loads(json_str)  #loads 将字符串转换成字典
print(new_dict)
print(type(new_dict))
```
- dump: 将数据写入json文件中
```
with open("../config/record.json","w") as f:
json.dump(new_dict,f)
print("加载入文件完成...")
```
- load:把文件打开，并把字符串变换为数据类型
```
with open("../config/record.json",'r') as load_f:
load_dict = json.load(load_f)
print(load_dict)
```
## 7.3. scripts
### 7.3.1. 散点图
```
import matplotlib.pyplot as plt

plt.xlabel('x-value')
plt.ylabel('y-label')
plt.legend()
plt.scatter(x_true, y_true, s=20, c="#ff1212", marker='o')
plt.scatter(x_false, y_false, s=20, c="b", marker='o')
plt.savefig('./res.png')
```
## 7.4. 密度曲线图
```
import plotly.figure_factory as ff

y_true=[]
y_false=[]
for d in total_data_true:
    y_true.append(float(d))
for d in total_data_false:
    y_false.append(float(d))

# 9. Group data together
hist_data = [y_true, y_false]
group_labels = ['true proposals', 'false proposals']
colors = ['#333F44', '#37AA9C']

fig = ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)
# 10. Add title
fig.update_layout(title_text='proposals scores')
fig.show()
```
### 7.4.1. 文件移动
```
import os,shutil
shutil.copy(ori_filepath,filepath)  #文件复制移动
shutil.move(ori_filepath,filepath)  #文件移动
```

---
# 8. C++编程
## 8.1. OpenCV

### 8.1.1. 关于rows，cols
```
float * mat2float(cv::Mat image)
{
    float *image_float = new float[image.rows * image.cols];
    int index = 0;
    for (int i = 0; i < image.rows; ++i)
    {
        for (int j = 0; j < image.cols; ++j)
        {
            image_float[index++] = image.at<float>(i, j);
        }
    }
    return image_float;
}
/*
image.at<float>(i, j) == image.at<float>(cv::Point(j,i));
row == heigh == Point.y
col == width == Point.x
Mat::at(Point(x, y)) == Mat::at(y,x)
*/
image.at<uchar>(i, j);
image.at<cv::Vec3b>(i, j);
```
### 8.1.2. 关于findContours
```
cv::findContours(mask_roi_, mask_origin_contour, CV_RETR_TREE, CV_CHAIN_APPROX_NONE);
cv::findContours(mask_roi_, mask_origin_contour, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);

cv::findContours(rect_mat, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);
cv::Rect rect = cv::boundingRect(cv::Mat(contours[0]));
cv::Rect rect2 = cv::boundingRect(rect_mat);

cv::rectangle(dist_mat,rect,cv::Scalar(125),-1);//填充成125
```
```
std::string visual_str = result[i].ext_info["visual_img"];
std::vector<uchar> buf;
buf.assign(visual_str.begin(), visual_str.end());
cv::Mat visual_mat = cv::imdecode(buf, -1);

std::vector<cv::Vec4i> hierarchy;
std::vector<std::vector<cv::Point>> contours;
in::MultiPolygon tmp_gmasks;
in::scale(m_->global_svc.mask, tmp_gmasks, float(visual_mat.cols), float(visual_mat.rows));
polygons_to_contours(tmp_gmasks, contours, hierarchy);
cv::drawContours(visual_mat, contours, -1, cv::Scalar(255), -1, cv::LINE_8, hierarchy);

cv::imencode(".png", visual_mat, buf);
visual_str.assign(buf.begin(), buf.end());
result[i].ext_info["visual_img"] = visual_str;
```

```
cv::Mat imageMask(std::vector<cv::Mat> camImages) {
    assert(camImages.size() > 0);
    cv::Mat image = camImages[0].clone();
    int quarter = image.cols / 4.0;
    int eighth = image.rows / 8.0;
    cv::Mat result, bgModel, fgModel;
    cv::Rect area(quarter, eighth, 3 * quarter, 7 * eighth);
    /* grabcut expects rgb images */
    //cv::cvtColor(image, image, CV_GRAY2BGR);
    cv::grabCut(image, result, area, bgModel, fgModel, 1, cv::GC_INIT_WITH_RECT);
    cv::compare(result, cv::GC_PR_FGD, result, cv::CMP_EQ);
    return result;
}
```
```
    Mat mat_8U;
    aqcv::normalize(mat, mat_8U, 1, 0, aqcv::kNormMinMax);
    mat_8U.convert_to(mat_8U, AQ_8U, 255.0);
```

```
    bool filter_noise(Mat src) {
        float max_value = -999, min_value = 999;
        for (int r = 0; r < src.rows; r++) {
            float *ptr = src.ptr<float>(r);
            for (int c = 0; c < src.cols; c++) {
                if (ptr[c] > max_value)
                    max_value = ptr[c];
                if (ptr[c] < min_value)
                    min_value = ptr[c];
            }
        }
        int offset = 0;
        if (min_value < 0) {
            offset = -int(255 * min_value);
        }
        int pixel_range = int(255 * max_value) + offset + 1;
        std::vector<std::vector<int>> pix_nums(pixel_range, std::vector<int>());
        for (int r = 0; r < src.rows; r++) {
            float *ptr = src.ptr<float>(r);
            for (int c = 0; c < src.cols; c++) {
                pix_nums[int(ptr[c] * 255) + offset].push_back(r * src.cols + c);
            }
        }
        int max_index = src.rows * src.cols - 1;
        int filter_num = 1000000, step = 1, count = 0, i = 0;
        while (i >= 0 && i < pixel_range) {
            for (int j = 0; j < pix_nums[i].size(); j++) {
                int index = pix_nums[i][j];
                src.at<float>(index / src.cols, index % src.cols) = (src.at<float>(index / src.cols, index % src.cols)\
                    + src.at<float>(std::max((index - 1), 0) / src.cols, std::max((index - 1), 0) % src.cols)\
                    + src.at<float>(std::min((index + 1), max_index) / src.cols, std::min((index + 1), max_index) % src.cols)\
                    + src.at<float>(std::min((index + src.cols - 1), max_index) / src.cols, std::min((index + src.cols - 1), max_index) % src.cols)\
                    + src.at<float>(std::min((index + src.cols + 1), max_index) / src.cols, std::min((index + src.cols + 1), max_index) % src.cols)\
                    + src.at<float>(std::min((index + src.cols), max_index) / src.cols, std::min((index + src.cols), max_index) % src.cols)\
                    + src.at<float>(std::max((index - src.cols - 1), 0) / src.cols, std::max((index - src.cols - 1), 0) % src.cols)\
                    + src.at<float>(std::max((index - src.cols + 1), 0) / src.cols, std::max((index - src.cols + 1), 0) % src.cols)\
                    + src.at<float>(std::max((index - src.cols), 0) / src.cols, std::max((index - src.cols), 0) % src.cols)) / 9;
                count++;
                if (count > filter_num) {
                    break;
                }
            }
            i += step;
            if (count > filter_num && step == 1) {
                i = pixel_range - 1;
                step = -1;
                count = 0;
            }
            if (count > filter_num) {
                break;
            }
        }
        return true;
    }
```

```

       if (1) {
            std::cout << "============== L_pseudo ==============" << std::endl;
            std::cout << L_pseudo << std::endl;

            std::cout << "============== B ==============" << std::endl;
            std::cout << B << std::endl;
            std::cout << "============== U_B ==============" << std::endl;
            std::cout << U_B << std::endl;
            std::cout << "============== V_B ==============" << std::endl;
            std::cout << V_B << std::endl;
            std::cout << "============== sigma_B ==============" << std::endl;
            std::cout << sigma_B << std::endl;

            std::cout << "============== A^-1 ==============" << std::endl;
            std::cout << A_inverse << std::endl;
            std::cout << "============== A^-1^T ==============" << std::endl;
            std::cout << A_inverse.transpose() << std::endl;
            std::cout << "============== A^-1^T * A^-1 ==============" << std::endl;
            std::cout << A_inverse.transpose() * A_inverse << std::endl;
        }

    void adaptiveCannyThresold(const aqcv::Mat &gray, aqcv::Vec2i &thresold)
    {
        //    cv::Mat image;
        //    cv::resize(gray,image, cv::Size(),0.5,0.5);
        Mat dx, dy;
        sobel(gray, dx, AQ_8UC1, 1, 0, 3);
        sobel(gray, dy, AQ_8UC1, 0, 1, 3);
        Mat dxy(dx.rows, dx.cols, AQ_8UC1);

        int max_val = 0;
        uchar *dxy_ptr;
        uchar *dx_ptr;
        uchar *dy_ptr;
        for (int y = 0; y < dx.rows; y++) {
            dxy_ptr = dxy.ptr<uchar>(y);
            dx_ptr = dx.ptr<uchar>(y);
            dy_ptr = dy.ptr<uchar>(y);
            for (int x = 0; x < dx.cols; x++) {
                dxy_ptr[x] = abs(dx_ptr[x]) + abs(dy_ptr[x]);
                if (max_val < dxy_ptr[x])
                    max_val = dxy_ptr[x];
            }
        }

        max_val += 1;
        std::vector<int> pix_nums(256, 0);
        for (int r = 0; r < dxy.rows; r++) {
            uchar *ptr = dxy.ptr<uchar>(r);
            for (int c = 0; c < dxy.cols; c++) {
                pix_nums[int(ptr[c])] += 1;
            }
        }
        int edge_persent = gray.cols * gray.rows * 0.5;
        int sum = 0;
        int mid_thresold = 0;
        for (int i = 0; i <= max_val; i++) {
            sum += pix_nums[i];
            if (sum > edge_persent) {
                mid_thresold = i;
                break;
            }
        }
        float low_thresold = mid_thresold * 0.7;
        if (low_thresold > 5)
        {
            thresold = Vec2i(low_thresold, mid_thresold * 1.3);
        }
        else {
            thresold = Vec2i(5, 15);
        }
    }


        Mat edge, edge_mask;
        Vec2i canny_thresold;
        adaptiveCannyThresold(bright, canny_thresold);
        aqcv::canny(bright, edge, canny_thresold[0], canny_thresold[1]);
        aqcv::canny(bright, edge, 128, 200);
        aqcv::threshold(edge, edge_mask, 1, 255, kThresholdBinary);
        aqcv::imwrite("D:\\yang.xie\\workspace\\aqcv_temporary\\test\\datas\\photometric\\output\\edge.png", edge);
        aqcv::imwrite("D:\\yang.xie\\workspace\\aqcv_temporary\\test\\datas\\photometric\\output\\edge_mask.png", edge_mask);


        Mat mask = aqcv::Mat::zeros(bright_segment.size(), AQ_8UC1);
        std::vector<std::vector<aqcv::Point>> bright_contours;
        aqcv::find_contours(bright_segment, bright_contours, kRetrievalExternal, kChainApproxNone);
        std::vector<aqcv::Vec4i> hierarchy;
        for (int i = 0; i < bright_contours.size(); i++) {
            aqcv::drawContours(mask, bright_contours, -1, aqcv::Scalar(255), -1, kLine8, hierarchy);
        }
        aqcv::imwrite("D:\\yang.xie\\workspace\\aqcv_temporary\\test\\datas\\photometric\\output\\mask.png", mask);
```
%(AdditionalOptions) -Zm800


### 8.1.3. 类型
```
cv::Mat img = cv::Mat::zeros(image.size(), CV_32FC1);
cv::Mat img = cv::Mat::zeros(image.rows, image.cols, CV_8UC1);
cv::Mat img = cv::Mat::zeros(h, w, CV_8UC1);
rotate_image.at<cv::Vec3b>(i, j) = cv::Vec3b(104, 117, 123)

```

## 8.2. 文本读写
### 8.2.1. 读文件
```
# 11. include <fstream>

std::string test_list = "E:\\data\\transformed_luyan_data.txt";
std::string line;
std::vector<std::string> image_list;
std::ifstream infile_list((test_list).c_str());
while (std::getline(infile_list, line))
{
    image_list.push_back(line);
}
```
### 8.2.2. 写文件
```
std::ofstream output_txt("output.txt");
output_txt.close();

std::ofstream output_txt("output.txt", std::ios::app); //写一行加在文件后面
output_txt << "this is one line in output file." <<std::endl;
output_txt.close();
```


---
# 9. sublime安装
## 9.1. 步骤
- 下载“Package Control” Package Manager
点击Tools 菜单下的Install Package Control 就可以了
- 打开cmd
```
pip install flake8
```
- 通过ctrl+shift+p ，输入 install Package，然后回车，安装SublimeLinter
- 安装 SublimeLinter-flake8
- 配置SublimeLinter-flake8 preference--package setting--sublimelinter把左边的配置全部拷贝到右边的配置里并把开头的default更改为user，然后把配置中 "mark_style": "outline",更改为："mark_style":“squiggly_underline”
- 代码补全anaconda安装
- 设置anaconda
preference-----package setting------- anaconda
```
{
"anaconda_linting": false,
"pep8": false
}
```
## 9.2. 证书
```
—– BEGIN LICENSE —– 
Die Socialisten GmbH 
10 User License 
EA7E-800613 
51311422 E45F49ED 3F0ADE0C E5B8A508 
2F4D9B65 64E1E244 EDA11F0E F9D06110 
B7B2E826 E6FDAA72 2C653693 5D80582F 
09DCFFB5 113A940C 5045C0CD 5F8332F8 
34356CC6 D96F6FDB 4DEC20EA 0A24D83A 
2C82C329 E3290B29 A16109A7 EC198EB9 
F28EBB17 9C07403F D44BA75A C23C6874 
EBF11238 5546C3DD 737DC616 445C2941 
—— END LICENSE ——
```

---
# 10. Caffe问题解决
Thanks,
I changed
CMAKE_CXX_FLAGS:STRING='-fPIC '
to
CMAKE_CXX_FLAGS:STRING=-fPIC
in CMakeCache.txt in gflags folder and it works.
at first I use installations instractions from here
http://caffe.berkeleyvision.org/install_apt.html
```
wget https://github.com/schuhschuh/gflags/archive/master.zip
unzip master.zip
cd gflags-master
mkdir build && cd build
export CXXFLAGS="-fPIC" && cmake .. && make VERBOSE=1
make && make install
```
```
git clone https://github.com/google/leveldb.git
cd leveldb/
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release .. && cmake --build .
sudo cp build/libleveldb.a /usr/local/lib/
sudo cp -r include/leveldb/ /usr/local/include/
```

aidi_vision编译
```
cmake -B./build/vs-release -G "Visual Studio 15 2017" -T host=x64 -A x64
cmake --build ./build/vs-release --config Release --target all -j 42
```

---
# MXnet安装
```
gedit ~/.bashrc
```
添加：
```
export GIT_TRACE_PACKET=1
export GIT_TRACE=1
export GIT_CURL_VERBOSE=1
```
```
git clone --recursive https://github.com/dmlc/mxnet.git
git checkout 998378a
cp /home/xieyang/RoITransformer_DOTA/fpn/operator_cxx/* /home/xieyang/mxnet/src/operator/contrib
cd /home/xieyang/mxnet/
make -j $(nproc) USE_OPENCV=1 USE_BLAS=openblas USE_CUDA=1 USE_CUDA_PATH=/usr/local/cuda USE_CUDNN=1

```
---
# VScode
## 修改颜色
```
ctrl+k ctrl+t
```



