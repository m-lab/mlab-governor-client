query_template= "bq --format=csv query -n 900000 "

upload_query=("SELECT test_id, STRFTIME_UTC_USEC(INTEGER(web100_log_entry.log_time) * 1000000, '%Y-%m-%d %T') AS day_timestamp,"
			" connection_spec.client_ip, connection_spec.server_ip, connection_spec.client_application, connection_spec.client_geolocation.city,"
			" connection_spec.client_geolocation.latitude, connection_spec.client_geolocation.longitude,"
			" 8 * web100_log_entry.snap.HCThruOctetsReceived/web100_log_entry.snap.Duration AS uploadThroughput,"
			" web100_log_entry.snap.Duration, web100_log_entry.snap.HCThruOctetsReceived"
			" FROM "
				"[plx.google:m_lab.2016_01.all]"
			" WHERE"
				" IS_EXPLICITLY_DEFINED(web100_log_entry.snap.Duration)"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.HCThruOctetsReceived)"
				" AND web100_log_entry.snap.HCThruOctetsReceived >= 8192"
				" AND IS_EXPLICITLY_DEFINED(project)"
				" AND project = 0"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.is_last_entry)"
				" AND web100_log_entry.snap.Duration >= 9000000"
				" AND web100_log_entry.snap.Duration < 3600000000"
				" AND (connection_spec.client_application = '{test_id}' ")

download_query= ("SELECT test_id, STRFTIME_UTC_USEC((INTEGER(web100_log_entry.log_time) * 1000000), '%Y-%m-%d %T') AS day_timestamp,"
				" connection_spec.client_ip, connection_spec.server_ip, connection_spec.client_geolocation.city,"
				" connection_spec.client_geolocation.latitude, connection_spec.client_geolocation.longitude,"
				" 8 * web100_log_entry.snap.HCThruOctetsAcked/ (web100_log_entry.snap.SndLimTimeRwin +"
					" web100_log_entry.snap.SndLimTimeCwnd + web100_log_entry.snap.SndLimTimeSnd)"
					" AS downloadThroughput,"
				" web100_log_entry.snap.HCThruOctetsAcked, web100_log_entry.snap.SndLimTimeRwin, web100_log_entry.snap.SndLimTimeCwnd,"
				" web100_log_entry.snap.SndLimTimeSnd, web100_log_entry.snap.CongSignals"
				" FROM"
					" [plx.google:m_lab.2016_01.all]"
				" WHERE"
				" IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeRwin)"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeCwnd)"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeSnd)"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.is_last_entry)"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.HCThruOctetsAcked)"
				" AND IS_EXPLICITLY_DEFINED(project)"
				" AND project = 0 "
				" AND IS_EXPLICITLY_DEFINED(connection_spec.data_direction)"
				" AND connection_spec.data_direction = 1 "
				" AND web100_log_entry.snap.HCThruOctetsAcked >= 8192"
				" AND (web100_log_entry.snap.SndLimTimeRwin + web100_log_entry.snap.SndLimTimeCwnd + web100_log_entry.snap.SndLimTimeSnd) >= 9000000"
				"AND (web100_log_entry.snap.SndLimTimeRwin + web100_log_entry.snap.SndLimTimeCwnd + web100_log_entry.snap.SndLimTimeSnd)"
				" < 3600000000 AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.CongSignals) AND web100_log_entry.snap.CongSignals > 0"
				" AND (connection_spec.client_application = '{test_id}' ")

