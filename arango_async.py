#!/usr/bin/env python
from contextlib import asynccontextmanager
import logging
import os
from typing import Optional

from fastapi import FastAPI
from arango import ArangoClient
from starlette.responses import FileResponse


PATH = os.path.dirname(os.path.abspath(__file__))
#print("PATH",PATH)

app = FastAPI()
port = os.getenv("PORT", 8080)
client = ArangoClient(hosts='http://18.210.74.110:8529/')
db = client.db('urovant', username='root', password='dataaces')



@asynccontextmanager
async def get_db():
        yield db


@app.get("/")
async def get_index():
    return FileResponse(os.path.join(PATH, "static", "index.html"))


def serialize_payer(payer):
    #print(payer)
    return {
        "PAYER_ENTITY_ID": payer["PAYER_ENTITY_ID"],
        "BOB_ID": payer["BOB_ID"],
        "ENTERPRISE": payer["ENTERPRISE"],
        "ENTERPRISE_ID": payer["ENTERPRISE_ID"],
    }


def serialize_cast(cast):
    return {
        "name": cast[0],
        "job": cast[1],
        "role": cast[2]
    }



@app.get("/graph")
async def get_graph(limit: int = 100):
    async with get_db() as dbs:
        results = dbs.aql.execute("FOR s in L3_payer  RETURN s")
        nodes = []
        rels = []
        i=0
        for record in results:
            #print("record" , record["_key"])
            payer = {"title": record["PAYER_ENTITY_ID"], "label": "payer"}
            try:
                target = nodes.index(payer)
            except ValueError:
                nodes.append(payer)
                target = i
                i += 1
            #nodes.append({"title": record["PAYER_ENTITY_ID"], "label": "payer"})
            #target = i
            #i += 1
            #for id in record["payer_names"]:
            enterprise = {"title": record["ENTERPRISE_ID"], "label": "enterprise"}
            try:
                source = nodes.index(enterprise)
            except ValueError:
                nodes.append(enterprise)
                source = i
                i += 1
            rels.append({"source": source, "target": target})
            print("source:", source, "Destination",target)
        return {"nodes": nodes, "links": rels}
    
    
# @app.get("/graph")
# async def get_graph(limit: int = 100):
#     async with get_db() as dbs:
#         results = dbs.aql.execute("FOR s in L3_payer_under_enterprise RETURN s")
        #print("aaaaaaaa:", results)
        #print(type(results))
        # nodes = []
        # rels = []
        a=[]
        x=[]
        #m=[]
        # c=0
        # i=0
        # for record in results:
        #     a.append(record["_from"])
        #     #print("aaaaaaaaaa",a)
        # for r in a:
        #      if(r in x):
        #          k=x.index(r)
        #          print(record["_to"])
        #          m=map(x[k],record["_to"])
        #          #print("m",list(m))
        #      else:
        #          x.append(r)
        #          k=x.index(r)
        #          m=map(x[k],record["_to"])

        ar=[]
        m={}
        tolist=[]
        # for record in results:
        #     if(a is None):

        #         a.append(record["_from"])
        #     if(record["_from"] in a):
        #         k=a.index(record["_from"])
        #         #print(k)
        #         x=list(map(a[k],record["_to"]))
        #         print(x)
        #     else:
        #         a.append(record["_from"])
        #         k=a.index(record["_from"])
        #         x=list(map(a[k],record["_to"]))

        # for record in results:
        #     if not ar:
        #          tolist.append(record["_to"])
        #          m={record["_from"],tolist}
        #          ar.append(m)
        #     if(record["_from"] == k for k,v in m()):
        #          for(k,v in m()):
        #             if (k == record["_from"]):
                        

        #     ([])
            
        #     if()
            

        # print(next(ar))
        
        # for record in results:
        #     #print(record)
        #     print(type(record))
        # #     if(c==0):
        # #         x.append(record['_from'])
        # #         c=1
        #     a.append(record["_from"])
        #     print("frommm",a)
        #     for r in a:
        #         print("rrr",r)
        #         if(record["_from"] != r):
        #             x.append(r)
        #             print("x:",x)
        #             k=x.index(r)
        #             print("k:",k)
        #             m=map(x[k],record["_to"])

        #             print("m",m)
        #         else:
        #             k=x.index(r)
        #             m=map(x[k],record["_to"])
        #             print("m",m)
            #print("record" , record["_key"])
        #     nodes.append({"title": record["_from"], "label": "enterprise"})
        #     target = i
        #     i += 1
        #     #for id in record["payer_names"]:
        #     payer = {"title": record["_to"], "label": "payer"}
        #     try:
        #         source = nodes.index(payer)
        #     except ValueError:
        #         nodes.append(payer)
        #         source = i
        #         i += 1
        #     rels.append({"source": source, "target": target})
        # return {"nodes": nodes, "links": rels}
    #for record in results:
       
    
        # for r in results:
        #     a.append(r['_from'])
        # for r in results:
        #     if(r['_from'] in a):
        #         l.append(map(a,r['_to']))
        #     else:
        #         a.append(r['_from'])


        # z = a.length()
        # for x in a:
        #     if()
        #     l.append(map(a,r['_to']))


        #     if(r['_from'] in a):
        #         l.append(map(a,r['_to']))
        #     else:


