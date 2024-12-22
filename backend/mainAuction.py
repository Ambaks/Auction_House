from fastapi import FastAPI
from sqlmodel import SQLModel, Session
from sqlalchemy import create_engine
import uvicorn
from starlette.websockets import WebSocket, WebSocketDisconnect
import datetime as dt


app = FastAPI()
eng = 'database.db'
sql_url = f'sqlite:///{eng}'
engine = create_engine(sql_url)
session = Session(bind=engine)

class AuctionConnectionManager:
    def __init__(self):
        self.auction_connections: dict[any, list] = {}

    async def connect(self, websocket: WebSocket, auction_id):
        await websocket.accept()
        if not self.auction_connections.get(auction_id):
            self.auction_connections[auction_id] = []
        self.auction_connections[auction_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, auction_id):
        self.auction_connections[auction_id].remove(websocket)
    
    async def broadcast(self, message: str, auction_id: int, new_price = None, ends = None):
        for connection in list(self.auction_connections.get(auction_id)):
            await connection.send_text(message)
            payload = {}

            if new_price:
                payload = {'new_price'}

            if ends:
                payload.update(ends = str(ends))
            
            if payload.keys():
                await connection.send_json(payload)

manager = AuctionConnectionManager()


@app.websocket('/websocket/{id}/ws/{participant_id}')
async def auction(websocket: WebSocket, id: int, participant_id: int):
    from models import AuctionItem
    await manager.connect(websocket, id)
    try:
        while True:
            data = await websocket.receive_json()
            item = session.get(AuctionItem, id)
            step = item.price_step
            current_bid = item.bid or 0
            min_new_bid = current_bid + step
            new_bid = data.get('bid')

            if not new_bid:
                continue
            if participant_id == item.bidder_id or not new_bid > current_bid:
                continue
            if item.min_price < new_bid >= min_new_bid:
                item.bid = new_bid
                item.bidder_id = participant_id
                item.ends = dt.datetime.now() + dt.timedelta(seconds = 60)
                session.commit()
                await manager.broadcast(f'Participant {participant_id} has bid {item.bid}!', auction_id=id,  new_price=item.bid,
                                        ends= item.ends)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, id)
        await manager.broadcast(f'Participant has left the auction', auction_id=id)
            



if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
    #SQLModel.metadata.create_all(engine)