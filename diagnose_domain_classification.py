#!/usr/bin/env python3
"""
Domain Classification Diagnosis & Fix Tool
==========================================

This script diagnoses and fixes domain classification issues to ensure
queries return correct domains instead of "unknown" or wrong domains.

Author: Legal Agent Team
Date: 2025-08-28
"""

import sys
import json
import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Any

def load_training_data() -> List[Dict]:
    """Load training data to analyze domains"""
    try:
        with open('training_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading training data: {e}")
        return []

def analyze_training_data(training_data: List[Dict]) -> Dict[str, Any]:
    """Analyze training data structure"""
    
    domains = {}
    for item in training_data:
        domain = item.get('domain', 'unknown')
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(item.get('text', ''))
    
    return {
        'total_examples': len(training_data),
        'unique_domains': len(domains),
        'domains': domains,
        'domain_counts': {domain: len(examples) for domain, examples in domains.items()}
    }

def test_ml_classifier():
    """Test the ML classifier with various queries"""
    
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        
        classifier = create_ml_domain_classifier()
        
        # Critical test queries that should return specific domains
        test_queries = [
            ("my phone is being hacked by someone", "cyber_crime"),
            ("my boss is not giving my salary", "employment_law"),
            ("landlord not returning deposit", "tenant_rights"),
            ("bought defective phone want refund", "consumer_complaint"),
            ("my husband beats me daily", "family_law"),
            ("I was raped by my neighbor", "criminal_law"),
            ("visa application denied", "immigration_law"),
            ("contract was breached", "contract_dispute"),
            ("elderly father being abused", "elder_abuse"),
            ("injured in car accident need compensation", "personal_injury")
        ]
        
        results = []
        print("🧪 TESTING ML CLASSIFIER:")
        print("-" * 50)
        
        for query, expected in test_queries:
            try:
                domain, confidence, alternatives = classifier.classify_with_confidence(query)
                
                # Status indicators
                if domain == expected:
                    status = "✅ CORRECT"
                elif domain == "unknown":
                    status = "❌ UNKNOWN"
                else:
                    status = f"⚠️ WRONG (got {domain})"
                
                results.append({
                    'query': query,
                    'expected': expected,
                    'actual': domain,
                    'confidence': confidence,
                    'correct': domain == expected,
                    'unknown': domain == "unknown"
                })
                
                print(f"{status}")
                print(f"   Query: \"{query}\"")
                print(f"   Expected: {expected}")
                print(f"   Got: {domain} (confidence: {confidence:.3f})")
                
                if domain != expected and alternatives:
                    print(f"   Alternatives: {alternatives[:3]}")
                
                print()
                
            except Exception as e:
                print(f"❌ Error testing query '{query}': {e}")
                results.append({
                    'query': query,
                    'expected': expected,
                    'actual': 'ERROR',
                    'confidence': 0.0,
                    'correct': False,
                    'unknown': False,
                    'error': str(e)
                })
        
        return classifier, results
        
    except Exception as e:
        print(f"❌ Cannot load ML classifier: {e}")
        return None, []

def analyze_classifier_performance(results: List[Dict]) -> Dict[str, Any]:
    """Analyze classifier performance"""
    
    if not results:
        return {'error': 'No results to analyze'}
    
    total = len(results)
    correct = sum(1 for r in results if r.get('correct', False))
    unknown = sum(1 for r in results if r.get('unknown', False))
    wrong = sum(1 for r in results if not r.get('correct', False) and not r.get('unknown', False))
    
    return {
        'total_queries': total,
        'correct_classifications': correct,
        'unknown_classifications': unknown,
        'wrong_classifications': wrong,
        'accuracy_percentage': (correct / total) * 100 if total > 0 else 0,
        'unknown_percentage': (unknown / total) * 100 if total > 0 else 0,
        'wrong_percentage': (wrong / total) * 100 if total > 0 else 0
    }

def suggest_fixes(analysis: Dict[str, Any], classifier_results: List[Dict]) -> List[str]:
    """Suggest fixes based on analysis"""
    
    fixes = []
    
    # Analyze common issues
    unknown_queries = [r for r in classifier_results if r.get('unknown', False)]
    wrong_queries = [r for r in classifier_results if not r.get('correct', False) and not r.get('unknown', False)]
    
    if len(unknown_queries) > len(classifier_results) * 0.3:  # More than 30% unknown
        fixes.append("HIGH PRIORITY: Lower confidence threshold in ml_domain_classifier.py")
        fixes.append("  - Change self.confidence_threshold from current value to 0.01")
        fixes.append("  - Change self.cosine_threshold to 0.01")
    
    if len(wrong_queries) > len(classifier_results) * 0.2:  # More than 20% wrong
        fixes.append("MEDIUM PRIORITY: Retrain model with more diverse training data")
        fixes.append("  - Add more training examples for problematic domains")
        fixes.append("  - Balance training data across all domains")
    
    # Check specific domain issues
    domain_issues = {}
    for result in classifier_results:
        if not result.get('correct', False):
            expected = result.get('expected')
            if expected not in domain_issues:
                domain_issues[expected] = []
            domain_issues[expected].append(result)
    
    for domain, failed_results in domain_issues.items():
        if len(failed_results) > 1:  # Multiple failures for same domain
            fixes.append(f"DOMAIN SPECIFIC: Fix {domain} classification")
            fixes.append(f"  - Add more training examples for {domain}")
            fixes.append(f"  - Check keyword patterns for {domain}")
    
    # Model loading issues
    if any('error' in r for r in classifier_results):
        fixes.append("CRITICAL: Fix model loading/training issues")
        fixes.append("  - Check if models are properly trained")
        fixes.append("  - Verify training data format")
        fixes.append("  - Ensure model files exist and are valid")
    
    return fixes

def apply_automatic_fixes(classifier):
    """Apply automatic fixes to improve classification"""
    
    fixes_applied = []
    
    try:
        # Fix 1: Lower confidence thresholds
        if hasattr(classifier, 'confidence_threshold') and classifier.confidence_threshold > 0.05:
            classifier.confidence_threshold = 0.01
            fixes_applied.append("✅ Lowered confidence_threshold to 0.01")
        
        if hasattr(classifier, 'cosine_threshold') and classifier.cosine_threshold > 0.05:
            classifier.cosine_threshold = 0.01
            fixes_applied.append("✅ Lowered cosine_threshold to 0.01")
        
        # Fix 2: Retrain if needed
        if hasattr(classifier, 'is_trained') and not classifier.is_trained:
            if hasattr(classifier, 'train_models'):
                success = classifier.train_models()
                if success:
                    fixes_applied.append("✅ Retrained ML models")
                else:
                    fixes_applied.append("❌ Failed to retrain ML models")
        
        # Fix 3: Save updated models if fixes applied
        if fixes_applied and hasattr(classifier, 'save_models'):
            classifier.save_models()
            fixes_applied.append("✅ Saved updated models")
            
    except Exception as e:
        fixes_applied.append(f"❌ Error applying fixes: {e}")
    
    return fixes_applied

def main():
    """Main diagnosis and fix function"""
    
    print("🔍 DOMAIN CLASSIFICATION DIAGNOSIS TOOL")
    print("=" * 60)
    print("Diagnosing domain classification issues...")
    print("=" * 60)
    print()
    
    # Step 1: Analyze training data
    print("📊 STEP 1: ANALYZING TRAINING DATA")
    print("-" * 40)
    
    training_data = load_training_data()
    if not training_data:
        print("❌ Cannot proceed without training data")
        return 1
    
    analysis = analyze_training_data(training_data)
    
    print(f"✅ Training Data Analysis:")
    print(f"   Total examples: {analysis['total_examples']}")
    print(f"   Unique domains: {analysis['unique_domains']}")
    print(f"   Domains: {list(analysis['domains'].keys())}")
    print()
    
    for domain, count in analysis['domain_counts'].items():
        print(f"   - {domain}: {count} examples")
    print()
    
    # Step 2: Test ML Classifier
    print("🤖 STEP 2: TESTING ML CLASSIFIER")
    print("-" * 40)
    
    classifier, results = test_ml_classifier()
    
    if not classifier:
        print("❌ Cannot test classifier - initialization failed")
        return 1
    
    # Step 3: Analyze Performance
    print("📈 STEP 3: PERFORMANCE ANALYSIS")
    print("-" * 40)
    
    performance = analyze_classifier_performance(results)
    
    print(f"✅ Classification Performance:")
    print(f"   Total queries tested: {performance['total_queries']}")
    print(f"   Correct classifications: {performance['correct_classifications']} ({performance['accuracy_percentage']:.1f}%)")
    print(f"   Unknown classifications: {performance['unknown_classifications']} ({performance['unknown_percentage']:.1f}%)")
    print(f"   Wrong classifications: {performance['wrong_classifications']} ({performance['wrong_percentage']:.1f}%)")
    print()
    
    # Step 4: Suggest Fixes
    print("🛠️ STEP 4: RECOMMENDED FIXES")
    print("-" * 40)
    
    fixes = suggest_fixes(analysis, results)
    
    if fixes:
        print("Recommended fixes:")
        for fix in fixes:
            print(f"   {fix}")
        print()
    else:
        print("✅ No major issues detected!")
        print()
    
    # Step 5: Apply Automatic Fixes
    print("🔧 STEP 5: APPLYING AUTOMATIC FIXES")
    print("-" * 40)
    
    auto_fixes = apply_automatic_fixes(classifier)
    
    if auto_fixes:
        print("Automatic fixes applied:")
        for fix in auto_fixes:
            print(f"   {fix}")
        print()
    else:
        print("No automatic fixes needed or available.")
        print()
    
    # Step 6: Re-test After Fixes
    if auto_fixes:
        print("🔄 STEP 6: RE-TESTING AFTER FIXES")
        print("-" * 40)
        
        _, new_results = test_ml_classifier()
        new_performance = analyze_classifier_performance(new_results)
        
        print(f"✅ Updated Performance:")
        print(f"   Accuracy: {new_performance['accuracy_percentage']:.1f}% (was {performance['accuracy_percentage']:.1f}%)")
        print(f"   Unknown: {new_performance['unknown_percentage']:.1f}% (was {performance['unknown_percentage']:.1f}%)")
        print(f"   Wrong: {new_performance['wrong_percentage']:.1f}% (was {performance['wrong_percentage']:.1f}%)")
        
        improvement = new_performance['accuracy_percentage'] - performance['accuracy_percentage']
        if improvement > 0:
            print(f"   🎉 Improvement: +{improvement:.1f}% accuracy!")
        elif improvement < 0:
            print(f"   ⚠️ Regression: {improvement:.1f}% accuracy")
        else:
            print(f"   ➡️ No change in accuracy")
        print()
    
    # Final Status
    final_accuracy = new_performance['accuracy_percentage'] if auto_fixes else performance['accuracy_percentage']
    
    print("🎯 FINAL STATUS")
    print("-" * 20)
    
    if final_accuracy >= 80:
        print(f"✅ EXCELLENT: {final_accuracy:.1f}% accuracy - Domain classification working well!")
    elif final_accuracy >= 60:
        print(f"⚠️ GOOD: {final_accuracy:.1f}% accuracy - Some improvements possible")
    else:
        print(f"❌ POOR: {final_accuracy:.1f}% accuracy - Manual fixes needed")
        print("   Recommended actions:")
        print("   1. Check training data quality")
        print("   2. Add more diverse training examples")
        print("   3. Review domain definitions")
        print("   4. Consider retraining from scratch")
    
    print()
    print("🚀 Domain classification diagnosis complete!")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)