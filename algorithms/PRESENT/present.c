#include <string.h>
#include <stdint.h>
#include <stdio.h>
//#include <math.h>
#define CRYPTO_IN_SIZE  8 	// Present has 64-bit blocks
#define CRYPTO_KEY_SIZE 10  // Present has 80-bit key
#define CRYPTO_OUT_SIZE 8   // Present has 64-bit blocks

/**
 *  LUT of S-Box
 *
 */
static const uint8_t sbox[16] = {
	0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2,
};
/**
 * LUT of P-Box
 *
 */
static const uint8_t pbox[64] ={0 ,16,32,48,1 ,17,33,49,2 ,18,34,50,3 ,19,35,51,
         						4 ,20,36,52,5 ,21,37,53,6 ,22,38,54,7 ,23,39,55,
         						8 ,24,40,56,9 ,25,41,57,10,26,42,58,11,27,43,59,
         						12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63};
/**
 * The key is Xored with the plaintext.
 *
 * @param pt[] The array with the playtext
 * @param key[] The array with the key
 * @return void.
 **/
static void add_round_key(uint8_t pt[CRYPTO_IN_SIZE], uint8_t key[CRYPTO_KEY_SIZE])
{
	uint8_t i;
	for(i=0;i<8;i++){
		pt[i]= pt[i]^key[i];
	}
}
/**
 * Substitution Box is a non-linear mapping
 *
 *@param s The current state of the plaintext.
 *@return void.
 */
static void sbox_layer(uint8_t s[CRYPTO_IN_SIZE])
{
	uint8_t i,tmp;
	for(i=0;i<8;i++){
		tmp = sbox[s[i] & 0x0F];
		tmp |= sbox[(s[i]>>4)&0x0F]<<4;
		s[i] =tmp;
	}
}
/**
* Permutation Layer is a linear mapping providing
* difusion
*
*@param s The current state of the plaintext.
*@return void.
**/
static void pbox_layer(uint8_t s[CRYPTO_IN_SIZE])
{
	uint8_t i,tmp;
	uint8_t t[8] = {0};
	for(i=0;i<64;i++){
 		tmp= (s[i/8] >> (i%8)) &0x01;
 		t[pbox[i]/8]|= tmp << (pbox[i]%8);
		}

 	//Load values to s array
	for(i=0;i<8;i++){
		s[i]=t[i];
	}
}
static void update_round_key(uint8_t key[CRYPTO_KEY_SIZE], const uint8_t r)
{
	uint8_t tmp = 0;
	const uint8_t tmp2 = key[2];
	const uint8_t tmp1 = key[1];
	const uint8_t tmp0 = key[0];

	// rotate right by 19 bit
	key[0] = key[2] >> 3 | key[3] << 5;
	key[1] = key[3] >> 3 | key[4] << 5;
	key[2] = key[4] >> 3 | key[5] << 5;
	key[3] = key[5] >> 3 | key[6] << 5;
	key[4] = key[6] >> 3 | key[7] << 5;
	key[5] = key[7] >> 3 | key[8] << 5;
	key[6] = key[8] >> 3 | key[9] << 5;
	key[7] = key[9] >> 3 | tmp0 << 5;
	key[8] = tmp0 >> 3   | tmp1 << 5;
	key[9] = tmp1 >> 3   | tmp2 << 5;

	// perform sbox lookup on MSbits
	tmp = sbox[key[9] >> 4];
	key[9] &= 0x0F;
	key[9] |= tmp << 4;

	// XOR round counter k19 ... k15
	key[1] ^= r << 7;
	key[2] ^= r >> 1;
}

void crypto_func(uint8_t pt[CRYPTO_IN_SIZE], uint8_t key[CRYPTO_KEY_SIZE])
{
	uint8_t i = 0;

	for(i = 1; i <= 31; i++)
	{
		// Note +2 offset on key since output of keyschedule are upper 8 byte
		add_round_key(pt, key + 2);
		sbox_layer(pt);
		pbox_layer(pt);
		update_round_key(key, i);
	}

	// Note +2 offset on key since output of keyschedule are upper 8 byte
	add_round_key(pt, key + 2);

}

void main(void) {

    // message:  45 84 22 7B 38 C1 79 55
    uint8_t message[CRYPTO_IN_SIZE] = {0x45,0x84,0x22,0x7B,0x38,0xC1,0x79,0x55};
    // key: 3C F4 00 D8 28 F1 08 7A 60 26
    uint8_t key[CRYPTO_KEY_SIZE] = {0x3C,0xF4,0x00,0xD8,0x28,0xF1,0x08,0x7A,0x60,0x26};

    // before
    printf("Before:\t\t");
    for(uint8_t i = 0; i < CRYPTO_IN_SIZE; i++) { printf("%02x ", message[i]);}
    crypto_func(message, key);

    // after
    printf("\nAfter:\t\t");
    for(uint8_t i = 0; i < CRYPTO_IN_SIZE; i++) { printf("%02x ", message[i]);}

    // expected
    printf("\nExpected:\td0 44 6a 0a c9 13 35 d4\n");

}
