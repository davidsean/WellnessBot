# MongoDb Interactive Mode

Kick-off the docker compose shell into the `mongodb` docker container then run:
```bash
mongo admin -u root -p rootpassword
```

To login as the root user

From the mongo cli you can create a sample database and collections such as below:
```bash
use test # create a new database called test
db.createCollection("posts") # create a new collection called posts
```

You can also perform any number of db functions such as queries etc. and it is great for sandboxing. If you want to reset simply respin the docker compose.