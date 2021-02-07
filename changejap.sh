#!/usr/bin/expect


set room [lindex $argv 0] 
set source [lindex $argv 1] 
set action [lindex $argv 2]
set on "switchon" 
set off "switchoff"
set onDescription $on$source
set offDescription $off$source
set offstatesource 11

log_user 0
spawn telnet 192.168.54.34

if { $action == "status"} {
	expect "Username:"
	send "admin\r"
	expect "Password:"
	send "admin\r"
	expect "#"
	set timeout 1
	send "show interface GigabitEthernet 1/$room description\r"
	expect {
		$onDescription {send_user  "on"; send "exit\r"; exit }
		$offDescription {send_user "off"; send "exit\r"; exit }
		send_user "off"; send "exit\r"; exit
	}
	send_user "off"
	send "exit\r"
	exit

} else {
	expect "Username:"
	send "admin\r"
	expect "Password:"
	send "admin\r"
	expect "#"
	send "config t\r"
	expect "(config)#"
	send "interface GigabitEthernet 1/$room\r"
	expect "(config-if)#"

	if { $action == "switchon"} {
		send "description $action$source\r"
		expect "(config-if)#"
		send "switchport hybrid allowed vlan 10,$source\r"
	} else {
		send "description $action$offstatesource\r" 
		expect "(config-if)#"
		send "switchport hybrid allowed vlan 10,$offstatesource\r"
		
	}

expect  -re ".*#"
send "exit\r"
exit
}
