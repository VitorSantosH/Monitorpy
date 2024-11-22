#crontab -u sgtrack -e
# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
#@reboot /bin/bash -c "/usr/local/bin/IniciarServico.sh"
@reboot /usr/local/bin/IniciarServico.sh


# sudo chmod 600 /tmp/iniciar_servico.log
# sudo chown sgtrack:sgtrack /tmp/iniciar_servico.log
# sudo chmod +x /usr/local/bin/IniciarServico.sh

# A SAIDA TEM QUE SER : 
#sgtrack@sgtrack:~ $ ls -l /usr/local/bin/IniciarServico.sh
#-rwxr-xr-x 1 root root 1395 Nov 21 12:39 /usr/local/bin/IniciarServico.sh
#sgtrack@sgtrack:~ $
# sudo apt install xdotool
# E O USUARIO QUE INICIAR A MAQUINA TEM QUE TER ESSA PERMISSÃO
# definir audio para p2 amixer cset numid=3 1
# testar audio speaker-test -D plughw:1,0 -t wav
# desativer economia de energia da tela sudo nano /etc/lightdm/lightdm.conf
# arquivo para ignorar ou ativar o mouse sudo nano /usr/share/X11/xorg.conf.d/50-invisible-cursor.conf