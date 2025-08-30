FROM jhao/modeling

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update &&  apt-get upgrade -y --fix-missing

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    xdg-utils \
    build-essential

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -

RUN apt-get install -y nodejs
RUN npm install -g serve

# projects
RUN cd /projects  &&  git clone https://jintou:jh050565@gitee.com/jintou/vga.git
ENV projects_env=2
COPY --chown=root:root assets/env_vga /projects/vga/docker/assets/env_vga
ENV projects_version=9
RUN mkdir -p /projects/vga/docker/assets
RUN cd /projects/vga  && git pull
EXPOSE 7860
EXPOSE 22
EXPOSE 8000
EXPOSE 8080

CMD [ "bash", "-c", "/projects/vga/docker/run/run.sh" ]
#
#CMD [ "bash", "-c", "/opt/run/start.sh" ]