@app.get("/search")
async def get_search(e: str = None, p: str = None):
    # print("length of q is "+len(q))
    # print("Enterprise is given as ")
    print(str(e)+" IS Enterprise and "+str(p)+" is Payer")
    if len(str(e)) == 0 and len(str(p)) == 0:
        print("Both e and p are None..")
        async with get_db() as dbs:
            results = dbs.aql.execute("FOR s in L3_payer RETURN s")
            return [serialize_payer(record) for record in results]
    elif len(str(e))>0 and len(str(p))==0:
        print("only p is None")
        async with get_db() as dbs:
            results = dbs.aql.execute("FOR s in L3_payer FILTER s.ENTERPRISE==@enterprise RETURN s",bind_vars={"enterprise":e})
            return [serialize_payer(record) for record in results]
    elif len(str(e))>0 and len(str(p))>0:
        print("both e and p are NOT none")
        async with get_db() as dbs:
            results = dbs.aql.execute("FOR s in L3_payer FILTER s.ENTERPRISE==@enterprise && s.PAYER_ENTITY_ID==@payer RETURN s",bind_vars={"enterprise":e, "payer":p})
            return [serialize_payer(record) for record in results]        

# @app.get("/payer/{name}")
# async def get_payer(name: str):
#     async def work(tx):
#         result_ = await tx.run(
#             "MATCH (payer:payer {name:$name}) "
#             "OPTIONAL MATCH (payer)<-[r]-(person:Person) "
#             "RETURN payer.title as title,"
#             "COLLECT([person.name, "
#             "HEAD(SPLIT(TOLOWER(TYPE(r)), '_')), r.roles]) AS cast "
#             "LIMIT 1",
#             {"title": title}
#         )
#         return await result_.single()

#     async with get_db() as db:
#         result = await db.execute_read(work)

#         return {"title": result["title"],
#                 "cast": [serialize_cast(member)
#                          for member in result["cast"]]}


# @app.post("/payer/{title}/vote")
# async def vote_in_payer(title: str):
#     async def work(tx):
#         result = await tx.run(
#             "MATCH (m:payer {title: $title}) "
#             "SET m.votes = coalesce(m.votes, 0) + 1;",
#             {"title": title})
#         return await result.consume()

#     async with get_db() as db:
#         summary = await db.execute_write(work)
#         updates = summary.counters.properties_set

#         return {"updates": updates}


if __name__ == "__main__":
    import uvicorn

    logging.root.setLevel(logging.INFO)
    logging.info("Starting on port %d, database is at %s", port, client)

    uvicorn.run(app, port=port)
