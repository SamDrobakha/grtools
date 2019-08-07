#Parses process data - spaces to new_lines. Usefull for Java long strings
ps -ef | grep $PROCESSID | grep -v grep | sed -E -e 's/[[:blank:]]+/\n/g'


#ssh tunnels example to servers via jumpbox machine ($jumpbox is 'user@host'). 
#EXAMPLE: Connection to local port 9011 will send you to 'stage_machine:8161'
ssh \
    -L 9011:stage_machine:8161 \
    -L 9021:pilot_machine:8161 \
    -L 9031:prod_machine:8161 \
    $jumpbox


#MACOS specific (they dont have 'ip' command)
#interfaces
networksetup -listallhardwareports
#my ip
ipconfig getifaddr en0


#site load
while true; do curl -s -w %{time_total}\\n -o /site/url/here/; sleep 1; done
#and
~/jmeter/apache-jmeter-5.1.1/bin/jmeter -n -t ~/jmeter/test.jmx