import json
import asyncio
import concurrent.futures

from quart import Quart, request
from quart.wrappers import Request

app = Quart(__name__)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

def getList(data: Request.data):
    jsonData = json.loads(data.decode())

    data = f'인증된 사용자입니다. {jsonData["name"]}' \
        if jsonData['name'] == 'imsi' \
            else f'허용되지 않은 사용자입니다. {jsonData["name"]}'
    
    return json.dumps({
        'text': data,
    })

@app.route('/list', methods=['POST'])
async def index():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, getList, await request.get_data())
    return result

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)