import asyncio
import websockets
import json
import os
import logging
##
import json
import asyncio
import websockets
import sys
import os

sys.path.append(r"pygundb/gundb/backends")
from backends.utils import defaultify
from backends import Memory, Mongo, Pickle, RedisKV, DummyKV, UDB
from backends.resolvers import is_reference, is_root_soul
sys.path.append(r"pygundb/gundb")
import gundb.gunrequesthandler
from gundb.utils import lex_from_graph, ham_mix, newuid, new_node
from gundb.consts import METADATA, STATE, SOUL
import os
import logging
import json
import uuid
def _init_backend(backend_db):
        print("backenddb var: ", backend_db)
        if backend_db == "mem":
            print("mem backend")
            backend = Memory()  # Pickle()
        elif backend_db == "mongo":
            print("mongo backend")
            backend = Mongo()
        elif backend_db == "pickle":
            print("pickle backend")
            backend = Pickle()
        elif backend_db == "redis":
            backend = RedisKV()
        elif backend_db == "dummy":
            backend = DummyKV()
        elif backend_db == "pickle":
            backend = Pickle()
        elif backend_db == "udb":
            backend = UDB()
        elif backend_db == "bcdb":
            try:
                from .backends import bcdb

                backend = bcdb.BCDB()
            except:
                backend = Memory()

        return backend

def emit(data):
        resp = json.dumps(data)
def _init_backend(backend_db):
        print("backenddb var: ", backend_db)
        if backend_db == "mem":
            print("mem backend")
            backend = Memory()  # Pickle()
        elif backend_db == "mongo":
            print("mongo backend")
            backend = Mongo()
        elif backend_db == "pickle":
            print("pickle backend")
            backend = Pickle()
        elif backend_db == "redis":
            backend = RedisKV()
        elif backend_db == "dummy":
            backend = DummyKV()
        elif backend_db == "pickle":
            backend = Pickle()
        elif backend_db == "udb":
            backend = UDB()
        else:
            backend = Memory()

        return backend

graph = {}
peers = []
trackedids = []
def push_diffs(diff):
        """
        Apply diff to reflect the changes in graph into the database.

        Diff are divided into reference updates and value updates.

        Reference updates are applied first then value updates.
        """
        ref_diff = defaultify({})
        val_diff = defaultify({})

        for soul, node in diff.items():
            ref_diff[soul][METADATA] = diff[soul][METADATA]
            for k, v in node.items():
                if k == METADATA:
                    continue
                if is_reference(v):
                    ref_diff[soul][k] = v
                else:
                    val_diff[soul][k] = v

        for soul, node in val_diff.items():
            for k, v in node.items():
                if k == METADATA or is_root_soul(k):
                    continue
                state = diff[soul][METADATA][STATE][k]
                backend.put(soul, k, v, state, graph)
        return graph
def trackid( id_):
        if id_ not in trackedids:
            trackedids.append(id_)
        return id_

def gun(ws):
    resp = {"ok": True}
    if ws is not None:
        msg = json.loads(ws)
        if not isinstance(msg, list):
            msg = [msg]
        overalldiff = defaultify({})
        for payload in msg:
            print(payload)
            if isinstance(payload, str):
                payload = json.loads(payload)
            if "put" in payload:
                change = payload["put"]
                msgid = payload["#"]
                diff = ham_mix(change, graph)
                uid = trackid(str(uuid.uuid4()))
                resp = {"@": msgid, "#": uid, "ok": True}
                print("DIFF:", diff)

                for soul, node in diff.items():
                    for k, v in diff[soul][METADATA].items():
                        if isinstance(v, dict):
                            overalldiff[soul][METADATA][k] = dict(
                                list(overalldiff[soul][METADATA][k].items()) + list(v.items())
                            )
                        else:
                            overalldiff[soul][METADATA][k] = v
                    for k, v in node.items():
                        if k == METADATA:
                            continue
                        overalldiff[soul][k] = v
            elif "get" in payload:
                uid = trackid(str(uuid.uuid4()))
                get = payload["get"]
                msgid = payload["#"]
                backend = _init_backend(ws)

                ack = lex_from_graph(get, backend)
                resp = {"put": ack, "@": msgid, "#": uid, "ok": True}
        push_diffs(overalldiff)
        emit(resp)
        emit(msg)



async def receive_data():
    async with websockets.connect('wss://prat.minfuel.com/gun') as websocket:
        while True:
            data = await websocket.recv()
            
            print(gun(data)) 
            data_json = json.loads(data)
            print(data_json)
            if "put" in data_json:
                # Do something with the new data
                print(data_json["put"])
                # Save the data to a local file
                with open("data.txt", "a") as f:
                    f.write(data_json["put"] + "\n")

async def main():
    await receive_data()

if __name__ == '__main__':
    asyncio.run(main())
