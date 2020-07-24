BLOCK_SIZE             = 64 * 1024 - 1
COMPRESS               = True

TABIX_FORMAT_NAME      = "TBI"
TABIX_EXTENSION        = '.tbi'
TABIX_MAGIC            = b'TBI\x01'
TABIX_FILE_BYTES_MASK  = 0xFFFFFFFFFFFFF0000
TABIX_BLOCK_BYTES_MASK = 0x0000000000000FFFF
TABIX_MAX_BIN          = (((1<<18)-1)//7)

TABIXPY_FORMAT_VER     = 5
TABIXPY_FORMAT_NAME    = "TBJ"
TABIXPY_EXTENSION      = '.tbj'

VCFBGZ_FORMAT_VER      = 1
VCFBGZ_FORMAT_NAME     = "TBK"
VCFBGZ_EXTENSION       = ".tbk"
VCFBGZ_EOF             = bytes.fromhex('000102030405060708090A0B0C0D0E0F')
