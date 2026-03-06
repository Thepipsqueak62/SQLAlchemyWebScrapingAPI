import httpx
from selectolax.parser import HTMLParser
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///quotes.db",echo=True)
Base = declarative_base()

class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    quote = Column(Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



def db_quotes():
    html = httpx.get(f"https://quotes.toscrape.com/")
    tree = HTMLParser(html.text)
    for quote in tree.css('.quote'):
        new_quote= Quote(quote=quote.css_first('.text').text(strip=True))
        session.add(new_quote)
        session.commit()

db_quotes()













