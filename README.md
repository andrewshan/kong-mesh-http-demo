
## Topology

- Start a HTTP Service user that listen on 8089
- Start a HTTP Service shop that listen on 8090
- Start a HTTP Service promotion that listen on 8091
- Start Kong as a mesh sidecar in the same pod with the service
- Configure Kong and the pod iptables to send all traffic redirect through Kong

## Services API

### Service user

- /api/v6/user/create

create user info<br/>
call /api/v6/shop/items in the shop Service<br/>
response is {"result":{"userId":"1234", "userName":"vincent"}}

- /api/v6/user/accout/query

query account info for the user<br/>
call /api/v6/shop/order in the shop Service<br/>
response is {"userId":"1234", "detail":{"moneyLeft":52000,"deposit":12000}}

- /health

health checking<br/>
response is { "status":"UP" }

### Service shop

- /api/v6/shop/items

return the shop items info<br/>
response is {"items": [{"itemId":"001", "itemName":"cloth"}, {"itemId":"002", "itemName":"cloth1"}, {"itemId":"003", "itemName":"cloth2"}]}

- /api/v6/shop/order

place a shopping order<br/>
call /api/v6/promotion/query in the promotion Service<br/>
response is {"userId": "1234", "itemId": "002" }

- /api/v6/product/deliver

return the product delivery info<br/>
response is {"itemId": "002", "destination": "shenzhen"}

- /health

health checking<br/>
response is { "status":"UP" }

### Service promotion

- /api/v6/promotion/query

query the promotion details<br/>
response is {"promotions": [{"itemId":"001", "status":"off"}, {"itemId":"002", "status":"on"}, {"itemId":"003", "status":"on"} ]}

- /api/v6/promotion/item/discount

query the discount info for a specific item<br/>
call /api/v6/product/deliver in the shop Service<br/>
response is {"discount": "40", "itemId": "002" }

- /health

health checking<br/>
response is { "status":"UP" }
