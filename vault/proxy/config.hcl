log_level  = "info"
log_file   = "/vault/logs/agent.log"
log_format = "standard"

api_proxy {
  use_auto_auth_token = "force"
}

auto_auth {
  method {
    type = "approle"
    config = {
      role_id_file_path                   = "/home/vault/role-id"
      secret_id_file_path                 = "/home/vault/secret-id"
      remove_secret_id_file_after_reading = false
    }
  }
  sink "file" {
    config = {
      path = "/home/vault/.vault-token"
    }
  }
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}

telemetry {
  disable_hostname          = true
  prometheus_retention_time = "12h"
}

vault {
  retry {
    num_retries = 5
  }
}
