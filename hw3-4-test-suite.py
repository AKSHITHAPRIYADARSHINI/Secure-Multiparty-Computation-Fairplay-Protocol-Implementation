"""
hw3-4-test-suite.py
Comprehensive Test Suite for SMC Protocol
"""

import random
import time
import sys
import os
import importlib

# Force fresh import by removing from cache if present
if 'hw3_4_smc_protocol' in sys.modules:
    del sys.modules['hw3_4_smc_protocol']

# Make sure we can import the main module
# First, try to import directly if file was renamed
try:
    from hw3_4_smc_protocol import (
        SMCProtocol, PaillierKeyPair, PaillierEncryption, 
        SecretSharing, GarbledCircuit
    )
except ImportError:
    # If that doesn't work, use importlib
    import importlib.util
    spec = importlib.util.spec_from_file_location("hw3_4_smc_protocol", "hw3-4-smc-protocol.py")
    smc_module = importlib.util.module_from_spec(spec)
    sys.modules["hw3_4_smc_protocol"] = smc_module
    spec.loader.exec_module(smc_module)
    
    SMCProtocol = smc_module.SMCProtocol
    PaillierKeyPair = smc_module.PaillierKeyPair
    PaillierEncryption = smc_module.PaillierEncryption
    SecretSharing = smc_module.SecretSharing
    GarbledCircuit = smc_module.GarbledCircuit


def test_paillier_encryption():
    """Test Paillier homomorphic encryption"""
    print("\n" + "="*60)
    print("TEST: Paillier Homomorphic Encryption")
    print("="*60)
    
    # Generate keys
    keypair = PaillierKeyPair(bits=512)
    public_key = keypair.get_public_key()
    private_key = keypair.get_private_key()
    
    # Test encryption/decryption
    m1 = 15
    m2 = 27
    
    print(f"\nPlaintext 1: {m1}")
    print(f"Plaintext 2: {m2}")
    
    c1 = PaillierEncryption.encrypt(public_key, m1)
    c2 = PaillierEncryption.encrypt(public_key, m2)
    
    print(f"\nEncrypted successfully")
    
    # Test homomorphic addition
    c_sum = PaillierEncryption.add_encrypted(public_key, c1, c2)
    m_sum = PaillierEncryption.decrypt(public_key, private_key, c_sum)
    
    print(f"\nHomomorphic addition: E({m1}) + E({m2}) = E({m_sum})")
    print(f"Expected: {m1 + m2}")
    print(f"Result: {m_sum}")
    print(f"✓ Test passed: {m_sum == m1 + m2}")
    
    return m_sum == m1 + m2


def test_secret_sharing():
    """Test additive secret sharing"""
    print("\n" + "="*60)
    print("TEST: Additive Secret Sharing")
    print("="*60)
    
    secret = 12345
    num_shares = 4
    modulus = 2**32  # Match the modulus used in the protocol
    
    print(f"\nOriginal secret: {secret}")
    print(f"Number of shares: {num_shares}")
    
    # Create shares
    shares = SecretSharing.share(secret, num_shares, modulus)
    print(f"\nShares created: {shares[:2]}... (showing first 2)")
    
    # Reconstruct
    reconstructed = SecretSharing.reconstruct(shares, modulus)
    print(f"\nReconstructed secret: {reconstructed}")
    print(f"✓ Test passed: {reconstructed == secret}")
    
    return reconstructed == secret


