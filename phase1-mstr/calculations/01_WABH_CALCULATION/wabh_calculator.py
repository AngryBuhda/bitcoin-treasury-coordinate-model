"""
WABH Calculator - Weighted Average Block Height
Bitcoin Treasury Coordinate Model - Phase 1
"""

import csv
from pathlib import Path

def load_tranche_data(filepath):
    """Load tranche history CSV and return list of tranches"""
    tranches = []
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tranche = {
                'date': row['Date'],
                'btc': float(row['BTC_Amount']),
                'price': float(row['Avg_Price_Per_BTC']),
                'total_btc': float(row['Total_BTC_Holdings']),
                'block_height': float(row['Block_Height_Estimate'])
            }
            tranches.append(tranche)
    
    return tranches

def calculate_wabh(tranches):
    """
    Calculate Weighted Average Block Height
    
    WABH = Sum(BTC_Amount * Block_Height) / Sum(BTC_Amount)
    """
    
    # Calculate total BTC
    total_btc = sum(t['btc'] for t in tranches)
    
    if total_btc == 0:
        return None, 0
    
    # Calculate weighted sum
    weighted_sum = sum(t['btc'] * t['block_height'] for t in tranches)
    
    # Calculate WABH
    wabh = weighted_sum / total_btc
    
    return wabh, total_btc

def main():
    """Main execution"""
    
    # Load data
    data_file = '../../data/01_TRANCHE_HISTORY/mstr_tranches_raw.csv'
    
    print("\n" + "="*70)
    print("WABH CALCULATOR - Weighted Average Block Height")
    print("="*70)
    
    try:
        tranches = load_tranche_data(data_file)
        print(f"✓ Loaded {len(tranches)} tranches from CSV")
    except FileNotFoundError:
        print(f"✗ Error: Could not find {data_file}")
        return
    
    # Calculate WABH
    wabh, total_btc = calculate_wabh(tranches)
    
    # Expected values
    expected_wabh = 785000
    tolerance = 7850  # 1%
    
    # Display results
    print(f"\nCalculation Results:")
    print(f"-" * 70)
    print(f"Total BTC Holdings: {total_btc:,.0f}")
    print(f"Number of tranches: {len(tranches)}")
    print(f"\nWABH Result: {wabh:,.2f} blocks")
    print(f"Expected: {expected_wabh:,.0f} ± {tolerance:,.0f}")
    print(f"Tolerance: ±1%")
    
    # Verify
    difference = abs(wabh - expected_wabh)
    
    print(f"\nVerification:")
    print(f"-" * 70)
    print(f"Difference: {difference:,.2f} blocks")
    print(f"Within tolerance: {difference <= tolerance}")
    
    if difference <= tolerance:
        print(f"✓ PASS - WABH within acceptable range")
        status = "PASS"
    else:
        print(f"✗ FAIL - WABH outside tolerance range")
        status = "FAIL"
    
    # Save results
    with open('wabh_results.txt', 'w') as f:
        f.write(f"WABH Calculation Results\n")
        f.write(f"========================\n\n")
        f.write(f"Total BTC: {total_btc:,.0f}\n")
        f.write(f"Tranches: {len(tranches)}\n")
        f.write(f"WABH: {wabh:,.2f}\n")
        f.write(f"Expected: {expected_wabh:,.0f}\n")
        f.write(f"Status: {status}\n")
    
    print(f"\n✓ Results saved to: wabh_results.txt")
    print("="*70 + "\n")
    
    return wabh

if __name__ == '__main__':
    wabh = main()
