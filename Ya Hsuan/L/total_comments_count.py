from sqlalchemy import create_engine, Column, Integer, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    articles_ID = Column(Integer, primary_key=True)
    campground_ID = Column(Integer, ForeignKey('campground.campground_ID'))

class Campground(Base):
    __tablename__ = 'campground'
    campground_ID = Column(Integer, primary_key=True)
    total_comments_count = Column(Integer)


engine = create_engine("mysql+pymysql://test:PassWord_1@104.199.214.113:3307/test2_db")
Session = sessionmaker(bind=engine)
session = Session()

# Step 1: 統計每個營地的評論數量
comment_counts = (
    session.query(
        Article.campground_ID,
        func.count().label('total_comments')
    )
    .group_by(Article.campground_ID)
    .all()
)

# Step 2: 更新 campground 表
for campground_id, count in comment_counts:
    session.query(Campground).filter(Campground.campground_ID == campground_id).update({
        Campground.total_comments_count: count
    })

session.commit()
session.close()
