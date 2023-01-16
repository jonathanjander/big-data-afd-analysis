/*db.auth('admin-user', 'admin-password')
db = db.getSiblingDB('Big-Data-DB')
db.createCollection("Tweets");

db.createUser({
  user: 'test-user',
  pwd: 'test-password',
  roles: [
    {
      role: 'root',
      db: 'Big-Data-DB',
    },
  ],
});*/

conn = new Mongo();
//db = conn.getDB("Big-Data-DB");
db = db.getSiblingDB('Big-Data-DB')
db.createCollection("Tweets");
db.createCollection("TweetViews");
//db.getCollection("Tweets");
