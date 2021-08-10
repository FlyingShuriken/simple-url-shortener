from flask import *
import random
import string
import json

app = Flask(__name__)
with open("./settings/settings.json","r") as file:
    settings = json.load(file)
    base_url = settings["your_domain_or_url"]

def generate(keys):
    code = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))
    if code not in keys:
        return code
    else:
        with open("short_url.json","r") as file:
            all = json.load(file)
        generate(list(all.keys()))

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/short",methods=["GET","POST"])
def short():
    url = request.args.get("url")
    print(url)
    with open("short_url.json","r") as file:
        all = json.load(file)

    if url not in list(all.values()):
        code = generate(list(all.keys()))
        all[code] = url
    else:
        code = list(all.keys())[list(all.values()).index(url)]
        full = f"{base_url}/url/{code}"
        return render_template("short.html",url = full)


    with open("short_url.json","w") as file:
        json.dump(all,file)

    full = f"{base_url}/url/{code}"
    return render_template("short.html",url = full)

@app.route("/url/<code>",methods=["GET","POST"])
def any(code):
    with open("short_url.json","r") as file:
        all = json.load(file)

    if code not in list(all.keys()):
        return redirect("/")
    elif code in list(all.keys()):
        url = all[code]
        return redirect(url)
