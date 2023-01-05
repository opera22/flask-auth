CREATE TABLE "Posts" (
	"postid"	INTEGER NOT NULL,
	"userid"	INTEGER NOT NULL,
	"content"	TEXT NOT NULL,
	"created_at"	TEXT NOT NULL,
	PRIMARY KEY("postid" AUTOINCREMENT),
	FOREIGN KEY("userid") REFERENCES "Users"("userid")
);