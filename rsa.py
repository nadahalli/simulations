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

def egcd(b, n):
    (x0, x1, y0, y1) = (1, 0, 0, 1)
    while n != 0:
        (q, b, n) = (b // n, n, b % n)
        (x0, x1) = (x1, x0 - q * x1)
        (y0, y1) = (y1, y0 - q * y1)
    return (b, x0, y0)

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
        if check:
            encrypted = encrypt_rsa(decrypted, public_key)
            print 'index     =', i
            print 'encrypted =', encrypted
            print 'decrypted =', decrypted
            decrypted2 = pow(seed, private_key['d']
            print '-' * 10
            assert(encrypted == seed)
        seed = decrypted

    print '#' * 10

    for i in range(n):
        e = public_key['e']
        f = pow(seed, (e - (i % e)) * e, n)
        print i, f

def wrap(f, *args, **kwargs):
    def wrapped():
        return f(*args, **kwargs)
    return wrapped

if __name__ == '__main__':
    p = number.getStrongPrime(512)
    q = number.getStrongPrime(512)
    p = 23
    q = 11
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

    print("RSA: ", timeit.timeit(wrap(test_rsa, 20, public_key, private_key, check = True), number=1))

    


