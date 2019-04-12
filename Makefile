client cli:
        ./redis-cli

start restart:
        ./redis-server redis.conf

stop:
        cat redis.pid | xargs kill

