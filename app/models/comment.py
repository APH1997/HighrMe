from .db import db, environment, SCHEMA, add_prefix_for_prod


class Comment(db.Model):
    __tablename__ = 'comments'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')))
    photo_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('photos.id')))
    content = db.Column(db.String(200), nullable=False)

    photo = db.relationship(
        "Photo",
        back_populates="comments"
    )

    author = db.relationship(
        "User",
        back_populates="comments"
    )

    replies = db.relationship(
        "Reply",
        back_populates="parent"
    )

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author.to_dict(),
            'photo': self.photo.to_dict_no_author(),
            'content': self.content,
            'replies': [reply.to_dict() for reply in self.replies]
        }