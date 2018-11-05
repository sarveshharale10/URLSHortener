from flask import Flask,render_template,request,redirect
from redis import Redis
from hashlib import md5
from db import Mapping,MappingDao

redis = Redis()
mappingDao = MappingDao()
expiryTimeInSeconds = 600

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def form():
    if(request.method == 'GET'):
        return render_template('form.html',shortUrl="")
    elif(request.method == 'POST'):
        url = request.form['url']
        md5hash = md5(url.encode()).hexdigest()
        hash = md5hash[0:5]
        if(redis.exists(hash) and redis.get(hash).decode() != url):
            hash = md5hash[1:6]

        redis.set(hash,url)
        redis.expire(hash,expiryTimeInSeconds)
        mapping = Mapping(hash,url)
        mappingDao.add(mapping)
        
        shortUrl = "localhost/"+hash
        return render_template('form.html',shortUrl=shortUrl)


@app.route('/<hash>')
def redirectFromHash(hash):
    if(redis.exists(hash)):
        url = redis.get(hash)
    else:
        url = mappingDao.getbyhash(hash)
        redis.set(hash,url)
        redis.expire(hash,expiryTimeInSeconds)

    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True,port=80)