rtt_query=  ("SELECT test_id, STRFTIME_UTC_USEC((INTEGER(web100_log_entry.log_time) * 1000000), '%Y-%m-%d %T') AS day_timestamp,"
			" connection_spec.client_ip, connection_spec.server_ip, connection_spec.client_application, connection_spec.client_geolocation.city,"
			" connection_spec.client_geolocation.latitude, connection_spec.client_geolocation.longitude, web100_log_entry.snap.MinRTT AS min_rtt"
			" FROM"
				" [plx.google:m_lab.2016_01.all]"
			" WHERE"
				" IS_EXPLICITLY_DEFINED(web100_log_entry.connection_spec.remote_ip)"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.connection_spec.local_ip)"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.HCThruOctetsAcked)"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeRwin)"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeCwnd)"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeSnd)"
				" AND project = 0"
				" AND IS_EXPLICITLY_DEFINED(connection_spec.data_direction)"
				" AND connection_spec.data_direction = 1"
				" AND IS_EXPLICITLY_DEFINED(web100_log_entry.is_last_entry)"
				" AND web100_log_entry.is_last_entry = True"
				" AND web100_log_entry.snap.HCThruOctetsAcked >= 8192"
				" AND (web100_log_entry.snap.SndLimTimeRwin + web100_log_entry.snap.SndLimTimeCwnd + web100_log_entry.snap.SndLimTimeSnd) >= 9000000"
	 			" AND (web100_log_entry.snap.SndLimTimeRwin + web100_log_entry.snap.SndLimTimeCwnd + web100_log_entry.snap.SndLimTimeSnd) < 3600000000"
	 			" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.MinRTT)"
	 			" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.CountRTT)"
				" AND web100_log_entry.snap.CountRTT > 10"
	 			" AND (web100_log_entry.snap.State == 1"
	 				" OR (web100_log_entry.snap.State >= 5 AND web100_log_entry.snap.State <= 11))"
				" AND (connection_spec.client_application = '{test_id}' ")
					

# Packet Retransmission Rate
packet_retrans_query=   ("SELECT test_id, STRFTIME_UTC_USEC((INTEGER(web100_log_entry.log_time) * 1000000), '%Y-%m-%d %T') AS day_timestamp,"
						" connection_spec.client_ip, connection_spec.server_ip, connection_spec.client_application, connection_spec.client_geolocation.city,"
						" connection_spec.client_geolocation.latitude, connection_spec.client_geolocation.longitude,"
 						" (web100_log_entry.snap.SegsRetrans / web100_log_entry.snap.DataSegsOut) AS packet_retransmission_rate"
						" FROM"
							" [plx.google:m_lab.2016_01.all]"
						" WHERE"
							" IS_EXPLICITLY_DEFINED(web100_log_entry.connection_spec.remote_ip)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.connection_spec.local_ip)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.HCThruOctetsAcked)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeRwin)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeCwnd)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeSnd)"
							" AND project = 0"
							" AND IS_EXPLICITLY_DEFINED(connection_spec.data_direction)"
							" AND connection_spec.data_direction = 1"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.is_last_entry)"
							" AND web100_log_entry.is_last_entry = True"
							" AND web100_log_entry.snap.HCThruOctetsAcked >= 8192"
							" AND (web100_log_entry.snap.SndLimTimeRwin +"
							 	" web100_log_entry.snap.SndLimTimeCwnd +"
							 	" web100_log_entry.snap.SndLimTimeSnd) >= 9000000"
							" AND (web100_log_entry.snap.SndLimTimeRwin +"
							 	" web100_log_entry.snap.SndLimTimeCwnd +"  
							 	" web100_log_entry.snap.SndLimTimeSnd) < 3600000000"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SegsRetrans)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.DataSegsOut)"
							" AND web100_log_entry.snap.DataSegsOut > 0"
							" AND (web100_log_entry.snap.State == 1"
								" OR (web100_log_entry.snap.State >= 5"
									" AND web100_log_entry.snap.State <= 11))"
							" AND (connection_spec.client_application = '{test_id}' ")

