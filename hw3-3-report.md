# CS528 Assignment 3 — Problem 3: Implementing MPC using SFDL
**Author:** Akshitha Priyadarshini Murugan

**Course:** Data Security and Privacy  

**Instructor:** Binghui Wang  

**Date:** 2025-10-21

---

## 1. Protocol Design

We compute the scalar product of two private boolean vectors A and B of length 10 using Fairplay's
Secure Function Definition Language (SFDL) compiled to garbled circuits (SHDL). Alice supplies A,
Bob supplies B, and the circuit outputs the public integer \( \sum_i (A_i \wedge B_i) \).

**Security goal.** Neither party learns the other's inputs beyond what is implied by the final output.
The evaluation uses Yao's garbled circuits with semi-honest security as implemented by Fairplay.

**Functionality.** For each index i, compute \(c_i = A_i \wedge B_i\) and sum these ten bits.
Summation is performed on a 5-bit integer (max value = 10), preventing overflow.

---

## 2. Implementation Details

- **SFDL**: A single SFDL program (`hw3-3-dotprod.sfdl`) declares party-scoped inputs:
  `private boolean A[10]` for Alice and `private boolean B[10]` for Bob, and a `public int<5>` result.
  The program iterates over the 10 positions, accumulating `sum += (A[i] & B[i])`.
- **Compilation**: The SFDL is compiled by Fairplay into SHDL (a Boolean circuit) and then evaluated.
  The communication and two-party runtime are integrated in Fairplay.
- **I/O format**: Inputs are provided as 10 lines of `0`/`1` for each party. The output is a public 5-bit integer.
- **Correctness**: The circuit realizes the exact scalar product since boolean AND corresponds to bitwise multiplication.
- **Complexity**: The circuit uses 10 AND gates plus adders for the popcount (can be implemented as an increment-on-true).
  Fairplay handles the gate-level expansion during compilation.

---

## 3. Inputs and Outputs (Example)

Using the example vectors from the prompt:

- **Alice (A):** [1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
- **Bob (B):** [0, 1, 0, 0, 1, 1, 0, 1, 1, 1]
- **Output (A · B):** **5**

The sum is 5 because indices 1, 5, 6, 8, 9 have both bits equal to 1.

---

## 4. How to Run

1. Place `hw3-3-dotprod.sfdl` into your Fairplay source folder (e.g., `SFECompiler/`).
2. Compile SFDL to SHDL (see the project README for your version):
   ```bash
   ant compile -Dsfdl=hw3-3-dotprod.sfdl
   ```
3. Launch two parties (Alice = party 1, Bob = party 2) with their respective inputs as text files.
   Follow `hw3-3-readme.txt` for command examples.
4. The runtime prints the public result on completion.

---

## 5. Screenshots

Include screenshots of (a) compiling, (b) launching Alice and Bob, and (c) the final output.

---

## 6. Source Code
hw3-3-scalar_product.sfdl

"program ScalarProduct {
    type int4 = Int<4>;
    type AliceInput = Boolean[10];
    type BobInput = Boolean[10];
    type AliceOutput = int4;
    type BobOutput = int4;
    type Output = struct {AliceOutput alice, BobOutput bob};
    type Input = struct {AliceInput alice, BobInput bob};
    
    function Output output(Input input) {
        var Boolean b0, b1, b2, b3, b4, b5, b6, b7, b8, b9;
        var int4 result;
        
        b0 = input.alice[0] & input.bob[0];
        b1 = input.alice[1] & input.bob[1];
        b2 = input.alice[2] & input.bob[2];
        b3 = input.alice[3] & input.bob[3];
        b4 = input.alice[4] & input.bob[4];
        b5 = input.alice[5] & input.bob[5];
        b6 = input.alice[6] & input.bob[6];
        b7 = input.alice[7] & input.bob[7];
        b8 = input.alice[8] & input.bob[8];
        b9 = input.alice[9] & input.bob[9];
        
        result = 0;
        if (b0) result = result + 1;
        if (b1) result = result + 1;
        if (b2) result = result + 1;
        if (b3) result = result + 1;
        if (b4) result = result + 1;
        if (b5) result = result + 1;
        if (b6) result = result + 1;
        if (b7) result = result + 1;
        if (b8) result = result + 1;
        if (b9) result = result + 1;
        
        output.alice = result;
        output.bob = result;
    }
}

---

## 7. Discussion / Findings

- Garbled-circuit cost scales with input length; an adder tree can reduce depth versus incremental addition,
  but Fairplay's compiler already optimizes typical patterns.
- The result is intentionally public. If a private result is desired, declare it `private` to one or both parties.
- For larger vectors, ensure sufficient integer bitwidth to avoid overflow.

---

## 8. References

- Fairplay: Secure Function Evaluation Project (HUJI).