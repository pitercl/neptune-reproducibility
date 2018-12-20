#!/bin/bash
export RESULT=`curl --data "grant_type=password&client_id=neptune-cli&username=neptune&password=${PROD_NEPTUNE_PASS}" https://auth.neptune.ml/auth/realms/neptune/protocol/openid-connect/token`
export TOKEN=`echo "$RESULT" | jq -r '.access_token'`

SQL_HOST="35.189.246.6"
SQL_PORT="3306"
SQL_USER="root"
SQL_PASS="${PROD_SQL_ROOT_PASS}"

function db {
  mysql -h "${SQL_HOST}" -p"${SQL_PASS}" -u "${SQL_USER}" -P "${SQL_PORT}" -e "$1" $2
  return $?
}
#https://eap.neptune.ml/api/leaderboard/v1/organizations/uat-user/projects/sandbox/leaderboard?endDate=&limit=50&offset=0&sortBy=name&sortDirection=ascending&sortFieldType=native&startDate=&&trashed=false

DATA="$(db "use kubernetes_app_neptune; select CONCAT('organizations/', o.name,'/projects/', p.name) from experiment e join project p on p.id = e.project_id join organization o on o.id = p.organization_id where o.deleted is null and p.deleted is null group by p.id having count(e.id) >= 10;" -sN 2>/dev/null)"

for X in $DATA; do
  ADDR="https://app.neptune.ml/api/leaderboard/v1/$X/leaderboard?endDate=&limit=50&offset=0&sortBy=name&sortDirection=ascending&sortFieldType=native&startDate=&&trashed=false"
  ts=$(date +%s%N)
  curl "$ADDR" -H "Authorization: Bearer $TOKEN" -s -f -o /dev/null 2>/dev/null
  Y="$?"
  tt=$((($(date +%s%N) - $ts)/1000000))
  echo "$X ($Y): $tt ms"
done

