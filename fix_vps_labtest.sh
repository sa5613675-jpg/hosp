#!/bin/bash

# VPS FIX SCRIPT - Run this on your VPS to fix the database error
# Error: no such column: lab_labtest.test_type

echo "🔧 Fixing lab_labtest.test_type column error..."
echo ""

# Step 1: Navigate to project directory
cd /root/hosp

# Step 2: Activate virtual environment
source venv/bin/activate

# Step 3: Create a Python script to add the missing column
cat > fix_labtest_column.py << 'EOF'
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.db import connection

print("Checking database...")

# Check if column exists
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(lab_labtest);")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    print(f"Current columns: {column_names}")
    
    if 'test_type' not in column_names:
        print("\n⚠️  Column 'test_type' is missing!")
        print("Adding column...")
        
        # Add the column
        cursor.execute("""
            ALTER TABLE lab_labtest 
            ADD COLUMN test_type VARCHAR(20) DEFAULT 'NORMAL' NOT NULL;
        """)
        
        print("✅ Column added successfully!")
    else:
        print("\n✅ Column 'test_type' already exists!")

# Verify
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(lab_labtest);")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    print(f"\nFinal columns: {column_names}")

print("\n✅ Database fix complete!")
EOF

# Step 4: Run the fix script
echo "Running database fix script..."
python fix_labtest_column.py

# Step 5: Run migrations to ensure everything is in sync
echo ""
echo "Running migrations..."
python manage.py migrate

# Step 6: Restart the service
echo ""
echo "Restarting service..."
sudo systemctl restart hosp

# Step 7: Check status
echo ""
echo "Checking service status..."
sudo systemctl status hosp --no-pager -l

echo ""
echo "✅ Fix complete! Check the service status above."
echo "If still having issues, check logs with: sudo journalctl -u hosp -n 50"
