from app import db, login_manager, bcrypt
import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


def get_current_timestamp() -> datetime.datetime:
    """GetDate time implementation"""
    return datetime.datetime.now()


class UserModel(db.Model, UserMixin):
    """User model implementation"""

    __tablename__ = "auth_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(64), default="")
    last_name = db.Column(db.String(64), default="")
    twises = db.relationship("TwisModel", backref="userid", cascade="all,delete,delete-orphan", single_parent=True,
                             order_by="desc(TwisModel.date)")

    @property
    def pk(self):
        return self.id

    def check_password(self, password: str) -> bool:
        """Check passed raw password with user assigned"""

        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def generate_hashed_password(raw_password: str) -> str:
        """Return hashed password"""

        return bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def __repr__(self) -> str:
        """Return a string representation of an instance"""

        return f"<UserModel(username='{self.username}', email='{self.email}')>"

    def __str__(self) -> str:
        """Return a string version of an instance"""

        return self.username


class TwisModel(db.Model):
    """Twis model implementation"""

    __tablename__ = "twises"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=get_current_timestamp().replace(microsecond=0).isoformat(' '))
    date_update = db.Column(db.DateTime, nullable=True)
    user_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)

    @property
    def pk(self):
        return self.id

    @property
    def twis_text(self):
        return self.value

    def __repr__(self) -> str:
        """Return a string representation of instance"""

        return f"<TwissModel(value='{self.value}')>"

    def __str__(self) -> str:
        """Return a string version of an instance"""
        return (f"twis_text={self.value}")
