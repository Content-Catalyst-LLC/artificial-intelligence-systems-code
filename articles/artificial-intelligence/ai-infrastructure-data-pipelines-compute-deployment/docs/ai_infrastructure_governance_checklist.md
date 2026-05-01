# AI Infrastructure Governance Checklist

Recommended governance questions:

1. What data pipelines feed the system?
2. Are pipeline dependencies documented as a DAG?
3. Are data validation checks active?
4. Are training and serving feature definitions consistent?
5. Are datasets, features, models, and deployments versioned?
6. Is the model registered before deployment?
7. Are deployment approvals required?
8. Is rollback available?
9. Are latency, throughput, and error-rate metrics monitored?
10. Are model-specific signals monitored, including drift and calibration?
11. Are access controls enforced across data, code, models, and logs?
12. Are model artifacts signed or otherwise controlled?
13. Is observability available through metrics, logs, traces, and model signals?
14. Are incidents documented and reviewed?
15. Is governance integrated into the production lifecycle?
