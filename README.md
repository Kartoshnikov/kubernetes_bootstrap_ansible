On ElasticSearch run
  systemctl edit elasticsearch
and add the following line under the 'Service' stanza (create it if needed)
  OOMScoreAdjust=-900
then run
  systemctl daemon-reload
  systemctl restart elasticsearch 

Add the snippet below at the end of the inputs stanza in /etc/telegraf/telegraf.conf (see configMap)
and restart telegraf daemonset ( kubectl -n monitoring delete po --selector 'app.kubernetes.io/instance=telegraf' ) !Watch out: namespace can be changed in the future.

    [[inputs.linux_sysctl_fs]]
    [[inputs.interrupts]]
    [[inputs.internal]]
    [[inputs.netstat]]
    [[inputs.nstat]]
    [[inputs.conntrack]]
    dirs = ["/proc/sys/net/netfilter",]
    files = ["nf_conntrack_count","nf_conntrack_max"]

And also import the following dashboards into grafana

    9111  Kubernetes Aggregated Container Stats
    2577  Kubernetes Cluster Health Monitoring
    928   Telegraf: system dashboard
    10585 Docker Dashboard
    1150  InfluxDB Docker
    11074 Node Exporter for Prometheus Dashboard EN v20201010
    8588  Kubernetes Deployment Statefulset Daemonset metrics (edit fields in queries "pod_name" -> "pod" etc.)
    11594 Detailed pods resources (edit fields in queries "container_name" -> "container" etc.)
    4358  Elasticsearch
