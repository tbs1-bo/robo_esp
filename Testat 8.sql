SELECT strftime('%Y-%m-%d %H:00:00', datetime(command.tstamp, 'unixepoch')) AS datum, COUNT(*) AS anzahl FROM 
	motor_command 
		INNER JOIN command 
		ON command.command_id = motor_command.motor_command_id 
			INNER JOIN robot 
			ON robot.robot_id = command.robot_id 
				INNER JOIN motor 
				ON motor_command.motor_id = motor.motor_id
WHERE motor.name='motor_left'
GROUP BY datum
ORDER BY datum DESC;