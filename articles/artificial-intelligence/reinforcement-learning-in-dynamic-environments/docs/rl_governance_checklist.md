# Reinforcement Learning Governance Checklist

Recommended governance questions:

1. What reward function is being optimized?
2. Does the reward function reflect the intended system objective?
3. What actions are available to the agent?
4. What actions are prohibited?
5. What safety constraints are enforced?
6. How is exploration limited in high-risk states?
7. Is the environment stationary or non-stationary?
8. What hidden state or partial observability exists?
9. What simulation-to-real assumptions are being made?
10. How are constraint violations logged?
11. How is policy behavior monitored after deployment?
12. Can humans override or pause the agent?
13. What fallback policy exists?
14. What conditions require retraining or rollback?
15. Who owns incident review?
