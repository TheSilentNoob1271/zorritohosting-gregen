from flask import Flask, render_template, request, Response
from ngvlib.subnetExpander import subnetExpander
import secrets
import os

app = Flask(__name__, template_folder="./public")

APP__NAME = "GRE x VirtFusion"
def APP_HASH():
    return secrets.token_hex(32)


class SYSAPP:
    def __init__(self, APP__NAME):
        self.Name = APP__NAME

    def getName(self):
        return self.Name

    
APP = SYSAPP(APP__NAME=APP__NAME)

def GenerateURL(remoteip, localip, greip1, defaultroute, bridgename, gateway, newIPs):
    # Generate Hash
    hash = APP_HASH()
    print(hash)
    if os.path.exists(f"./curl/{hash}"):

        pass

    else:

        # Append data
        with open(f"./curl/{hash}", "a") as f:
            f.write(f"ip tunnel add gre1 mode gre local {localip} remote {remoteip} ttl 255\n")
            f.write(f"ip addr add {greip1}/30 dev gre1\n")
            f.write(f"ip link set gre1 up\n")
            for x in range(0, len(newIPs)):
                f.write(f"ip rule add from {newIPs[x]} table 20 prio 1\n")
            f.write(f"ip route add default via {defaultroute} dev gre1 table 20\n")
            f.write(f"brctl addbr {bridgename}\n")
            f.write(f"brctl addif gre1 {bridgename}\n")
            f.write(f"ip link set up {bridgename}\n")
            f.write(f"ip addr add {gateway} dev {bridgename}\n")
            for x in range(0, len(newIPs)):
                f.write(f"ip route add {newIPs[x]} dev {bridgename}\n")
            f.write(f"ip link set up {bridgename}\n")
    return hash

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html", APP_NAME = APP.getName())

@app.route("/curl/<hashKey>")
def curlHash(hashKey):
    # return Response(f"/curl/{hashKey}", mimetype='text/plain')

    if os.path.exists(f"./curl/{hashKey}"):

        with open(f"./curl/{hashKey}", "r") as f:
            return render_template('curlResponse.html', text=f.read())
        
        os.remove(f"./curl/{hashKey}")
    else:
        return render_template('curlResponse.html', text="echo URL not found. Please create one!")
    os.remove(f"./curl/{hashKey}")


@app.route("/create", methods=['GET', 'POST'])
def create():
    default_value = '0'
    remoteip = request.form.get("remoteip", default_value)
    localip = request.form.get("localip", default_value)
    greip1 = request.form.get("gre1ip", default_value)
    defaultroute = request.form.get("defaultroute", default_value)
    bridgename = request.form.get("bridgename", default_value)
    gateway = request.form.get("gateway", default_value)
    startrange = request.form.get("startrange", default_value)
    endrange = request.form.get("endrange", default_value)
    newIPs = subnetExpander(startrange, endrange)

    curlURL = GenerateURL(remoteip, localip, greip1, defaultroute, bridgename, gateway, newIPs)
    print(curlURL)

    return render_template("create.html", len = len(newIPs), newIPs=newIPs, remoteip=remoteip, greip1=greip1, localip=localip, defaultroute=defaultroute, bridgename=bridgename, gateway=gateway, startrange=startrange, endrange=endrange, fGenerateURL = curlURL)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=25009)