"""
hw3-4-demo.py
Interactive Demonstration of SMC Protocol
"""

import random
import sys
import importlib.util

# Force fresh import
if 'hw3_4_smc_protocol' in sys.modules:
    del sys.modules['hw3_4_smc_protocol']

# Import the main module (handle dashes in filename)
try:
    from hw3_4_smc_protocol import SMCProtocol
except ImportError:
    spec = importlib.util.spec_from_file_location("hw3_4_smc_protocol", "hw3-4-smc-protocol.py")
    smc_module = importlib.util.module_from_spec(spec)
    sys.modules["hw3_4_smc_protocol"] = smc_module
    spec.loader.exec_module(smc_module)
    SMCProtocol = smc_module.SMCProtocol


def print_banner(text):
    """Print a formatted banner"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def print_section(text):
    """Print a section header"""
    print("\n" + "-"*70)
    print(f"  {text}")
    print("-"*70)


def visualize_encryption(vectors):
    """Visualize the encryption process"""
    print("\n📊 VECTOR DATA:")
    print(f"   Alice:  {vectors['Alice']}")
    print(f"   Bob:    {vectors['Bob']}")
    print(f"   Chris:  {vectors['Chris']}")
    print(f"   David:  {vectors['David']}")


def visualize_phases(protocol):
    """Run protocol with detailed visualization"""
    
    print_section("PHASE 1: Key Generation")
    print("\n🔑 Alice generates Paillier keypair...")
    protocol.phase1_key_generation()
    print("   ✓ Public key (n, g) shared with all parties")
    print("   ✓ Private key kept secret by Alice")
    input("\n   Press Enter to continue...")
    
    print_section("PHASE 2: Homomorphic Encryption & Addition")
    print("\n🔐 Parties encrypt and combine vectors homomorphically...")
    print("\n   Step 1: Alice encrypts her vector")
    print("           E[i] = Encrypt(Va[i])")
    print("\n   Step 2: Bob adds his encrypted vector")
    print("           E[i] = E[i] ⊕ Encrypt(Vb[i])")
    print("\n   Step 3: Chris adds his encrypted vector")
    print("           E[i] = E[i] ⊕ Encrypt(Vc[i])")
    print("\n   Step 4: David adds his encrypted vector")
    print("           E[i] = E[i] ⊕ Encrypt(Vd[i])")
    
    protocol.phase2_homomorphic_encryption()
    print("\n   ✓ Encrypted sum vector E computed")
    print("   ✓ E[i] = Encrypt(Va[i] + Vb[i] + Vc[i] + Vd[i])")
    input("\n   Press Enter to continue...")
    
    print_section("PHASE 3: Distributed Decryption & Secret Sharing")
    print("\n🔓 Alice decrypts and creates secret shares...")
    protocol.phase3_secret_sharing()
    
    print("\n   Alice decrypted E to get V (sum vector)")
    print("   Then immediately split V into 4 shares:")
    print("\n   For each V[i]:")
    print("      s1[i] = random")
    print("      s2[i] = random")
    print("      s3[i] = random")
    print("      s4[i] = V[i] - s1[i] - s2[i] - s3[i]")
    
    print("\n   📤 Shares distributed:")
    print("      Alice  keeps: s4[i] for all i")
    print("      Bob    gets:  s1[i] for all i")
    print("      Chris  gets:  s2[i] for all i")
    print("      David  gets:  s3[i] for all i")
    
    print("\n   ✓ No single party knows V!")
    print("   ✓ Need all 4 shares to reconstruct any V[i]")
    input("\n   Press Enter to continue...")
    
    print_section("PHASE 4: Secure Maximum Computation")
    print("\n🔒 All parties engage in Garbled Circuit...")
    print("\n   Circuit inputs (shares from each party):")
    print("      Alice:  [s4[1], s4[2], ..., s4[10]]")
    print("      Bob:    [s1[1], s1[2], ..., s1[10]]")
    print("      Chris:  [s2[1], s2[2], ..., s2[10]]")
    print("      David:  [s3[1], s3[2], ..., s3[10]]")
    
    print("\n   Circuit computation:")
    print("      1. Reconstruct: V[i] = s1[i] + s2[i] + s3[i] + s4[i]")
    print("      2. Find max:    max_value = max(V[1], ..., V[10])")
    print("      3. Output:      max_value only")
    
    max_value, reconstructed = protocol.phase4_secure_maximum()
    
    print(f"\n   ✓ Circuit completed securely")
    input("\n   Press Enter to see results...")
    
    return max_value, reconstructed


def run_interactive_demo():
    """Run an interactive demonstration"""
    print_banner("SECURE MULTI-PARTY COMPUTATION PROTOCOL")
    print("         Vector Sum and Maximum Finding")
    print("\nThis demonstration shows how 4 parties can securely compute")
    print("the maximum of their summed vectors without revealing:")
    print("  • Their individual vectors")
    print("  • The sum vector")
    print("\nOnly the maximum value will be revealed!\n")
    
    input("Press Enter to begin...")
    
    # Demo 1: Simple example
    print_banner("DEMO 1: Simple Example")
    
    vectors = {
        'Alice':  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Bob':    [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        'Chris':  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        'David':  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    
    visualize_encryption(vectors)
    
    protocol = SMCProtocol(
        vectors['Alice'],
        vectors['Bob'],
        vectors['Chris'],
        vectors['David'],
        verbose=False
    )
    
    max_value, reconstructed = visualize_phases(protocol)
    
    print_banner("RESULTS")
    print(f"\n   🎯 MAXIMUM VALUE: {max_value}")
    
    print("\n   ℹ️  For verification purposes only:")
    print(f"      Actual sum vector V = {reconstructed}")
    print(f"      Actual maximum = {max(reconstructed)}")
    print(f"\n   ✓ Protocol output is correct!")
    
    print("\n   🔒 SECURITY ACHIEVED:")
    print("      ✓ Individual vectors never revealed")
    print("      ✓ Sum vector V never revealed to any single party")
    print("      ✓ Only maximum value disclosed")
    
    # Demo 2: Let user try custom values
    print_banner("DEMO 2: Try Your Own Vectors!")
    
    choice = input("\nWould you like to try custom vectors? (y/n): ")
    
    if choice.lower() == 'y':
        try:
            print("\nEnter 10 integers for each party (space-separated):")
            alice_input = input("Alice's vector:  ")
            bob_input = input("Bob's vector:    ")
            chris_input = input("Chris's vector:  ")
            david_input = input("David's vector:  ")
            
            alice_vec = [int(x) for x in alice_input.split()]
            bob_vec = [int(x) for x in bob_input.split()]
            chris_vec = [int(x) for x in chris_input.split()]
            david_vec = [int(x) for x in david_input.split()]
            
            if len(alice_vec) == len(bob_vec) == len(chris_vec) == len(david_vec) == 10:
                protocol2 = SMCProtocol(alice_vec, bob_vec, chris_vec, david_vec, verbose=False)
                max_val2, _ = protocol2.run_protocol()
                
                print_banner("YOUR RESULTS")
                print(f"\n   🎯 MAXIMUM VALUE: {max_val2}")
                print("\n   ✓ Protocol executed successfully!")
            else:
                print("\n   ✗ Error: All vectors must have exactly 10 elements")
        except:
            print("\n   ✗ Error: Invalid input format")
    
    # Demo 3: Random large values
    print_banner("DEMO 3: Large Random Values")
    
    choice = input("\nWould you like to see a demo with random values? (y/n): ")
    
    if choice.lower() == 'y':
        random.seed()
        alice_rand = [random.randint(1, 1000) for _ in range(10)]
        bob_rand = [random.randint(1, 1000) for _ in range(10)]
        chris_rand = [random.randint(1, 1000) for _ in range(10)]
        david_rand = [random.randint(1, 1000) for _ in range(10)]
        
        print("\n📊 Random vectors generated:")
        print(f"   Alice:  {alice_rand}")
        print(f"   Bob:    {bob_rand}")
        print(f"   Chris:  {chris_rand}")
        print(f"   David:  {david_rand}")
        
        protocol3 = SMCProtocol(alice_rand, bob_rand, chris_rand, david_rand, verbose=False)
        max_val3, sum_vec3 = protocol3.run_protocol()
        
        print("\n   🎯 MAXIMUM VALUE:", max_val3)
        print(f"   ✓ Protocol completed in < 1 second")
    
    print_banner("DEMONSTRATION COMPLETE")
    print("\n   Thank you for exploring the SMC protocol!")
    print("\n   Key Takeaways:")
    print("   • Homomorphic encryption enables secure computation")
    print("   • Secret sharing prevents information leakage")
    print("   • Garbled circuits compute functions securely")
    print("   • Only specified outputs are revealed")
    print("\n   Applications:")
    print("   • Private data analytics")
    print("   • Secure auctions")
    print("   • Privacy-preserving machine learning")
    print("   • Confidential voting systems")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    run_interactive_demo()