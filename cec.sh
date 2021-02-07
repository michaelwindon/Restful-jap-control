#!/usr/bin/expect


set tv [lindex $argv 0] 
set command [lindex $argv 1]

spawn telnet $tv
expect "/usr/local/bin #"
send "CEC_SEND_BYTES $command\r"
expect "*#"
send "exit\r"
exit
