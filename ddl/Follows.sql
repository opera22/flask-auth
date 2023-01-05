CREATE TABLE "Follows" (
	"follower"	INTEGER NOT NULL,
	"followee"	INTEGER NOT NULL,
	PRIMARY KEY("follower","followee"),
	FOREIGN KEY("follower") REFERENCES "Users"("userid"),
	FOREIGN KEY("followee") REFERENCES "Users"("userid")
);