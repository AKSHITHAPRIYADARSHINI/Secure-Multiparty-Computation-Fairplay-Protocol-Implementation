Secure Multiparty Computation — Fairplay Protocol Implementation

This repository contains my implementation for a Secure Multiparty Computation (SMC) assignment using the Fairplay SFE framework and custom Python-based secure computation protocols.
The project demonstrates how private data from multiple parties can be jointly processed without revealing individual inputs, using both Fairplay (SFDL) and Python SMC workflows.

📘 Project Overview

This project explores different approaches to privacy-preserving computation:

1. Fairplay SFE (Secure Function Evaluation)

Fairplay enables two parties (Alice and Bob) to compute a function over private inputs using:

SFDL programs (*.sfdl)

Generated circuits and format files

Secure input files

Execution scripts (run_alice, run_bob)

Included Example:
✔ Secure Scalar Product Protocol
The Fairplay program securely computes the dot-product of Alice’s and Bob’s vectors without exposing their raw data.

2. Python Secure Multiparty Computation

Several Python scripts demonstrate SMC concepts without Fairplay:

hw3-4-demo.py – SMC workflow demonstration

hw3-4-smc-protocol.py – Custom implementation of a secure protocol

hw3-4-test-suite.py – Automated test suite for functionality

3. Reports

The repository includes detailed documentation:

Assignment 3 REPORT.pdf

hw3-3-report.md

hw3-4-report.pdf

These explain the design, execution, analysis, and results of the secure computation tasks.

📁 Folder Structure
HW3/
│
├── hw3-3-scalar_product.sfdl
├── hw3-3-alice.input
├── hw3-3-bob.input
├── hw3-3-matrix.txt
│
├── hw3-4-demo.py
├── hw3-4-smc-protocol.py
├── hw3-4-test-suite.py
│
├── Fairplay_Project/
│   ├── jars/
│   ├── run/
│   ├── progs/
│   ├── SFE_logcfg.lcf
│   └── ...
│
├── Assignment 3 REPORT.pdf
├── hw3-3-report.md
├── hw3-4-report.pdf
└── README.md

🚀 How to Run the Project
1. Running the Fairplay SFE Program (Secure Scalar Product)
Step 1: Navigate to the Fairplay run directory
cd Fairplay_Project/run

Step 2: Run Alice
./run_alice progs/hw3-3-scalar_product.sfdl.txt ../hw3-3-alice.input

Step 3: Run Bob

In another terminal:

./run_bob progs/hw3-3-scalar_product.sfdl.txt ../hw3-3-bob.input

Result

Both parties compute the scalar product without revealing their private vectors.

2. Running the Python SMC Protocol
Option A — Demonstration Script
python3 hw3-4-demo.py

Option B — Run the custom SMC protocol
python3 hw3-4-smc-protocol.py

Option C — Execute the test suite
python3 hw3-4-test-suite.py


These scripts simulate secure multiparty computation logic without Fairplay, focusing on protocol design and verification.

📌 Notes

Ensure Python 3.8+ is installed.

Fairplay scripts may require execution permissions:

chmod +x run_alice run_bob


Java may be required for certain Fairplay JAR executions.

📄 License

This project is intended for academic and educational purposes only.
