path "/agent/v1/metrics" {
  capabilities = ["list", "read"]
}

path "/proxy/v1/metrics" {
  capabilities = ["list", "read"]
}

path "/sys/metrics" {
  capabilities = ["list", "read"]
}
