from sqlmodel import Session
from main import engine
from models import AuctionItem
import random


def create_auction_item():
    r = random.randint(0, 100)
    item_name = f'Painting number {r}'
    item_description = f'This is the painting description'
    min_price = random.randint(5000, 20000)
    price_step = min_price/10
    return AuctionItem(item_name= item_name, item_description= item_description, min_price= min_price, price_step= price_step)



def create_auction_db():
    items = [create_auction_item() for _ in range(10)]
    with Session(engine) as session:
        session.add_all(items)