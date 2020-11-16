import rediscluster

host = "192.168.9.241"
conn = rediscluster.RedisCluster(
    startup_nodes=[
        {"host": host, "port": "7000"},
        {"host": host, "port": "8001"},
        {"host": host, "port": "9000"},
        {"host": host, "port": "9001"},
        {"host": host, "port": "7001"},
        {"host": host, "port": "8000"}
    ],
    decode_responses=True)

conn.set("x1", "hello world", ex=5)  # ex代表seconds，px代表ms
val = conn.get("x1")
print(val)
