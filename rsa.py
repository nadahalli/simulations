from Crypto.Util import number
import random
import sys
import timeit
import hashlib

sys.setrecursionlimit(1000000)

def gcd(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def encrypt_rsa(m, public_key):
    return pow(m, public_key['e'], public_key['n'])

def decrypt_rsa(c, private_key):
    return pow(c, private_key['d'], private_key['n'])

def test_rsa(n, public_key, private_key, check = True):
    seed = random.randrange(1, public_key['n'])
    print("RSA Seed: ", seed)
    for i in range(n):
        decrypted = decrypt_rsa(seed, private_key)
        print 'decrypted =', decrypted
        if check:
            encrypted = encrypt_rsa(decrypted, public_key)
            print 'encrypted =', encrypted
            print '-' * 10
            assert(encrypted == seed)
        seed = decrypted

def wrap(f, *args, **kwargs):
    def wrapped():
        return f(*args, **kwargs)
    return wrapped

if __name__ == '__main__':
    p = number.getStrongPrime(512)
    q = number.getStrongPrime(512)
    n = p * q
    phi = (p-1) * (q-1)/gcd(p-1, q-1)

    # e = random.randrange(1, phi)
    e = 3
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = modinv(e,phi)

    private_key = {'d': d, 'n': n}
    public_key = {'e': e, 'n': n}

    print("RSA: ", timeit.timeit(wrap(test_rsa, 10, public_key, private_key, check = True), number=1))

    


