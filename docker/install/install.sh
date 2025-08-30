#!/bin/bash
conda env remove -p /projects/vga/docker/assets/env_vga
conda create -p /projects/vga/docker/assets/env_vga  python=3.10.16  -y
source activate  /projects/vga/docker/assets/env_vga
pip  install -r /projects/vga/docker/install/requirements.txt --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple
