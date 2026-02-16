from cryptography.fernet import Fernet

with open("image.txt", "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Ejemplo de encriptado
config_data = {

    "mongo_credentials": {
        "username": "user_database",
        "password": "password",
        "host": "ip",
        "port": "27017",
        "authSource": "admin",
        "databases": ["local"]
    },
    "kafka_credentials": {
        "bootstrap.servers": "ip:9092",
        "acks": "all",
        "client.id": "name-topic-kafka"
    },
    "clickhouse_config": {
        'host': 'ip_database',
        'port': 8123,
        'user': 'admin',
        'password': 'password'
    },

    "consumer_config":  {
        'bootstrap.servers': 'ip:9092',
        'group.id': 'name_topic_kafka',
        'auto.offset.reset': 'earliest'
    },

}

encrypted_config = {}
for key, value in config_data.items():
    encrypted_config[key] = {
        k: cipher_suite.encrypt(str(v).encode()).decode()
        if isinstance(v, str) else v
        for k, v in value.items()
    }

with open("config.py", "w") as file:
    file.write(f"ENCRYPTED_CONFIG = {encrypted_config}")

print("Encrypted credentials saved to config.py.")
