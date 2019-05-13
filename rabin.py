import random
import sys
import timeit

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
    return pow(m, public_key[0], public_key[1])

def decrypt_rsa(c, private_key):
    return pow(c, private_key[0], private_key[1])

def test_rsa(n, public_key, private_key):
    seed = random.randrange(1, public_key[1])
    for i in range(n):
        decrypted = decrypt_rsa(seed, private_key)
        encrypted = encrypt_rsa(decrypted, public_key)
        assert(encrypted == seed)
        seed = decrypted

def sqrt_p_3_mod_4(a, p):
    r = pow(a, (p + 1) // 4, p)
    return r

def encrypt_rabin(m, public_key):
    return pow(m, 2, public_key[0])

def decrypt_rabin(m, private_key):
    p = private_key[0]
    q = private_key[1]
    n = private_key[2]
    
    r, s = 0, 0
    if p % 4 == 3:
        r = sqrt_p_3_mod_4(m, p)
    else:
        assert(False)
    if q % 4 == 3:
        s = sqrt_p_3_mod_4(m, q)
    else:
        assert(False)

    gcd, c, d = egcd(p, q)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]

    return lst[0]

def fast_x_power_2_power_k(x, k, p, q):
    t = pow(2, k, (p-1)*(q-1))
    return pow(x, t, p*q)

def test_rabin(m, public_key, private_key):
    x = random.randint(0, public_key[0])
    seed = fast_x_power_2_power_k(x, m, private_key[0], private_key[1])
    for i in range(m):
        decrypted = decrypt_rabin(seed, private_key)
        encrypted = encrypt_rabin(decrypted, public_key)
        assert(encrypted == seed)
        seed = decrypted

def wrap(f, *args, **kwargs):
    def wrapped():
        return f(*args, **kwargs)
    return wrapped

if __name__ == '__main__':
    p = 32416190071
    q = 32416188191
    n = p * q
    phi = (p-1) * (q-1)/gcd(p-1, q-1)

    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = modinv(e,phi)

    private_key = [d, n]
    public_key = [e, n]

    print("RSA: ", timeit.timeit(wrap(test_rsa, 10000, public_key, private_key), number=20))

    private_key = [p, q, p*q]
    public_key = [p*q]

    print("RABIN: ", timeit.timeit(wrap(test_rabin, 10000, public_key, private_key), number=20))

    


