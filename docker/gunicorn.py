import gunicorn

accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Forwarded-For}i)s"'
capture_output = True
forwarded_allow_ips = "*"
secure_scheme_headers = {"X-CLOUDFRONT": "yes"}
workers = 2
worker_class = "gthread"
worker_connections = 5
bind = ":8000"
keep_alive = 75
chdir = "/madewithwagtail"

# Obfuscate the Server header (to the md5sum of "Springload")
gunicorn.SERVER_SOFTWARE = "04e96149a2f64d6135c82d199ab62122"
