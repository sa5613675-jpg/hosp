#!/usr/bin/env python
"""
Prepare system for production deployment
- Remove fake patient data
- Add real lab tests
- Clear medicine stock
- Clear financial records
- Keep all user accounts
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model
from appointments.models import Appointment, Patient
from lab.models import LabTest, LabOrder, LabResult, LabBill
from pharmacy.models import Drug, PharmacySale, SaleItem, StockAdjustment
from finance.models import Income, Expense

User = get_user_model()

def clear_patient_data():
    """Remove all patient and appointment data"""
    print("\n" + "="*80)
    print("STEP 1: Clearing Patient Data")
    print("="*80)
    
    # Delete appointments
    appointment_count = Appointment.objects.count()
    Appointment.objects.all().delete()
    print(f"✓ Deleted {appointment_count} appointments")
    
    # Delete patients
    patient_count = Patient.objects.count()
    Patient.objects.all().delete()
    print(f"✓ Deleted {patient_count} patients")

def clear_lab_data():
    """Remove old lab tests and add new ones"""
    print("\n" + "="*80)
    print("STEP 2: Clearing Old Lab Data & Adding New Tests")
    print("="*80)
    
    # Delete lab bills, orders, results
    LabBill.objects.all().delete()
    LabOrder.objects.all().delete()
    LabResult.objects.all().delete()
    print("✓ Cleared all lab bills, orders, and results")
    
    # Delete old lab tests
    old_tests = LabTest.objects.count()
    LabTest.objects.all().delete()
    print(f"✓ Deleted {old_tests} old lab tests")
    
    # Add new lab tests from Universal Health Services And Diagnostic Center
    lab_tests = [
        # Cell Counter (Hematology Exam)
        {"name": "CBC", "category": "Hematology", "lab_category": "BLOOD", "price": 300, "sample": "Blood"},
        {"name": "Hb%", "category": "Hematology", "lab_category": "BLOOD", "price": 100, "sample": "Blood"},
        {"name": "CE Count", "category": "Hematology", "lab_category": "BLOOD", "price": 150, "sample": "Blood"},
        {"name": "Platelet Count", "category": "Hematology", "lab_category": "BLOOD", "price": 200, "sample": "Blood"},
        {"name": "C.PBF", "category": "Hematology", "lab_category": "BLOOD", "price": 250, "sample": "Blood"},
        {"name": "MP (Malarial Parasite)", "category": "Hematology", "lab_category": "BLOOD", "price": 150, "sample": "Blood"},
        {"name": "BT, CT", "category": "Hematology", "lab_category": "BLOOD", "price": 100, "sample": "Blood"},
        {"name": "ESR", "category": "Hematology", "lab_category": "BLOOD", "price": 100, "sample": "Blood"},
        {"name": "TCR", "category": "Hematology", "lab_category": "BLOOD", "price": 150, "sample": "Blood"},
        {"name": "RBC", "category": "Hematology", "lab_category": "BLOOD", "price": 150, "sample": "Blood"},
        
        # Biochemistry Analyzer
        {"name": "Fasting/RBS", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 100, "sample": "Blood"},
        {"name": "2 hrs ABF/Lunch/Dinner/75gm glucose", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 150, "sample": "Blood"},
        {"name": "Urine Sugar", "category": "Biochemistry", "lab_category": "URINE", "price": 50, "sample": "Urine"},
        {"name": "S.Bilirubin (Total/Direct/Indirect)", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 300, "sample": "Blood"},
        {"name": "S.GPT", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 200, "sample": "Blood"},
        {"name": "S.GOT", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 200, "sample": "Blood"},
        {"name": "Alk. Phosphatase", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 250, "sample": "Blood"},
        {"name": "LFT (Liver Function Test)", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 800, "sample": "Blood"},
        {"name": "Lipid Profile", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 600, "sample": "Blood"},
        {"name": "Triglyceride", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 200, "sample": "Blood"},
        {"name": "Cholesterol", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 150, "sample": "Blood"},
        {"name": "Total Cholesterol", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 200, "sample": "Blood"},
        {"name": "HDL Cholesterol", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 250, "sample": "Blood"},
        {"name": "S. Calcium", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 200, "sample": "Blood"},
        {"name": "S. Uric Acid", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 200, "sample": "Blood"},
        {"name": "Blood Urea", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 200, "sample": "Blood"},
        {"name": "S. Amylase", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 300, "sample": "Blood"},
        {"name": "Total Protein", "category": "Biochemistry", "lab_category": "BIOCHEMISTRY", "price": 250, "sample": "Blood"},
        
        # Digital X-Ray
        {"name": "Chest P/A view/Lat. View", "category": "X-Ray", "lab_category": "IMAGING", "price": 500, "sample": "N/A"},
        {"name": "Ba meal/Swallow & Duodenum", "category": "X-Ray", "lab_category": "IMAGING", "price": 1200, "sample": "N/A"},
        {"name": "Ba Enema/Double Contrast", "category": "X-Ray", "lab_category": "IMAGING", "price": 1500, "sample": "N/A"},
        {"name": "K.U.B", "category": "X-Ray", "lab_category": "IMAGING", "price": 600, "sample": "N/A"},
        {"name": "I.V.U With post mict. film", "category": "X-Ray", "lab_category": "IMAGING", "price": 1000, "sample": "N/A"},
        {"name": "Other X-Ray Abdomen", "category": "X-Ray", "lab_category": "IMAGING", "price": 500, "sample": "N/A"},
        {"name": "Skull P/A/P/N S", "category": "X-Ray", "lab_category": "IMAGING", "price": 600, "sample": "N/A"},
        {"name": "Cervical Spine B.V", "category": "X-Ray", "lab_category": "IMAGING", "price": 700, "sample": "N/A"},
        {"name": "Lumbo Sacral Spin B.V", "category": "X-Ray", "lab_category": "IMAGING", "price": 700, "sample": "N/A"},
        
        # Hormonal Exam (CLIA Analyzer)
        {"name": "T3", "category": "Hormonal", "lab_category": "BIOCHEMISTRY", "price": 400, "sample": "Blood"},
        {"name": "T4", "category": "Hormonal", "lab_category": "BIOCHEMISTRY", "price": 400, "sample": "Blood"},
        {"name": "TSH", "category": "Hormonal", "lab_category": "BIOCHEMISTRY", "price": 500, "sample": "Blood"},
        {"name": "FT3", "category": "Hormonal", "lab_category": "BIOCHEMISTRY", "price": 500, "sample": "Blood"},
        {"name": "FT4", "category": "Hormonal", "lab_category": "BIOCHEMISTRY", "price": 500, "sample": "Blood"},
        {"name": "Testosterone", "category": "Hormonal", "lab_category": "BIOCHEMISTRY", "price": 600, "sample": "Blood"},
        {"name": "Vitamin (D)", "category": "Hormonal", "lab_category": "BIOCHEMISTRY", "price": 1000, "sample": "Blood"},
        {"name": "Prolactin", "category": "Hormonal", "lab_category": "BIOCHEMISTRY", "price": 600, "sample": "Blood"},
        {"name": "HBsAg (Hormonal)", "category": "Hormonal", "lab_category": "MICROBIOLOGY", "price": 400, "sample": "Blood"},
        {"name": "IgE", "category": "Hormonal", "lab_category": "BIOCHEMISTRY", "price": 800, "sample": "Blood"},
        {"name": "Troponin I", "category": "Hormonal", "lab_category": "BIOCHEMISTRY", "price": 1200, "sample": "Blood"},
        
        # Electrolyte Analyzer
        {"name": "S. Electrolytes (Na, K, Cl)", "category": "Electrolyte", "lab_category": "BIOCHEMISTRY", "price": 500, "sample": "Blood"},
        
        # HPLC Analyzer
        {"name": "HbA1c", "category": "HPLC", "lab_category": "BIOCHEMISTRY", "price": 800, "sample": "Blood"},
        
        # Protein Analyzer
        {"name": "A/G Titre", "category": "Protein", "lab_category": "BIOCHEMISTRY", "price": 300, "sample": "Blood"},
        {"name": "CRP", "category": "Protein", "lab_category": "BIOCHEMISTRY", "price": 400, "sample": "Blood"},
        {"name": "UCRP", "category": "Protein", "lab_category": "BIOCHEMISTRY", "price": 500, "sample": "Blood"},
        
        # Serology Exam
        {"name": "Widal Test", "category": "Serology", "lab_category": "MICROBIOLOGY", "price": 250, "sample": "Blood"},
        {"name": "Weil Felix Test", "category": "Serology", "lab_category": "MICROBIOLOGY", "price": 300, "sample": "Blood"},
        {"name": "Febrile Antigen", "category": "Serology", "lab_category": "MICROBIOLOGY", "price": 350, "sample": "Blood"},
        {"name": "VDRL", "category": "Serology", "lab_category": "MICROBIOLOGY", "price": 300, "sample": "Blood"},
        {"name": "TPHA", "category": "Serology", "lab_category": "MICROBIOLOGY", "price": 400, "sample": "Blood"},
        {"name": "HBsAg", "category": "Serology", "lab_category": "MICROBIOLOGY", "price": 400, "sample": "Blood"},
        {"name": "Blood Grouping & Rh Factor", "category": "Serology", "lab_category": "BLOOD", "price": 200, "sample": "Blood"},
        {"name": "Dengue NS1 Antigen - IgG, IgM", "category": "Serology", "lab_category": "MICROBIOLOGY", "price": 800, "sample": "Blood"},
        {"name": "Pregnancy Test", "category": "Serology", "lab_category": "OTHER", "price": 100, "sample": "Urine"},
        {"name": "ICT for Malaria", "category": "Serology", "lab_category": "MICROBIOLOGY", "price": 300, "sample": "Blood"},
        
        # Stool Exam
        {"name": "Stool R/E", "category": "Stool", "lab_category": "STOOL", "price": 100, "sample": "Stool"},
        {"name": "Stool OBT", "category": "Stool", "lab_category": "STOOL", "price": 150, "sample": "Stool"},
        
        # Urine Exam
        {"name": "Urine P/T (Pregnancy Test)", "category": "Urine", "lab_category": "URINE", "price": 100, "sample": "Urine"},
        {"name": "Urine R/E", "category": "Urine", "lab_category": "URINE", "price": 100, "sample": "Urine"},
        {"name": "Glucose, Albumin Protein", "category": "Urine", "lab_category": "URINE", "price": 150, "sample": "Urine"},
        {"name": "Ketone, Bilirubin", "category": "Urine", "lab_category": "URINE", "price": 150, "sample": "Urine"},
        {"name": "Urobilinogen, pH", "category": "Urine", "lab_category": "URINE", "price": 100, "sample": "Urine"},
        {"name": "Specific Gravity, Blood", "category": "Urine", "lab_category": "URINE", "price": 100, "sample": "Urine"},
        {"name": "Nitrite, Leukocytes", "category": "Urine", "lab_category": "URINE", "price": 150, "sample": "Urine"},
        
        # Ultrasonography
        {"name": "U.S.G Color Doppler", "category": "USG", "lab_category": "IMAGING", "price": 1500, "sample": "N/A"},
        {"name": "USG of Whole Abdomen", "category": "USG", "lab_category": "IMAGING", "price": 1000, "sample": "N/A"},
        {"name": "USG of Upper Abdomen", "category": "USG", "lab_category": "IMAGING", "price": 800, "sample": "N/A"},
        {"name": "USG of Lower Abdomen", "category": "USG", "lab_category": "IMAGING", "price": 800, "sample": "N/A"},
        {"name": "Genita-Urinary System (GUS)", "category": "USG", "lab_category": "IMAGING", "price": 900, "sample": "N/A"},
        {"name": "Kidneys, Ureter, Urinary Bladder, Prostate", "category": "USG", "lab_category": "IMAGING", "price": 900, "sample": "N/A"},
        {"name": "Testes/Testis (L/R)", "category": "USG", "lab_category": "IMAGING", "price": 700, "sample": "N/A"},
        {"name": "Early Pregnancy", "category": "USG", "lab_category": "IMAGING", "price": 600, "sample": "N/A"},
        {"name": "Normal Pregnancy", "category": "USG", "lab_category": "IMAGING", "price": 800, "sample": "N/A"},
        {"name": "Pregnancy Profile", "category": "USG", "lab_category": "IMAGING", "price": 1200, "sample": "N/A"},
        {"name": "Missed or Incomplete Abortion", "category": "USG", "lab_category": "IMAGING", "price": 800, "sample": "N/A"},
        {"name": "Liver, Gallbladder, Pancreas (HBS)", "category": "USG", "lab_category": "IMAGING", "price": 900, "sample": "N/A"},
        {"name": "Thyroid", "category": "USG", "lab_category": "IMAGING", "price": 700, "sample": "N/A"},
        {"name": "Breast", "category": "USG", "lab_category": "IMAGING", "price": 800, "sample": "N/A"},
        
        # Others
        {"name": "MT (Tuberculin Test)", "category": "Others", "lab_category": "MICROBIOLOGY", "price": 200, "sample": "Skin"},
        {"name": "Semen Analysis", "category": "Others", "lab_category": "PATHOLOGY", "price": 500, "sample": "Semen"},
        
        # ECHO
        {"name": "ECHO (Echocardiogram Color Doppler)", "category": "ECHO", "lab_category": "IMAGING", "price": 2000, "sample": "N/A"},
        
        # ECG
        {"name": "ECG", "category": "ECG", "lab_category": "OTHER", "price": 300, "sample": "N/A"},
    ]
    
    created_count = 0
    for test_data in lab_tests:
        # Generate test code from name
        test_code = test_data["name"][:10].upper().replace(" ", "").replace(".", "").replace(",", "").replace("/", "")
        if len(test_code) < 3:
            test_code = test_data["category"][:3].upper() + str(created_count + 1)
        
        test = LabTest.objects.create(
            test_code=test_code + str(created_count + 1),
            test_name=test_data["name"],
            category=test_data.get("lab_category", "OTHER"),
            price=test_data["price"],
            description=f"{test_data['name']} - Universal Health Services And Diagnostic Center",
            sample_type=test_data.get("sample", "As per test requirement"),
            turnaround_time="24-48 hours",
            is_active=True
        )
        created_count += 1
    
    print(f"✓ Created {created_count} new lab tests from Universal Health Services And Diagnostic Center")

def clear_pharmacy_stock():
    """Remove all medicine stock"""
    print("\n" + "="*80)
    print("STEP 3: Clearing Pharmacy Stock")
    print("="*80)
    
    # Delete sales
    sale_count = PharmacySale.objects.count()
    PharmacySale.objects.all().delete()
    print(f"✓ Deleted {sale_count} pharmacy sales")
    
    # Delete sale items
    SaleItem.objects.all().delete()
    print("✓ Deleted all sale items")
    
    # Delete stock adjustments
    adjustment_count = StockAdjustment.objects.count()
    StockAdjustment.objects.all().delete()
    print(f"✓ Deleted {adjustment_count} stock adjustments")
    
    # Reset all medicine quantities to 0
    drug_count = Drug.objects.count()
    Drug.objects.all().update(quantity_in_stock=0)
    print(f"✓ Reset stock quantity to 0 for {drug_count} medicines")

def clear_financial_data():
    """Clear all financial records"""
    print("\n" + "="*80)
    print("STEP 4: Clearing Financial Data")
    print("="*80)
    
    # Delete income records
    income_count = Income.objects.count()
    Income.objects.all().delete()
    print(f"✓ Deleted {income_count} income records")
    
    # Delete expense records
    expense_count = Expense.objects.count()
    Expense.objects.all().delete()
    print(f"✓ Deleted {expense_count} expense records")

def show_kept_accounts():
    """Show all accounts that are kept"""
    print("\n" + "="*80)
    print("STEP 5: Accounts Kept (NOT Deleted)")
    print("="*80)
    
    users = User.objects.all().order_by('role', 'username')
    print(f"\nTotal Users: {users.count()}\n")
    
    for user in users:
        print(f"✓ {user.role}: {user.username} - {user.get_full_name()}")
        if user.phone:
            print(f"  Phone: {user.phone}")

def main():
    print("\n" + "="*100)
    print("                    PREPARING SYSTEM FOR PRODUCTION")
    print("="*100)
    print("Hospital: Universal Health Services And Diagnostic Center")
    print("="*100)
    
    try:
        # Step 1: Clear patient data
        clear_patient_data()
        
        # Step 2: Clear and add lab tests
        clear_lab_data()
        
        # Step 3: Clear pharmacy stock
        clear_pharmacy_stock()
        
        # Step 4: Clear financial data
        clear_financial_data()
        
        # Step 5: Show kept accounts
        show_kept_accounts()
        
        print("\n" + "="*100)
        print("✓ PRODUCTION PREPARATION COMPLETE!")
        print("="*100)
        print("\nSystem is now ready for production deployment!")
        print("All user accounts (doctors, admin, receptionist, etc.) are preserved.")
        print("All fake data has been removed.")
        print("New lab tests from Universal Health Services added.")
        print("\n" + "="*100)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
