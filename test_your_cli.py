"""
Test Your CLI Interface - Phone Theft Classification
===================================================

This script simulates exactly what happens when you type 
"My phone is stolen" in your CLI interface.
"""

def test_cli_simulation():
    """Simulate the exact CLI process"""
    
    print("🖥️  SIMULATING YOUR CLI INTERFACE")
    print("=" * 60)
    
    # Import the CLI interface
    try:
        from cli_interface import LegalAgentCLI
        print("✅ CLI Interface imported successfully")
    except Exception as e:
        print(f"❌ Error importing CLI: {e}")
        return False
    
    # Create CLI instance (same as when you run it)
    try:
        cli = LegalAgentCLI(use_adaptive=False)  # Using enhanced agent
        print("✅ CLI initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing CLI: {e}")
        return False
    
    # Simulate typing "My phone is stolen"
    test_query = "My phone is stolen"
    print(f"\n👤 User types: '{test_query}'")
    print("🤖 Processing...")
    
    try:
        # This is exactly what happens when you type in the CLI
        cli.process_query(test_query)
        
        # Check what domain was classified
        if hasattr(cli, 'last_response') and cli.last_response:
            domain = cli.last_response.domain
            confidence = cli.last_response.confidence
            
            print(f"\n📊 RESULT:")
            print(f"   Domain: {domain}")
            print(f"   Confidence: {confidence:.3f}")
            
            if domain == "criminal_law":
                print("✅ SUCCESS! Your CLI now correctly classifies phone theft as Criminal Law!")
                return True
            else:
                print(f"❌ ISSUE: Still classified as {domain} instead of criminal_law")
                return False
        else:
            print("⚠️  Could not access response details")
            return False
            
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        return False


if __name__ == "__main__":
    print("🚀 TESTING YOUR CLI INTERFACE")
    print("=" * 70)
    
    success = test_cli_simulation()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 YOUR CLI IS NOW FIXED!")
        print("   You can now run: python cli_interface.py")
        print("   And type: 'My phone is stolen'")
        print("   It will be correctly classified as Criminal Law!")
    else:
        print("❌ There may still be issues with your CLI")
        print("   Try running the CLI directly to see what happens")
    
    print("\n💡 To test your CLI:")
    print("   1. Open terminal")
    print("   2. Run: python cli_interface.py")
    print("   3. Type: My phone is stolen")
    print("   4. Should show: Criminal Law (not Cyber Crime)")