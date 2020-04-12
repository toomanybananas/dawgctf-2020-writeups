#!/usr/bin/env python3
"""
solve-potentially-eazzzy.py
Author: chainsaw10

This is the script I used to develop the challenge. It's not pretty, nor is it
best practices for Python.

It does, however, show the intended solve of using z3.

More specifically, intended solve was:
    1. Notice it's a crackme with lots of constraints
    2. Wish I had written this in C so you could use angr (that's why I didn't)
    3. Dust off your copy of pyz3
    4. Define the constraints from the provided code in z3
        a. (You could copy-paste the "m" function and make it manufacture
        constraints with a bit of work, that could save time, idk if anyone
        did.)
    5. Give z3 an email address.
    6. Ask z3 to solve for key
    7. ???
    8. Profit!

This was what I had, there are almost certainly easier ways of doing it.
"""

import functools
import itertools

import z3


# Define our allowed alphabet for things
ALPHABET = [chr(i) for i in range(ord("*"), ord("z")+1)]


class Z3String:
    """z3 doesn't have a native string type, so I made a lame one here

    I'm told there are better ones out there, but I wanted to just whip one up
    """
    def __init__(self, name, length):
        self.bitvecs = [ z3.Int("%s_%d" % (name, i)) for i in range(length) ]

    def __getitem__(self, key):
        """This makes key[index] work"""
        return self.bitvecs[key]

    def add_equal_to(self, s, realstr):
        if len(realstr) != len(self.bitvecs):
            raise Exception("lengths must be the same for add_equal_to")
        for i, j in zip(self.bitvecs, realstr):
            s.add(i == ord(j))

    def add_equal_to_padded(self, s, padchar, realstr):
        realstr = realstr.ljust(len(self.bitvecs), padchar)
        if len(realstr) != len(self.bitvecs):
            raise Exception("lengths must be the same for add_equal_to")
        for i, j in zip(self.bitvecs, realstr):
            s.add(i == ord(j))

    def expr_count_of(self, char):
        """Counts char in string, returns expression.
        
        Returns a z3 expression representing the number of times char appears in
        the string.
        """
        return (z3.Sum([ z3.If(bv == ord(char), 1, 0) for bv in self.bitvecs ]))

    def resolve_from_model(self, model):
        resolved = ""
        for bv in self.bitvecs:
            interp = model.get_interp(bv)
            if interp is not None and interp.as_long() != 0:
                resolved += chr(interp.as_long())
            else:
                resolved += "<%s>" % (bv)

        return resolved

    def __iter__(self):
        """This makes for char in key work"""
        return self.bitvecs.__iter__()

    def __len__(self):
        """Makes len(email) work
        
        Not sure I actually used this anywhere.
        """
        return len(self.bitvecs)

    def index(self, char):
        """This doesn't actually do what the name suggests it does, oops"""
        return (z3.Sum([
            z3.If(bv == ord(char), idx, 0) for idx, bv in
            enumerate(self.bitvecs)]))

    def sum(self):
        return z3.Sum(self.bitvecs)


def alpha(num):
    """Make a value that's within ALPHABET from provided num"""
    return ord(ALPHABET[0]) + (num % len(ALPHABET))


def combine(s, emailchar, key1, key2, value):
    """Make a constraint that is based on the provided values"""
    mod = len(ALPHABET)//2
    start = ord(ALPHABET[0])
    s1, s2, s3 = emailchar - start, key1 - start, key2 - start
    s.add((s1 + s2 + s3) % mod == value%mod)