# Network Limited Ratio
net_lim_ratio_query=("SELECT test_id, STRFTIME_UTC_USEC((INTEGER(web100_log_entry.log_time) * 1000000), '%Y-%m-%d %T') AS day_timestamp,"
					" connection_spec.client_ip, connection_spec.server_ip, connection_spec.client_application,"
					" connection_spec.client_geolocation.city, connection_spec.client_geolocation.latitude, connection_spec.client_geolocation.longitude,"
 					" web100_log_entry.snap.SndLimTimeCwnd / (web100_log_entry.snap.SndLimTimeRwin + web100_log_entry.snap.SndLimTimeCwnd +"
					" web100_log_entry.snap.SndLimTimeSnd) AS network_limited_time"
					" FROM"
						"[plx.google:m_lab.2016_01.all]"
					" WHERE"
						" IS_EXPLICITLY_DEFINED(web100_log_entry.connection_spec.remote_ip)"
						" AND IS_EXPLICITLY_DEFINED(web100_log_entry.connection_spec.local_ip)"
						" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.HCThruOctetsAcked)"
						" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeRwin)"
						" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeCwnd)"
						" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeSnd)"
						" AND project = 0"
						" AND IS_EXPLICITLY_DEFINED(connection_spec.data_direction)"
						" AND connection_spec.data_direction = 1"
						" AND IS_EXPLICITLY_DEFINED(web100_log_entry.is_last_entry)"
						" AND web100_log_entry.is_last_entry = True"
						" AND web100_log_entry.snap.HCThruOctetsAcked >= 8192"
						" AND (web100_log_entry.snap.SndLimTimeRwin +"
							" web100_log_entry.snap.SndLimTimeCwnd +"
							" web100_log_entry.snap.SndLimTimeSnd) >= 9000000"
						" AND (web100_log_entry.snap.SndLimTimeRwin +"
							" web100_log_entry.snap.SndLimTimeCwnd +"  
							" web100_log_entry.snap.SndLimTimeSnd) < 3600000000"
						" AND (web100_log_entry.snap.State == 1"
							" OR (web100_log_entry.snap.State >= 5 AND web100_log_entry.snap.State <= 11))"
						" AND (connection_spec.client_application = '{test_id}' ")

# Receiver (Client) Limited Ratio
client_lim_ratio_query= ("SELECT test_id, STRFTIME_UTC_USEC((INTEGER(web100_log_entry.log_time) * 1000000), '%Y-%m-%d %T') AS day_timestamp,"
						" connection_spec.client_ip, connection_spec.server_ip, connection_spec.client_application,"
						" connection_spec.client_geolocation.city, connection_spec.client_geolocation.latitude, connection_spec.client_geolocation.longitude,"
						" web100_log_entry.snap.SndLimTimeRwin /"
							" (web100_log_entry.snap.SndLimTimeRwin +"
							" web100_log_entry.snap.SndLimTimeCwnd +"
							" web100_log_entry.snap.SndLimTimeSnd) AS receiver_limited_time"
						" FROM"
							" [plx.google:m_lab.2016_01.all]"
						" WHERE"
							" IS_EXPLICITLY_DEFINED(web100_log_entry.connection_spec.remote_ip)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.connection_spec.local_ip)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.HCThruOctetsAcked)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeRwin)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeCwnd)"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeSnd)"
							" AND project = 0"
							" AND IS_EXPLICITLY_DEFINED(connection_spec.data_direction)"
							" AND connection_spec.data_direction = 1"
							" AND IS_EXPLICITLY_DEFINED(web100_log_entry.is_last_entry)"
							" AND web100_log_entry.is_last_entry = True"
							" AND web100_log_entry.snap.HCThruOctetsAcked >= 8192"
							" AND (web100_log_entry.snap.SndLimTimeRwin +"
							  " web100_log_entry.snap.SndLimTimeCwnd +"
							  " web100_log_entry.snap.SndLimTimeSnd) >= 9000000"
							" AND (web100_log_entry.snap.SndLimTimeRwin +"
							  " web100_log_entry.snap.SndLimTimeCwnd +"
							  " web100_log_entry.snap.SndLimTimeSnd) < 3600000000"
							" AND (web100_log_entry.snap.State == 1"
							  " OR (web100_log_entry.snap.State >= 5"
							      " AND web100_log_entry.snap.State <= 11))"
							" AND (connection_spec.client_application = '{test_id}' ")


commands = {
			"client_lim_ratio_query": client_lim_ratio_query, 
			"net_lim_ratio_query": net_lim_ratio_query, 
			"packet_retrans_query": packet_retrans_query, 
			"rtt_query": rtt_query, 
			"download_query": download_query, 
			"upload_query":upload_query
			}


def format_command(query_string, testId): 
	"""
	Options for query_string: 
		client_lim_ratio_query
		net_lim_ratio_query
		packet_retrans_query
		rtt_query
		download_query
		upload_query
	""" 
	query= commands[query_string].format(test_id= testId)
	return query_template +"\""+ query











