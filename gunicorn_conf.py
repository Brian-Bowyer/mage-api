# import multiprocessing

# the socket to bind to
bind = "0.0.0.0:80"

# number of pending connections / waiting clients
backlog = 256

# the number of worker processes that should be kept alive for handling requests
workers = 2  # multiprocessing.cpu_count() - 1

# which worker class to use [sync, gevent, eventlet, tornado, gthread].
# In case of gevent and eventlet use worker_connections = 1000.
worker_class = "uvicorn.workers.UvicornWorker"

# If a worker does not notify the master process in this number of seconds
# it is killed and a new worker is spawned to replace it
timeout = 180

# The number of seconds to wait for the next request
keepalive = 2

# - means stdout
errorlog = "-"
loglevel = "info"  # one of "debug", "info", "warning", "error", "critical"
accesslog = "-"

# remote address - username date http_status_line status response_length referer user_agent
# url_path query_string
# %(q) was giving us problems, letting it default for now
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(U) %(q)'