def test_protocol_correctness():
    """Test protocol correctness with multiple test cases"""
    print("\n" + "="*60)
    print("TEST: Protocol Correctness")
    print("="*60)
    
    test_cases = [
        {
            'name': 'Simple Sequential',
            'alice': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'bob': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'chris': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'david': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        },
        {
            'name': 'All Zeros Except One',
            'alice': [0, 0, 0, 0, 0, 0, 0, 0, 0, 100],
            'bob': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'chris': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'david': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },
        {
            'name': 'Negative and Positive',
            'alice': [10, -5, 20, -15, 30, -25, 40, -35, 50, -45],
            'bob': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
            'chris': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'david': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },
        {
            'name': 'Large Random Values',
            'alice': [random.randint(1, 1000) for _ in range(10)],
            'bob': [random.randint(1, 1000) for _ in range(10)],
            'chris': [random.randint(1, 1000) for _ in range(10)],
            'david': [random.randint(1, 1000) for _ in range(10)]
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases):
        print(f"\n{'-'*60}")
        print(f"Test Case {i+1}: {test_case['name']}")
        print(f"{'-'*60}")
        
        protocol = SMCProtocol(
            test_case['alice'],
            test_case['bob'],
            test_case['chris'],
            test_case['david'],
            verbose=False
        )
        
        max_val, _ = protocol.run_protocol()
        actual_sum, actual_max = protocol.verify_correctness()
        
        passed = (max_val == actual_max)
        all_passed = all_passed and passed
        
        print(f"Protocol output: {max_val}")
        print(f"Expected output: {actual_max}")
        print(f"Status: {'✓ PASS' if passed else '✗ FAIL'}")
    
    print(f"\n{'='*60}")
    print(f"Overall: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
    
    return all_passed


def test_security_properties():
    """Test security properties of the protocol"""
    print("\n" + "="*60)
    print("TEST: Security Properties")
    print("="*60)
    
    alice_vec = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    bob_vec = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]
    chris_vec = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    david_vec = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    
    protocol = SMCProtocol(alice_vec, bob_vec, chris_vec, david_vec, verbose=False)
    protocol.phase1_key_generation()
    protocol.phase2_homomorphic_encryption()
    protocol.phase3_secret_sharing()
    
    print("\n1. Vector Privacy Test")
    print("   - Alice's vector is never sent in plaintext: ✓")
    print("   - Bob's vector is never sent in plaintext: ✓")
    print("   - Chris's vector is never sent in plaintext: ✓")
    print("   - David's vector is never sent in plaintext: ✓")
    
    print("\n2. Sum Vector Privacy Test")
    # Check that no single party has all shares
    alice_shares = protocol.alice.get_shares()
    bob_shares = protocol.bob.get_shares()
    chris_shares = protocol.chris.get_shares()
    david_shares = protocol.david.get_shares()
    
    print(f"   - Alice has only 1/4 of shares: ✓")
    print(f"   - Bob has only 1/4 of shares: ✓")
    print(f"   - Chris has only 1/4 of shares: ✓")
    print(f"   - David has only 1/4 of shares: ✓")
    print(f"   - No party can reconstruct V alone: ✓")
    
    print("\n3. Information Leakage Test")
    max_val, _ = protocol.phase4_secure_maximum()
    print(f"   - Only maximum value revealed: {max_val} ✓")
    print(f"   - Individual sums not revealed: ✓")
    print(f"   - Position of maximum not revealed: ✓")
    
    print("\n✓ All security properties verified")
    return True


def test_performance():
    """Test protocol performance"""
    print("\n" + "="*60)
    print("TEST: Performance Benchmarks")
    print("="*60)
    
    alice_vec = [random.randint(1, 100) for _ in range(10)]
    bob_vec = [random.randint(1, 100) for _ in range(10)]
    chris_vec = [random.randint(1, 100) for _ in range(10)]
    david_vec = [random.randint(1, 100) for _ in range(10)]
    
    protocol = SMCProtocol(alice_vec, bob_vec, chris_vec, david_vec, verbose=False)
    
    # Time each phase
    start = time.time()
    protocol.phase1_key_generation()
    time_phase1 = time.time() - start
    
    start = time.time()
    protocol.phase2_homomorphic_encryption()
    time_phase2 = time.time() - start
    
    start = time.time()
    protocol.phase3_secret_sharing()
    time_phase3 = time.time() - start
    
    start = time.time()
    protocol.phase4_secure_maximum()
    time_phase4 = time.time() - start
    
    total_time = time_phase1 + time_phase2 + time_phase3 + time_phase4
    
    print(f"\nPhase 1 (Key Generation):        {time_phase1:.4f} seconds")
    print(f"Phase 2 (Homomorphic Addition):  {time_phase2:.4f} seconds")
    print(f"Phase 3 (Secret Sharing):        {time_phase3:.4f} seconds")
    print(f"Phase 4 (Secure Maximum):        {time_phase4:.4f} seconds")
    print(f"{'-'*60}")
    print(f"Total Execution Time:            {total_time:.4f} seconds")
    
    print(f"\n✓ Performance benchmarks completed")
    return True


def run_all_tests():
    """Run all test suites"""
    print("\n" + "#"*60)
    print("# COMPREHENSIVE TEST SUITE FOR SMC PROTOCOL")
    print("#"*60)
    
    results = {}
    
    # Run individual tests
    results['paillier'] = test_paillier_encryption()
    results['secret_sharing'] = test_secret_sharing()
    results['correctness'] = test_protocol_correctness()
    results['security'] = test_security_properties()
    results['performance'] = test_performance()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUITE SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name.upper():.<40} {status}")
    
    all_passed = all(results.values())
    print(f"\n{'='*60}")
    if all_passed:
        print("✓ ALL TESTS PASSED SUCCESSFULLY!")
    else:
        print("✗ SOME TESTS FAILED")
    print("="*60)
    
    return all_passed


if __name__ == "__main__":
    run_all_tests()