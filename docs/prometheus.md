## Prometheus config `prometheus.yml`
```yaml
- job_name: 'heat-pump'
  scrape_interval: 30s
  metrics_path: '/metrics'
  scheme: "http"
  static_configs:
  - targets: ['ip-or-host-address:8555']
```