def validate_reg_key(s, email, regkey):
    """Add constraints for email and regkey
    
    s here is the z3 Solver object. You add constraints to the solver, then ask
    it to... well... solve.
    """
    # make sure it's printable, and in a sane range
    for bv in itertools.chain(email, regkey):
       s.add(bv >= ord(ALPHABET[0]))
       s.add(bv <= ord(ALPHABET[-1]))

    # There's got to be an at-sign, of course
    s.add(email.expr_count_of("@") == 1)

    # regkey must start with "Z"
    s.add(regkey[0] == ord("Z"))

    # fun with dots
    dotcount = email.expr_count_of(".")
    s.add(dotcount >= 0)
    s.add(dotcount < len(ALPHABET))
    s.add(regkey[1] == alpha(dotcount))

    # length
    s.add(regkey[2] == alpha(email.index("*") + 7))

    # Eh, let's make 3 based on 1 and 2
    s.add(regkey[3] == alpha(regkey[1]%30 + regkey[2]%30) + 5)

    # Summing the email seems fun
    s.add(regkey[4] == alpha(email.sum()%60 + regkey[5]))

    # Eh, waste some bytes
    s.add(regkey[5] == alpha(regkey[3] + 52))
    s.add(regkey[6] == alpha( (regkey[7] % 8) * 2) )
    s.add(regkey[7] == alpha(regkey[1] + regkey[2] - regkey[3]))
    s.add(regkey[8] == alpha( (regkey[6] % 16) / 2) )

    s.add(regkey[9] == alpha(regkey[6] + regkey[4] + regkey[8] - 4))

    s.add(regkey[10] == alpha(z3.Sum([
        (regkey[1] % 2) * 8,
        regkey[2] % 3,
        regkey[3] % 4,
    ])))

    # Here's where I got bored of making up new conditions
    combine(s, email[3], regkey[11], regkey[12], 8)
    combine(s, email[7], regkey[13], regkey[4], 18)
    combine(s, email[9], regkey[14], regkey[3], 23)
    combine(s, email[10], regkey[15], regkey[10], 3)
    combine(s, email[11], regkey[13], regkey[16], 792)
    combine(s, email[12], regkey[17], regkey[4], email.expr_count_of("d"))
    combine(s, email[13], regkey[18], regkey[7], email.expr_count_of("a"))
    combine(s, email[14], regkey[19], regkey[8], email.expr_count_of("w"))
    combine(s, email[15], regkey[20], regkey[1], email.expr_count_of("g"))
    combine(s, email[16], email[17], regkey[21], email.expr_count_of("s"))
    combine(s, email[18], email[19], regkey[22], email.expr_count_of("m"))
    combine(s, email[20], regkey[23], regkey[17], 9)
    combine(s, email[21], regkey[24], regkey[13], 41)
    combine(s, email[22], regkey[25], regkey[10], 3)
    combine(s, email[23], regkey[26], email[14], email.expr_count_of("1"))
    combine(s, email[24], email[25], regkey[27], email.expr_count_of("*"))
    combine(s, email[26], email[27], regkey[28], 7)
    combine(s, email[28], email[29], regkey[29], 2)
    combine(s, email[30], regkey[30], email[18], 4)
    combine(s, email[31], regkey[31], email[4], 7)


def check(email_in):
    s = z3.Solver()

    # So the flow here is we make a symbolic value for email and regkey
    # Then we're going to define constraints on those values and let z3 find a
    # valid key
    email = Z3String("email", 32) # We'll pad out to 32 chars if not I guess
    regkey = Z3String("regkey", 32) # 32 bytes seems enough

    # Here's where we set the email we want a key for
    email.add_equal_to_padded(s, "*", email_in)

    # Now we add the constraints
    validate_reg_key(s, email, regkey)

    #print(s.sexpr())

    # Ask z3 if the constraints are satisfiable
    chk = s.check()
    print(chk)
    if chk != z3.sat:
        return
    # If the constraints were satisfiable, ask z3 to find concrete values that
    # satisfy them
    m = s.model()
    #print(m)
    # Now print them out nicely to go paste into the challenge
    print("email:", email.resolve_from_model(m).strip("*"))
    print("regkey:", regkey.resolve_from_model(m))


def main():
    print("Alphabet length is:", hex(len(ALPHABET)), len(ALPHABET))

    check("lol@helloworldthere.com.net.org")
    check("info@umbccd.io")
    check("a@a")


if __name__ == "__main__":
    main()
