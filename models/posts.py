import sqlalchemy

metadata = sqlalchemy.MetaData()

posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("content", sqlalchemy.String)
)

comments = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column(
        "post_id", sqlalchemy.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    ),
    sqlalchemy.Column("content", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("publication_date", sqlalchemy.DateTime(), nullable=False)
)
