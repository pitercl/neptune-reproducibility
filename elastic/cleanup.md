```
kubectl scale deployment -n neptune neptune-instance-leaderboard --replicas=0
Inside cluster:
curl -X DELETE elasticsearch-client.elasticsearch:9200/project-leaderboard
curl -X DELETE  elasticsearch-client.elasticsearch:9200/organization-leaderboard

SQL:
use kubernetes_leaderboard;
DELETE FROM group_leaderboard;
DELETE FROM project_leaderboard;
DELETE FROM organization_leaderboard;

# update leaderboard

sleep 60
kubectl scale deployment -n neptune neptune-instance-leaderboard --replicas=1
```

