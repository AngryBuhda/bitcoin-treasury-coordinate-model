"""
WABH Calculator - Marathon Digital
Bitcoin Treasury Coordinate Model - Phase 2
"""

import csv
import os

def load_tranche_data():
    """Load Marathon tranche data"""
    tranches = []
    
    # Get current directory and build path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, '..', 'data', 'mara_tranches_raw.csv')
    
    print(f"Looking for file: {data_file}")
    
    with open(data_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tranche = {
                'date': row['Date'],
                'btc': float(row['BTC_Amount']),
                'block_height': float(row['Block_Height_Estimate'])
            }
            tranches.append(tranche)
    return tranches

def calculate_wabh(tranches):
    """Calculate WABH"""
    total_btc = sum(t['btc'] for t in tranches)
    if total_btc == 0:
        return None, 0
    
    weighted_sum = sum(t['btc'] * t['block_height'] for t in tranches)
    wabh = weighted_sum / total_btc
    
    return wabh, total_btc

def main():
    print("\n" + "="*70)
    print("MARATHON DIGITAL - WABH CALCULATION")
    print("="*70)
    
    try:
        tranches = load_tranche_data()
        wabh, total_btc = calculate_wabh(tranches)
        
        print(f"\n✓ File loaded successfully!")
        print(f"\nTotal BTC: {total_btc:,.0f}")
        print(f"Number of tranches: {len(tranches)}")
        print(f"WABH: {wabh:,.2f} blocks")
        print(f"Expected current block: 928,000")
        
        print("\n✓ MARA WABH calculation complete")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print(f"Please check that mara_tranches_raw.csv exists in the data folder")
        print("="*70 + "\n")

if __name__ == '__main__':
    main()
