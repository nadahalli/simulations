def sqrt_p_3_mod_4(a, p):
    r = pow(a, (p + 1) // 4, p)
    return r

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, y, x = egcd(b % a, a)
        return gcd, x - (b // a) * y, y


def encryption(plaintext, n):
    return plaintext ** 2 % n


def decryption(a, p, q):
    n = p * q
    r, s = 0, 0
    if p % 4 == 3:
        r = sqrt_p_3_mod_4(a, p)
    else:
        assert(False)
    if q % 4 == 3:
        s = sqrt_p_3_mod_4(a, q)
    else:
        assert(False)

    gcd, c, d = egcd(p, q)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]

    return lst

def check(x, p , q):
    step = 0
    for i in range(10):
        step += 1
        dall = decryption(x, p, q)
        d = dall[0]
        e = encryption(d, p * q)
        if e != x:
            if step > 1:
                return False
        x = d
    return True

if __name__ == '__main__':
    p = 32416190071
    q = 32416188191	

    print p % 4
    print q % 4

    k = 10
    x = 3 ** (2 ** k) % (p*q)

    for i in range(1000):
        print check(x - i, p, q)
