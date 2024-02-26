import json
import aiohttp

from quart import Quart, request, render_template

app = Quart(__name__)

urlPath = {
    'disaster': '5001'
}

@app.route('/')
async def index():
    return await render_template('main.html')

@app.route('/<path>/<opt>', methods=['POST'])
async def router(path, opt):
    jsonData = json.loads(await request.get_data().decode())

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f'http://localhost:{urlPath[path]}/{opt}',
            data=json.dumps(jsonData)
        ) as res:
            return await res.json(content_type=None) \
                if res.status == 200 \
                    else json.dumps(res.raise_for_status())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

