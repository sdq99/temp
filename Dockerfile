FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

# INSTALL SOURCES FOR CHROME REMOTE DESKTOP AND VSCODE
RUN apt-get update && apt-get upgrade --assume-yes
RUN apt-get --assume-yes install curl gpg wget apt-utils
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# INSTALL XFCE DESKTOP AND DEPENDENCIES
RUN apt-get update && apt-get upgrade --assume-yes
RUN apt-get install --assume-yes --fix-missing sudo wget apt-utils xvfb xfce4 xbase-clients \
    desktop-base vim xscreensaver google-chrome-stable python-psutil psmisc python3-psutil xserver-xorg-video-dummy ffmpeg dialog python3-xdg python3-packaging
RUN apt-get install libutempter0
RUN wget https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb
RUN dpkg --install chrome-remote-desktop_current_amd64.deb
RUN apt-get install --assume-yes --fix-broken
RUN bash -c 'echo "exec /etc/X11/Xsession /usr/bin/xfce4-session" > /etc/chrome-remote-desktop-session'


# ---------------------------------------------------------- 
# SPECIFY VARIABLES FOR SETTING UP CHROME REMOTE DESKTOP
ARG USER=myuser
# use 6 digits at least
ENV PIN=123456
#ENV CODE=4/0AeanS0bGIucL5NETahHxevhOu-bGxpL1v32W-ufQ8yavkemG6WjnobMqSi0EP1Nklqxmcw
ENV CODE=4/0AeanS0Z0KF4FEmevAhovk6FIY5k6xgvNokQfXGiwe77a-cBRAUfw_JF2wSYajUj4bHdoOg
ENV HOSTNAME=myvirtualdesktop
# ---------------------------------------------------------- 
# ADD USER TO THE SPECIFIED GROUPS
RUN adduser --disabled-password --gecos '' $USER
RUN mkhomedir_helper $USER
RUN adduser $USER sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN usermod -aG chrome-remote-desktop $USER
USER $USER
WORKDIR /home/$USER
RUN mkdir -p .config/chrome-remote-desktop
RUN chown "$USER:$USER" .config/chrome-remote-desktop
RUN chmod a+rx .config/chrome-remote-desktop
RUN touch .config/chrome-remote-desktop/host.json
RUN echo "/usr/bin/pulseaudio --start" > .chrome-remote-desktop-session
RUN echo "startxfce4 :1030" >> .chrome-remote-desktop-session

# SETUP FOR LC
RUN sudo wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/sublimehq-archive.gpg > /dev/null
RUN echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
RUN sudo apt-get update
RUN sudo apt-get install --assume-yes sublime-text cron python3.8-venv firefox
RUN sudo service cron start
RUN sudo mkdir /usr/xorg && sudo mkdir /usr/xorg/leetcode
RUN sudo chown -R $USER:$USER /usr/xorg
RUN python3 -m venv /usr/xorg/venv
RUN /usr/xorg/venv/bin/pip install selenium
RUN /usr/xorg/venv/bin/pip install requests
RUN firefox --headless -CreateProfile "sdq99 /usr/xorg/leetcode/firefox_profiles/sdq99"
RUN firefox --headless -CreateProfile "sdq996 /usr/xorg/leetcode/firefox_profiles/sdq996"
RUN firefox --headless -CreateProfile "sdq997 /usr/xorg/leetcode/firefox_profiles/sdq997"
RUN firefox --headless -CreateProfile "sdq998 /usr/xorg/leetcode/firefox_profiles/sdq998"
RUN firefox --headless -CreateProfile "sdq999 /usr/xorg/leetcode/firefox_profiles/sdq999"
COPY leetcode*.py geckodriver /usr/xorg/leetcode/
USER root
RUN sudo echo "2 0 * * * /bin/bash -c 'source /usr/xorg/venv/bin/activate && python /usr/xorg/leetcode/leetcode.py && deactivate' >> /usr/xorg/leetcode/leetcode.log 2>&1" >> /var/spool/cron/crontabs/myuser \
    && sudo echo "2 2 * * * /bin/bash -c 'source /usr/xorg/venv/bin/activate && python /usr/xorg/leetcode/leetcode.py && deactivate' >> /usr/xorg/leetcode/leetcode.log 2>&1" >> /var/spool/cron/crontabs/myuser \
    && sudo echo "32 2 * * 0 /bin/bash -c 'source /usr/xorg/venv/bin/activate && python /usr/xorg/leetcode/leetcode-weekly.py && deactivate' >> /usr/xorg/leetcode/leetcode-weekly.log 2>&1" >> /var/spool/cron/crontabs/myuser \
    && sudo echo "2 3 * * 0 /bin/bash -c 'source /usr/xorg/venv/bin/activate && python /usr/xorg/leetcode/leetcode-weekly.py && deactivate' >> /usr/xorg/leetcode/leetcode-weekly.log 2>&1" >> /var/spool/cron/crontabs/myuser \
    && sudo echo "32 14 * * 6 /bin/bash -c 'source /usr/xorg/venv/bin/activate && python /usr/xorg/leetcode/leetcode-bi-weekly.py && deactivate' >> /usr/xorg/leetcode/leetcode-bi-weekly.log 2>&1" >> /var/spool/cron/crontabs/myuser \
    && sudo echo "2 15 * * 6 /bin/bash -c 'source /usr/xorg/venv/bin/activate && python /usr/xorg/leetcode/leetcode-bi-weekly.py && deactivate' >> /usr/xorg/leetcode/leetcode-bi-weekly.log 2>&1" >> /var/spool/cron/crontabs/myuser




RUN chown myuser:myuser /var/spool/cron/crontabs/myuser

RUN sudo service cron start

USER $USER
RUN sudo service cron start
CMD [ "sh", "-c", "DISPLAY= /opt/google/chrome-remote-desktop/start-host --code=$CODE --redirect-url=\"https://remotedesktop.google.com/_/oauthredirect\" --name=$HOSTNAME --pin=$PIN && \
   HOST_HASH=$(echo -n $HOSTNAME | md5sum | cut -c -32) && \
   FILENAME=.config/chrome-remote-desktop/host#${HOST_HASH}.json && echo $FILENAME && \
   cp .config/chrome-remote-desktop/host#*.json $FILENAME && \
   sudo service chrome-remote-desktop stop && \
   sudo service chrome-remote-desktop start && \
   echo $HOSTNAME && \
   sleep infinity" ]
