extends Node3D

signal connection_established

var socket = WebSocketPeer.new()
var m0_center = -80
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Initiate connection to the given URL.
	var err = socket.connect_to_url("ws://localhost:8765")
	if err != OK:
		print("Unable to connect")
		set_process(false)
	else:
		await get_tree().create_timer(2).timeout
		
		# Send data.
		socket.send_text("Test packet")


func _on_connection_established():
	print("Connected to Python WebSocket")

func show_motor_positions(motor_positions: Variant):
	var text := "M0: %s\nM1: %s\nM2: %s\nM3: %s" % [
		motor_positions["M0"],
		motor_positions["M1"],
		motor_positions["M2"],
		motor_positions["M3"]
	]
	$CanvasLayer/Label.text = text
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	# Call this in _process or _physics_process. Data transfer and state updates
	# will only happen when calling this function..
	socket.poll()
	# get_ready_state() tells you what state the socket is in.
	var state = socket.get_ready_state()
	# WebSocketPeer.STATE_OPEN means the socket is connected and ready
	# to send and receive data.
	if state == WebSocketPeer.STATE_OPEN:
		while socket.get_available_packet_count():
			var message = socket.get_packet().get_string_from_utf8()
			var motor_positions = JSON.parse_string(message)
			if motor_positions:
				print(motor_positions)
				var m0_pos = $"stator".position
				var actual_m0_pos = -motor_positions["M0"] + m0_center
				m0_pos.z = actual_m0_pos
				$"stator".position = m0_pos
				$"stator".rotation.y = -motor_positions["M1"] + PI / 2
				$"arm".rotation.z = motor_positions["M2"]
				show_motor_positions(motor_positions)


	# WebSocketPeer.STATE_CLOSING means the socket is closing.
	# It is important to keep polling for a clean close.
	elif state == WebSocketPeer.STATE_CLOSING:
		pass
		# WebSocketPeer.STATE_CLOSED means the connection has fully closed.
	# It is now safe to stop polling.
	elif state == WebSocketPeer.STATE_CLOSED:
		# The code will be -1 if the disconnection was not properly notified by the remote peer.
		var code = socket.get_close_code()
		print("WebSocket closed with code: %d. Clean: %s" % [code, code != -1])
		set_process(false) # Stop processing.
	
