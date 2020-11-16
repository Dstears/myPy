from redis import Redis

# 普通连接
conn = Redis(host="redis_ip", port=6379)
conn.set("x1", "hello world", ex=5)  # ex代表seconds，px代表ms
val = conn.get("x1")
print(val)
