ronment activation paths
VENV="venv/bin/activate"

# Function to run a service
run_service() {
	local service_dir=$1
	local port=$2
	local script=$3

	cd "$service_dir" || exit
	source "$VENV"
	fastapi dev --port "$port" --app server --host 0.0.0.0 "$script" &
	local pid=$!
	cd ..
	return $pid
}

# Run auth service
run_service "auth_service" 8002 "auth_service.py"
auth_pid=$?

# Run vault service
run_service "vault_service" 8003 "vault_service.py"
vault_pid=$?

# Run gateway service
run_service "gateway_service" 8001 "gateway_service.py"
gateway_pid=$?

# Wait for all services to start
wait $auth_pid $vault_pid $gateway_pid

