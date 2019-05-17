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

def test_rsa(n, public_key, private_key, check = True):
    seed = random.randrange(1, public_key[1])
    print("RSA Seed: ", seed)
    for i in range(n):
        decrypted = decrypt_rsa(seed, private_key)
        if check:
            encrypted = encrypt_rsa(decrypted, public_key)
            assert(encrypted == seed)
        seed = decrypted

def sqrt_p_3_mod_4(a, p):
    r = pow(a, (p + 1) // 4, p)
    return r

def encrypt_rabin(m, public_key):
    return pow(m, 2, public_key[0])

def decrypt_rabin(m, private_key):
    p = private_key['p']
    q = private_key['q']
    n = private_key['n']
    
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

def generate_rabin(x, i, private_key):
    p = private_key['p']
    q = private_key['q']
    n = private_key['n']
    tot = private_key['tot']
    power = pow(2, i, tot)
    return pow(x, pow(2, i, tot), n)

def test_rabin(m, public_key, private_key, check = True):
    x = random.randint(0, public_key[0])
    print("Rabin Seed: ", x)
    seed = generate_rabin(x, m, private_key)
    for i in range(m):
        decrypted = decrypt_rabin(seed, private_key)
        if check:
            encrypted = encrypt_rabin(decrypted, public_key)
            assert(encrypted == seed)
        seed = decrypted

def test_rabin_series1(m, public_key, private_key, check = True):
    x = random.randint(0, public_key[0])
    print("Rabin Series Seed: ", x)
    for i in range(m):
        decrypted = generate_rabin(x, m - i, private_key)
        if check:
            encrypted_using_series = generate_rabin(x, m - i + 1, private_key)
            encrypted_using_standard = encrypt_rabin(decrypted, public_key)
            assert(encrypted_using_standard == encrypted_using_series)

class ReverseRabin:
    def __init__(self, m, private_key):
        self.prev_power = pow(2, m, private_key['tot'])

    def reverse(self, x, private_key):
        tot = private_key['tot']
        t = private_key['t']
        n = private_key['n']
        reversed = pow(x, self.prev_power, n)
        self.prev_power = (self.prev_power * t) % tot
        return reversed

def test_rabin_series2(m, public_key, private_key, check = True):
    rr = ReverseRabin(m , private_key)
    x = random.randint(0, public_key[0])
    print("Rabin Series Seed: ", x)
    end = rr.reverse(x, private_key)
    for i in range(m):
        decrypted = rr.reverse(x, private_key)
        if check:
            encrypted_using_series = generate_rabin(x, m - i, private_key)
            encrypted_using_standard = encrypt_rabin(decrypted, public_key)
            assert(encrypted_using_standard == encrypted_using_series)

def find_k(tot):
    while tot % 2 == 0:
        tot = tot/2
    return tot
            
def wrap(f, *args, **kwargs):
    def wrapped():
        return f(*args, **kwargs)
    return wrapped

if __name__ == '__main__':
    p = 298840311595359989218162782863818299419
    q = 257876331596501287971460799759063789759
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

    print("RSA: ", timeit.timeit(wrap(test_rsa, 10000, public_key, private_key, check = False), number=2))

    n = p * q
    tot = (p-1) * (q-1)
    k = find_k(tot)
    t = modinv(2, k)
    assert((2 * t) % k == 1)
    private_key = {'p': p, 'q': q, 'n': n, 'tot': tot, 't': t}
    public_key = [n]

    print("RABIN: ", timeit.timeit(wrap(test_rabin, 10000, public_key, private_key, check = False), number=2))
    print("RABIN SERIES1: ", timeit.timeit(wrap(test_rabin_series1, 10000, public_key, private_key, check = False), number=2))
    print("RABIN SERIES2: ", timeit.timeit(wrap(test_rabin_series2, 10000, public_key, private_key, check = False), number=2))

    


