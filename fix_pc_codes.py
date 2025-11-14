#!/usr/bin/env python
"""
Fix PC Member Codes - Update from 5-digit to 6-digit format
Run this script to update existing PC member codes
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import PCMember

print("=" * 60)
print("PC MEMBER CODE FORMAT FIX")
print("=" * 60)
print("\nUpdating PC codes from 5-digit to 6-digit format...")
print("Format: 10001 → 100001, 20001 → 200001, 30001 → 300001\n")

# Get all PC members
members = PCMember.objects.all().order_by('pc_code')

updated_count = 0
skipped_count = 0

for member in members:
    old_code = member.pc_code
    
    # Check if has "PC" prefix (old format)
    if old_code.startswith('PC') and len(old_code) == 7:
        # Extract the numeric part (e.g., PC10001 → 10001)
        numeric_part = old_code[2:]  # Remove "PC"
        
        if len(numeric_part) == 5 and numeric_part[0] in ['1', '2', '3']:
            # Convert 5-digit to 6-digit
            prefix = numeric_part[0]
            number = numeric_part[1:]
            new_code = f"{prefix}{number.zfill(5)}"  # Makes it 100001, 200001, 300001
            
            # Update the code
            member.pc_code = new_code
            member.save()
            
            print(f"✓ UPDATED: {old_code} → {new_code} - {member.name}")
            updated_count += 1
        else:
            print(f"⚠ SKIP: {old_code} - {member.name} (unexpected format)")
            skipped_count += 1
    
    # Check if already 6-digit format without prefix
    elif len(old_code) == 6 and old_code[0] in ['1', '2', '3']:
        print(f"✓ SKIP: {old_code} - {member.name} (already 6-digit)")
        skipped_count += 1
    
    # Check if 5-digit format without prefix
    elif len(old_code) == 5 and old_code[0] in ['1', '2', '3']:
        # Convert to 6-digit by padding
        prefix = old_code[0]
        number = old_code[1:]
        new_code = f"{prefix}{number.zfill(5)}"
        
        # Update the code
        member.pc_code = new_code
        member.save()
        
        print(f"✓ UPDATED: {old_code} → {new_code} - {member.name}")
        updated_count += 1
    
    else:
        # Custom format, don't change
        print(f"⚠ SKIP: {old_code} - {member.name} (custom format)")
        skipped_count += 1

print("\n" + "=" * 60)
print("SUMMARY:")
print(f"  Updated: {updated_count} PC members")
print(f"  Skipped: {skipped_count} PC members")
print(f"  Total: {members.count()} PC members")
print("=" * 60)

if updated_count > 0:
    print("\n✅ PC member codes updated successfully!")
    print("Please verify the codes in the admin panel or PC dashboard.")
else:
    print("\n✓ All PC codes are already in the correct format.")
