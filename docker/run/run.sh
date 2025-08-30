#!/bin/bash
cd /projects/vga
git pull
folder_path="/projects/vga/log/vga"
if [ ! -d "$folder_path" ]; then
    mkdir -p "$folder_path"
    echo "文件夹 '$folder_path' 已创建。"
else
    echo "文件夹 '$folder_path' 已存在。"
fi
export PYTHONPATH=$PYTHONPATH:/projects/vga
source /opt/conda/etc/profile.d/conda.sh
conda activate /projects/vga/docker/assets/env_vga
cd /projects/vga/vga_agents

#python ai_painting_agent_serverless.py --rp_serve_api --rp_api_host 0.0.0.0 --rp_api_port 8080

#python ai_painting_agent_serverless.py  --rp_api_host 0.0.0.0 --rp_api_port 8080

python ai_painting_agent.py

