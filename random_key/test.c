#include <stdlib.h>
#include <openssl/md5.h>

int main() {
    MD5_CTX ctx;
    MD5_Init(&ctx);
    return 0;
}
