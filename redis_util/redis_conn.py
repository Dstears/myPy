from redis import Redis

# 普通连接
conn = Redis(host="192.168.3.165", port=6379)
conn.set("x1", "hello world", ex=5)  # ex代表seconds，px代表ms
val = conn.get("x1")
print(val)
