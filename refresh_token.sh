#!/bin/bash
response=$(curl -X POST https://api.prokerala.com/token \
  -d "grant_type=client_credentials" \
  -d "client_id=a9ff276c-13fb-4cbf-bf55-6564b67b8697" \
  -d "client_secret=l738LYKUWN7mAe2cKkZejZkOsQkF5GIwcF5y34Uq")
new_token=$(echo $response | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
sed -i "s/PROKERALA_ACCESS_TOKEN=.*/PROKERALA_ACCESS_TOKEN=$new_token/" ~/WorkSpace/lunaya/.env
echo "New token: $new_token"