# Pyrogram Switcher Publisher

Run in docker:

```bash
docker run -it --rm -v switcher-config:/config -p 20002:20002/udp yossiok/pyro-switcher
```

or 
```bash
docker run -it --name pyrosw -v switcher-config:/config -p 20002:20002/udp yossiok/pyro-switcher
```

## TODO:
- Separate Telgram client and Switcher listener
- Check `users.yaml` and `config.ini` before start
- Fill `users.yaml` by sending telegram message