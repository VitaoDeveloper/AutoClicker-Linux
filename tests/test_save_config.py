from app.config import load_config, save_config


config = load_config()

print("Antes:")
print(config)


config["interval"] = 0.5
config["amount"] = 10


save_config(config)


print("Depois:")
print(load_config())