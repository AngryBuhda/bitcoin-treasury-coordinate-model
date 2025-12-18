"""
Coordinate Power Calculator
Bitcoin Treasury Coordinate Model - Phase 1
"""

def calculate_coordinate_power(wabh, h_now, h_terminal):
    """
    Calculate Coordinate Power (CP)
    
    CP = (H_now - WABH) / (H_terminal - H_now)
    
    Where:
    - H_now: Current block height
    - WABH: Weighted average block height
    - H_terminal: Terminal block height (year 2140, ~21M BTC)
    """
    
    if h_terminal == h_now:
        return None
    
    cp = (h_now - wabh) / (h_terminal - h_now)
    return cp

def main():
    """Main execution"""
    
    # Constants
    H_NOW = 928000  # Current block height (Dec 18, 2025)
    H_TERMINAL = 2100000  # Year 2140
    WABH = 912456.78  # From previous calculation
    
    print("\n" + "="*70)
    print("COORDINATE POWER CALCULATOR")
    print("="*70)
    
    # Calculate CP
    cp = calculate_coordinate_power(WABH, H_NOW, H_TERMINAL)
    
    # Expected values
    expected_cp = 0.00491
    tolerance = 0.00005  # 1 basis point
    
    print(f"\nInputs:")
    print(f"-" * 70)
    print(f"WABH: {WABH:,.2f} blocks")
    print(f"H_now: {H_NOW:,} blocks")
    print(f"H_terminal: {H_TERMINAL:,} blocks")
    
    print(f"\nCalculation:")
    print(f"-" * 70)
    print(f"CP = ({H_NOW:,} - {WABH:,.0f}) / ({H_TERMINAL:,} - {H_NOW:,})")
    print(f"CP = {H_NOW - WABH:,.2f} / {H_TERMINAL - H_NOW:,}")
    print(f"CP = {cp:.6f}")
    
    print(f"\nResult:")
    print(f"-" * 70)
    print(f"Coordinate Power: {cp:.6f}")
    print(f"Expected: {expected_cp:.6f} ± {tolerance:.6f}")
    
    difference = abs(cp - expected_cp)
    
    if difference <= tolerance:
        print(f"✓ PASS - Within tolerance")
        status = "PASS"
    else:
        print(f"✗ REVIEW - Outside tolerance (difference: {difference:.6f})")
        status = "REVIEW"
    
    # Save results
    with open('cp_results.txt', 'w') as f:
        f.write(f"Coordinate Power Calculation Results\n")
        f.write(f"=====================================\n\n")
        f.write(f"CP: {cp:.6f}\n")
        f.write(f"Expected: {expected_cp:.6f}\n")
        f.write(f"Status: {status}\n")
    
    print(f"\n✓ Results saved to: cp_results.txt")
    print("="*70 + "\n")
    
    return cp

if __name__ == '__main__':
    cp = main()
