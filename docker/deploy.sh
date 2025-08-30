#!/bin/bash

git remote set-url origin git@gitlab.gwm.cn:LLM/ai_solutions/vga.git

docker build  --no-cache=false -f Dockerfile -t jhao/vga .

docker build   --no-cache=true  --network host --build-arg "HTTP_PROXY=http://127.0.0.1:7890" --build-arg "HTTPS_PROXY=http://127.0.0.1:7890"   --build-arg "NO_PROXY=localhost,127.0.0.1" -f Dockerfile -t jhao/vga .



docker exec -it vga bash /projects/vga/docker/run/run.sh

docker stop  vga && docker rm  vga

docker run --gpus all -it --name vga  \
  --network host  \
  jhao/vga

docker rmi  jhao/vga

docker restart vga
# 长城云镜像

docker login vestack-registry.gwm.cn -u 'paas2b@1000000000' -p 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlNVWVk6SllCWTpQWklJOkpNWUQ6NkRKTjpVM1hMOkpFRk86R09PVzpRTDZJOkZCNEg6WTY2WjpJQzI0In0.eyJpc3MiOiJjci1pc3N1ZXIiLCJzdWIiOiJwYWFzMmJAMTAwMDAwMDAwMCIsImF1ZCI6WyJjciJdLCJleHAiOjE3NTEyNjM1NzUsIm5iZiI6MTc1MTI1OTk3NSwiaWF0IjoxNzUxMjU5OTc1LCJqdGkiOiJuOFAyblJQSnc0cnZMcWJ5IiwiaWRlbnRpdHlfdHlwZSI6ImFjY291bnQiLCJpZGVudGl0eV9hY2NvdW50X2lkIjoxMDAwMDAwMDAwLCJpZGVudGl0eV91c2VyX2lkIjoxMDAwMDAwMDAwfQ.Wc3SCdOpxfJ9x0Io4Qkd6WI_bta3zusf8v89yHzyevVT86Jre5esz4Z4AVDftzT1dxjXBiKzc8LsBb6EnSIM3zETscZWEiSbnj5rjzigUr95MhowN6URvAFMkPxE4GxBN98QbYAjtLnURlH7sPdigPjjagSCQSJPswY83raf3__TWorg-QKvYAAjOofhK_UAvKzi4aziDqTykqoUKq2I9mji2nqWviKdnRlbzXokKX8DUge4ag3sJeZ5CsVnogzKQjQ4WmjrwdOToPyYS0VFyzKpwKetqs4lDU_5JjD2AkZjH9tDqS6pQqws4H2CsTY01zMre4NZwQMbcM75q8jXfw'


docker tag jhao/vga  vestack-registry.gwm.cn/library/vga:v1.0

docker push vestack-registry.gwm.cn/library/vga:v1.0

ssh -i /home/jhao/space/projects/Project/ai/projects/ComfyUI/assets/ssh_keys/id_rsa -p 31177 root@10.240.243.203

docker exec -it vga bash /projects/vga/docker/run/run.sh

docker exec -it cat  /projects/vga/log/vga.log

# 阿里云镜像

docker login --username=1120260400@qq.com --password "(Jh050565)" registry.cn-shanghai.aliyuncs.com

docker tag jhao/vga  registry.cn-shanghai.aliyuncs.com/jhao_ai_images/vga:v2.9

docker push registry.cn-shanghai.aliyuncs.com/jhao_ai_images/vga:v2.9


10.240.243.203:31109

curl -X POST http://localhost:8080/runsync \
     -H "Content-Type: application/json" \
     -d '{"input": {"prompt": "你是谁"}}'