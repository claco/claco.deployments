api_addr           = "http://127.0.0.1:8200"
disable_clustering = true
disable_mlock      = true
log_level          = "info"
log_file           = "/vault/logs/server.log"
log_format         = "standard"
ui                 = false

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}

storage "file" {
  path = "/vault/file"
}

telemetry {
  disable_hostname          = true
  prometheus_retention_time = "12h"
}
