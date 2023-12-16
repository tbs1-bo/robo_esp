SELECT strftime('%Y-%m-%d %H:00:00', datetime(command.tstamp, 'unixepoch')) AS datum, COUNT(*) AS anzahl FROM 
	motor_command 
		INNER JOIN command 
		ON command.command_id = motor_command.command_id 
			INNER JOIN robot 
			ON robot.robot_id = command.robot_id 
				INNER JOIN motor 
				ON motor_command.motor_id = motor.motor_id
WHERE motor.name='motor_left'
GROUP BY datum
ORDER BY datum DESC;


--SELECT json.data, command.tstamp FROM command INNER JOIN json ON json.json_id = command.json_id WHERE datetime(command.tstamp, 'unixepoch') BETWEEN "2023-12-16 16:00:00" AND "2023-12-16 23:00:00" AND command.robot_id=2;