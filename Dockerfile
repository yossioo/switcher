FROM python:3.10

# USE BASH
SHELL ["/bin/bash", "-c"]

RUN useradd -ms /bin/bash user

RUN mkdir /app
RUN mkdir /config
RUN chown user:user -R /app
RUN chown user:user -R /config
USER user
WORKDIR /app
RUN python3 -m pip install wheel
# RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install pyaes==1.6.1 Pyrogram==1.4.7 PySocks==1.7.1  TgCrypto==1.2.3 pyyaml==5.4.1 coloredlogs==15.0.1

COPY app /app
CMD [ "python3", "switcher_v2.py" ]

