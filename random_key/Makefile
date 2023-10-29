all: build shared

build:
	gcc -I /nix/store/sss6wmnvh82nyhf9024bdxgqi6k0ygm2-openssl-3.0.10-dev/include -L /nix/store/4iabmjjq95069myjsrid8pk2ib3yz4nn-openssl-3.0.10/lib generate_key.c -lcrypto -o generate_key
shared:
	gcc -I /nix/store/sss6wmnvh82nyhf9024bdxgqi6k0ygm2-openssl-3.0.10-dev/include -L /nix/store/4iabmjjq95069myjsrid8pk2ib3yz4nn-openssl-3.0.10/lib generate_key.c -lcrypto -shared -fPIC -o generate_key.so
