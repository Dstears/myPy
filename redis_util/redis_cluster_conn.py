import rediscluster

conn = rediscluster.RedisCluster(
    startup_nodes=[
        {"host": "192.168.3.165", "port": "7000"},
        {"host": "192.168.3.165", "port": "8001"},
        {"host": "192.168.3.165", "port": "9000"},
        {"host": "192.168.3.165", "port": "9001"},
        {"host": "192.168.3.165", "port": "7001"},
        {"host": "192.168.3.165", "port": "8000"}
    ],
    decode_responses=True)

conn.set("x1", "hello world", ex=5)  # ex代表seconds，px代表ms
val = conn.get("x1")
print(val)
